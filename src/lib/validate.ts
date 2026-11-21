import type { Nation } from "@/data/types";
import { getForce } from "@/data/battles";
import { rosterFromForce } from "@/lib/forces";
import type { RosterState, RosterUnitLine } from "@/types/army";
import { unitPeriodBlocked } from "@/lib/periods";
import { brigadeTotal, rosterTotal } from "@/lib/points";
import {
  attachRule,
  attachTargets,
  batteriesIn,
  brigadeUnitLines,
  freeLines,
  limitText,
  optionAllowance,
  optionTaken,
  optionTakenInArmy,
  unitNoun,
} from "@/lib/options";
import {
  countByType,
  effectiveMax,
  battalionCount,
  mixedOthers,
  requirementMet,
  requirementLabel,
  unitCapRequirementMet,
  effectiveUnitCapMax,
  brigadeCountRequirementMet,
  slotUnitCount,
  countUnitsInInstance,
  armyUnitCountRequirementMet,
  countUnitsInArmy,
  choicesTaken,
  regimentsHolding,
} from "@/lib/brigadeLimits";

export interface ValidationIssue {
  /**
   * "error": something breaks the list's rules (too many, not allowed, can't be combined). "todo":
   * something the list still needs (a commander, a brigade's minimum), the normal state of a list
   * that's still being built, so it's shown calmly rather than as a mistake. "historical": a list started
   * from a historical force breaks the rules here just as that force did, so it's shown as the history
   * rather than a mistake (see `validateRoster`).
   */
  level: "error" | "todo" | "historical";
  /** A todo the slot's own badge already shows ("needs 1–2"), so the brigade card needn't repeat it */
  shownOnSlot?: boolean;
  message: string;
  /** The brigade instance this issue is about, when it's about one brigade rather than the whole army */
  brigadeKey?: string;
}

/**
 * What breaks the list's rules, and what it still needs. A list started from a historical force
 * (`sourceForceId`) has whatever that force itself breaks marked "historical" instead: the same issue,
 * about the same brigade, in the force as it was built. Change it so the issue reads differently (more
 * Light battalions than history had, say) and it's an ordinary issue again.
 */
export function validateRoster(nation: Nation, roster: RosterState): ValidationIssue[] {
  const issues = rulesIssues(nation, roster);
  const force = roster.sourceForceId ? getForce(roster.sourceForceId) : undefined;
  if (!force || force.nationId !== nation.id || issues.length === 0) return issues;
  // The force as built, with the list's own names and period, so renaming a brigade or choosing
  // another period doesn't change how its issues read
  const template = rosterFromForce(nation, force).roster;
  const names = new Map(roster.brigadeInstances.map((b) => [b.key, b.name]));
  template.armyName = roster.armyName;
  template.period = roster.period;
  template.brigadeInstances = template.brigadeInstances.map((b) => (names.has(b.key) ? { ...b, name: names.get(b.key) } : b));
  const id = (i: ValidationIssue) => `${i.brigadeKey ?? ""}\u0000${i.message}`;
  const historical = new Set(rulesIssues(nation, template).map(id));
  return issues.map((i) => (historical.has(id(i)) ? { ...i, level: "historical" as const } : i));
}

function rulesIssues(nation: Nation, roster: RosterState): ValidationIssue[] {
  const issues: ValidationIssue[] = [];

  // Determine which Command units are army-level (not tied to a brigade as its required commander)
  const brigadeCommanderIds = new Set(
    nation.brigades.map((b) => b.commanderUnitId).filter((id): id is string => Boolean(id))
  );
  const hasArmyCommandUnits = nation.units.some(
    (u) => u.category === "Command" && !brigadeCommanderIds.has(u.id)
  );

  const commandTotal = roster.commandItems.reduce((s, l) => s + l.qty, 0);
  if (hasArmyCommandUnits && commandTotal === 0 && !nation.armyCommandOptional) {
    issues.push({
      level: "todo",
      message: "Army Command: an army commander is required",
    });
  }
  if (commandTotal > 1) {
    issues.push({
      level: "error",
      message: `Army Command: only one army commander allowed (have ${commandTotal})`,
    });
  }

  // ─── Choices from another campaign period than the list's (Peninsular Early, Middle, Late) ───
  issues.push(...periodIssues(nation, roster));

  // Army total points (used for per-points caps like Earthworks "1 per 500 points")
  const armyTotalPoints = rosterTotal(nation, roster);

  for (const bt of nation.brigades) {
    const count = countByType(roster.brigadeInstances, bt.id);
    if (count < bt.min) {
      issues.push({
        level: "todo",
        message: `${bt.name}: needs at least ${bt.min} (have ${count})`,
      });
    }
    // Per-points minimum floor, e.g. "at least 1 Line Brigade per 500 points"
    if (bt.minPerPoints && armyTotalPoints > 0) {
      const requiredByPoints = Math.ceil(armyTotalPoints / bt.minPerPoints.perPoints);
      if (count < requiredByPoints) {
        issues.push({
          level: "todo",
          message: `${bt.name}: needs at least ${requiredByPoints} for a ${armyTotalPoints}-point army (1 per ${bt.minPerPoints.perPoints} points; have ${count})`,
        });
      }
    }
    const max = effectiveMax(bt, roster.brigadeInstances);
    if (count > max) {
      const cappedByNames = bt.maxRatio?.brigadeTypeIds.map(
        (id) => nation.brigades.find((b) => b.id === id)?.name ?? id
      );
      issues.push({
        level: "error",
        message: `${bt.name}: maximum ${max} allowed right now (have ${count})${
          cappedByNames ? ` — capped by ${cappedByNames.join("/")} taken` : ""
        }`,
      });
    }

    if (count > 0 && !requirementMet(bt, roster.brigadeInstances)) {
      const label = requirementLabel(bt, nation.brigades);
      issues.push({
        level: "error",
        message: `${bt.name}: ${label ?? "prerequisite brigade not met"} (have ${count})`,
      });
    }
  }

  for (const bt of nation.brigades) {
    const instances = roster.brigadeInstances.filter((bi) => bi.brigadeTypeId === bt.id);
    if (instances.length === 0) continue;

    if (bt.commanderUnitId) {
      const missing = instances.filter((bi) => !bi.commanderLine).length;
      if (missing > 0) {
        issues.push({
          level: "todo",
          message: `${bt.name}: ${missing} brigade${missing === 1 ? "" : "s"} missing a Brigade Commander`,
        });
      }
    }

    // ─── Per-instance: max total battalions across all slots ──────────────
    if (bt.maxBattalions) {
      const cap = bt.maxBattalions;
      const noun = cap.noun ?? "battalions";
      for (const bi of instances) {
        const count = battalionCount(bt, bi);
        if (count > cap.max) {
          issues.push({
            level: "error",
            brigadeKey: bi.key,
            message: `${bt.name}: maximum ${cap.max} ${noun} per brigade (have ${count})`,
          });
        } else if (cap.min !== undefined && count < cap.min) {
          issues.push({
            level: "todo",
            brigadeKey: bi.key,
            message: `${bt.name}: needs at least ${cap.min} ${cap.min === 1 ? noun.replace(/s$/, "") : noun} (has ${count})`,
          });
        }
      }
    }

    // ─── Per-instance: a brigade mostly of one class ───────────────────────
    if (bt.mixLimit) {
      for (const bi of instances) {
        const others = mixedOthers(bt, bi);
        if (others > bt.mixLimit.maxOthers) {
          const labels = bt.mixLimit.groups.map((g) => g.label).join(" or all ");
          issues.push({
            level: "error",
            brigadeKey: bi.key,
            message:
              bt.mixLimit.maxOthers === 0
                ? `${bt.name}: regiments should be all ${labels} (has ${others} of the other)`
                : `${bt.name}: regiments should be all ${labels}, with up to ${bt.mixLimit.maxOthers} of the other (has ${others})`,
          });
        }
      }
    }

    // ─── Per-instance: max combined regiments across regiment slots ───────
    if (bt.maxRegimentsTotal) {
      for (const bi of instances) {
        const regTotal = bt.maxRegimentsTotal.slotIndices.reduce(
          (sum, si) => sum + (bi.regimentSlots?.[si]?.length ?? 0), 0
        );
        if (regTotal > bt.maxRegimentsTotal.max) {
          issues.push({
            level: "error",
            brigadeKey: bi.key,
            message: `${bt.name}: maximum ${bt.maxRegimentsTotal.max} regiments per brigade (have ${regTotal})`,
          });
        }
        const regMin = bt.maxRegimentsTotal.min;
        if (regMin !== undefined && regTotal < regMin) {
          issues.push({
            level: "todo",
            brigadeKey: bi.key,
            message: `${bt.name}: needs at least ${regMin} regiment${regMin === 1 ? "" : "s"} per brigade (have ${regTotal})`,
          });
        }
      }
    }

    // ─── Army-wide: regiment slot armyMax (e.g. 1 Light Regiment per division) ─
    bt.slots.forEach((slot, si) => {
      if (!slot.regiment || slot.regiment.armyMax === undefined) return;
      const armyMax = slot.regiment.armyMax;
      // Count these regiments across all instances of THIS brigade type
      const armyRegCount = instances.reduce(
        (sum, bi) => sum + (bi.regimentSlots?.[si]?.length ?? 0), 0
      );
      if (armyRegCount > armyMax) {
        issues.push({
          level: "error",
          message: `${bt.name} → ${slot.regiment.label}: maximum ${armyMax} in the army (have ${armyRegCount})`,
        });
      }
    });

    bt.slots.forEach((slot, i) => {
      // ─── Regiment-based slot ───────────────────────────────────────────
      if (slot.regiment) {
        const regDef = slot.regiment;
        for (const bi of instances) {
          const regiments = bi.regimentSlots?.[i] ?? [];
          // Check regiment count
          if (regiments.length < regDef.min) {
            issues.push({
              level: "todo",
              shownOnSlot: true,
              brigadeKey: bi.key,
              message: `${bt.name} → ${slot.label}: needs at least ${regDef.min} ${regDef.label}${regDef.min > 1 ? "s" : ""} (have ${regiments.length})`,
            });
          }
          if (regiments.length > regDef.max) {
            issues.push({
              level: "error",
              brigadeKey: bi.key,
              message: `${bt.name} → ${slot.label}: maximum ${regDef.max} ${regDef.label}${regDef.max > 1 ? "s" : ""} allowed (have ${regiments.length})`,
            });
          }
          // Check each regiment's sub-slots
          regiments.forEach((reg, regIdx) => {
            regDef.slots.forEach((subSlot, subIdx) => {
              const lines = reg.slotLines[subIdx] ?? [];
              const total = lines.reduce((s, l) => s + l.qty, 0);
              if (total < subSlot.min) {
                issues.push({
                  level: "todo",
                  shownOnSlot: true,
                  brigadeKey: bi.key,
                  message: `${bt.name} → ${regDef.label} #${regIdx + 1} → ${subSlot.label}: needs at least ${subSlot.min} (have ${total})`,
                });
              }
              if (total > subSlot.max) {
                issues.push({
                  level: "error",
                  brigadeKey: bi.key,
                  message: `${bt.name} → ${regDef.label} #${regIdx + 1} → ${subSlot.label}: maximum ${subSlot.max} allowed (have ${total})`,
                });
              }
              // Single-unit-type constraint within the sub-slot (no mixing)
              if (subSlot.singleUnitType) {
                const distinct = new Set(lines.filter((l) => l.qty > 0).map((l) => l.unitId));
                if (distinct.size > 1) {
                  const names = [...distinct].map(
                    (id) => nation.units.find((u) => u.id === id)?.name ?? id
                  );
                  issues.push({
                    level: "error",
                    brigadeKey: bi.key,
                    message: `${bt.name} → ${regDef.label} #${regIdx + 1} → ${subSlot.label}: cannot mix types (have ${names.join(", ")})`,
                  });
                }
              }
              // Per-unit caps within the sub-slot
              for (const limit of subSlot.unitLimits ?? []) {
                const uTotal = lines.filter((l) => l.unitId === limit.unitId).reduce((s, l) => s + l.qty, 0);
                if (uTotal > limit.max) {
                  const uName = nation.units.find((u) => u.id === limit.unitId)?.name ?? limit.unitId;
                  issues.push({
                    level: "error",
                    brigadeKey: bi.key,
                    message: `${bt.name} → ${regDef.label} #${regIdx + 1} → ${subSlot.label}: maximum ${limit.max} ${uName} (have ${uTotal})`,
                  });
                }
              }
            });
          });
        }
        return; // skip flat-slot logic for this slot
      }

      // ─── Flat slot ─────────────────────────────────────────────────────
      const slotMax = slot.maxPerPoints
        ? Math.floor(armyTotalPoints / slot.maxPerPoints.perPoints)
        : slot.max;
      for (const bi of instances) {
        const lines = bi.slotLines[i] ?? [];
        const total = lines.reduce((s, l) => s + l.qty, 0);
        if (total < slot.min) {
          issues.push({
            level: "todo",
            shownOnSlot: true,
            brigadeKey: bi.key,
            message: `${bt.name} → ${slot.label}: needs at least ${slot.min} (have ${total})`,
          });
        }
        if (total > slotMax) {
          const reason = slot.maxPerPoints ? ` (1 per ${slot.maxPerPoints.perPoints} pts, army is ${armyTotalPoints} pts)` : "";
          issues.push({
            level: "error",
            brigadeKey: bi.key,
            message: `${bt.name} → ${slot.label}: maximum ${slotMax} allowed${reason} (have ${total})`,
          });
        }
        // Check single-unit-type constraint (e.g. cannot mix Cuirassier and Dragoon)
        if (slot.singleUnitType) {
          const distinctUnitIds = new Set(lines.filter((l) => l.qty > 0).map((l) => l.unitId));
          if (distinctUnitIds.size > 1) {
            const names = [...distinctUnitIds].map(
              (id) => nation.units.find((u) => u.id === id)?.name ?? id
            );
            issues.push({
              level: "error",
              brigadeKey: bi.key,
              message: `${bt.name} → ${slot.label}: cannot mix types (have ${names.join(", ")})`,
            });
          }
        }
        // Check mutually exclusive unit groups: at most `maxGroups` (default 1) may be present
        if (slot.mutuallyExclusiveGroups) {
          const maxGroups =
            slot.mutuallyExclusiveGroups.find((g) => g.maxGroups != null)?.maxGroups ?? 1;
          const presentGroups = slot.mutuallyExclusiveGroups.filter((g) =>
            lines.some((l) => l.qty > 0 && g.unitIds.includes(l.unitId))
          );
          if (presentGroups.length > maxGroups) {
            const labels = presentGroups.map((g, idx) =>
              g.label ?? g.unitIds.map((id) => nation.units.find((u) => u.id === id)?.name ?? id).join("/") ?? `group ${idx + 1}`
            );
            const choose =
              maxGroups === 1 ? "choose one option" : `choose at most ${maxGroups} options`;
            issues.push({
              level: "error",
              brigadeKey: bi.key,
              message: `${bt.name} → ${slot.label}: too many options selected (${labels.join(", ")}) — ${choose}`,
            });
          }
        }
        // Check per-brigade-instance unit limits (e.g. up to 2 Dragoon per this brigade)
        for (const limit of slot.unitLimits ?? []) {
          const unitTotal = lines
            .filter((l) => l.unitId === limit.unitId)
            .reduce((s, l) => s + l.qty, 0);
          if (unitTotal > limit.max) {
            const unitName = nation.units.find((u) => u.id === limit.unitId)?.name ?? limit.unitId;
            issues.push({
              level: "error",
              brigadeKey: bi.key,
              message: `${bt.name} → ${slot.label}: maximum ${limit.max} ${unitName} per brigade (have ${unitTotal})`,
            });
          }
        }
        // Check combined group limits (e.g. up to 1 Cossack OR Uhlan combined)
        for (const grp of slot.unitGroupLimits ?? []) {
          const grpTotal = lines
            .filter((l) => grp.unitIds.includes(l.unitId))
            .reduce((s, l) => s + l.qty, 0);
          if (grpTotal > grp.max) {
            const label = grp.label ??
              grp.unitIds.map((id) => nation.units.find((u) => u.id === id)?.name ?? id).join(" / ");
            issues.push({
              level: "error",
              brigadeKey: bi.key,
              message: `${bt.name} → ${slot.label}: maximum ${grp.max} ${label} combined per brigade (have ${grpTotal})`,
            });
          }
        }
        // Check dynamic per-unit limits (regimental artillery ratios)
        for (const dyn of slot.dynamicUnitLimits ?? []) {
          const uTotal = lines.filter((l) => l.unitId === dyn.unitId).reduce((s, l) => s + l.qty, 0);
          if (uTotal === 0) continue;
          const uName = nation.units.find((u) => u.id === dyn.unitId)?.name ?? dyn.unitId;

          if (dyn.perBattalions) {
            const battalions = dyn.perBattalions.countSlotIndices.reduce(
              (sum, idx) => sum + slotUnitCount(bi, idx), 0
            );
            const allowed = Math.floor(battalions / dyn.perBattalions.ratio);
            if (uTotal > allowed) {
              issues.push({
                level: "error",
                brigadeKey: bi.key,
                message: `${bt.name} → ${slot.label}: maximum ${allowed} ${uName} (1 per ${dyn.perBattalions.ratio} battalions; ${battalions} in brigade, have ${uTotal})`,
              });
            }
          }

          if (dyn.perQualifyingRegiment) {
            const { regimentSlotIndices, minBattalions } = dyn.perQualifyingRegiment;
            let qualifying = 0;
            for (const idx of regimentSlotIndices) {
              const regs = bi.regimentSlots?.[idx] ?? [];
              for (const reg of regs) {
                const bnCount = reg.slotLines.reduce((s, ls) => s + ls.reduce((a, l) => a + l.qty, 0), 0);
                if (bnCount >= minBattalions) qualifying += 1;
              }
            }
            if (uTotal > qualifying) {
              issues.push({
                level: "error",
                brigadeKey: bi.key,
                message: `${bt.name} → ${slot.label}: maximum ${qualifying} ${uName} (1 per regiment${minBattalions > 1 ? ` of ${minBattalions}+ battalions` : ""}, have ${uTotal})`,
              });
            }
          }
        }
        // Check brigade-level unit count prerequisite (e.g. "artillery only if 6+ battalions in this brigade")
        if (total > 0 && !brigadeCountRequirementMet(slot, bi)) {
          const needed = slot.requiresBrigadeCount!.min;
          const have = countUnitsInInstance(bi, slot.requiresBrigadeCount!.unitIds);
          issues.push({
            level: "error",
            brigadeKey: bi.key,
            message: `${bt.name} → ${slot.label}: requires ${needed} qualifying units in this brigade first (have ${have})`,
          });
        }
        // Check army-wide unit count prerequisite (e.g. "requires 8+ infantry battalions in the army")
        if (total > 0 && !armyUnitCountRequirementMet(slot, roster.brigadeInstances)) {
          const needed = slot.requiresArmyUnitCount!.min;
          const have = countUnitsInArmy(roster.brigadeInstances, slot.requiresArmyUnitCount!.unitIds);
          issues.push({
            level: "error",
            brigadeKey: bi.key,
            message: `${bt.name} → ${slot.label}: requires ${needed} qualifying units in the army (have ${have})`,
          });
        }
      }

      for (const cap of slot.unitCaps ?? []) {
        const total = instances.reduce((sum, bi) => {
          const lines = bi.slotLines[i] ?? [];
          return sum + lines.filter((l) => l.unitId === cap.unitId).reduce((s, l) => s + l.qty, 0);
        }, 0);
        if (total === 0) continue;

        const unitName = nation.units.find((u) => u.id === cap.unitId)?.name ?? cap.unitId;

        // Check prerequisite brigade threshold
        if (!unitCapRequirementMet(cap, roster.brigadeInstances)) {
          const { brigadeTypeIds, min } = cap.requiresBrigades!;
          const names = brigadeTypeIds.map((id) => nation.brigades.find((b) => b.id === id)?.name ?? id).join(" or ");
          issues.push({
            level: "error",
            message: `${unitName}: needs ${min === 1 ? `a ${names}` : `${min} × ${names}`} in the army`,
          });
          continue;
        }

        // Check effective max (may be ratio-scaled)
        const max = effectiveUnitCapMax(cap, roster.brigadeInstances);
        if (total > max) {
          const reason = cap.maxRatio
            ? ` — scaled by brigades taken (1 per ${cap.maxRatio.ratio})`
            : "";
          issues.push({
            level: "error",
            message: `${unitName}: maximum ${max} in the army across all ${bt.name} brigades (have ${total})${reason}`,
          });
        }
      }
    });
  }

  // ─── Upgrades and downgrades: limits, and ones that can't be combined ──────
  const armyWideReported = new Set<string>();
  const armyMaxReported = new Set<string>();
  const sharedReported = new Set<string>();
  for (const bi of roster.brigadeInstances) {
    const bt = nation.brigades.find((b) => b.id === bi.brigadeTypeId);
    if (!bt?.options?.length) continue;

    for (const o of bt.options) {
      // An army-wide limit is reported once, for the army, not on every brigade
      if (o.limit?.armyWide) {
        if (armyWideReported.has(o.id)) continue;
        armyWideReported.add(o.id);
      }
      const taken = optionTaken(o, bi, roster.brigadeInstances);
      const allowed = optionAllowance(o, bi, roster.brigadeInstances);
      // Options sharing a limit (Highlanders, with or without Ferocious Charge) report it once
      const shared = [o.id, ...(o.limit?.sharedWith ?? [])].sort().join("+");
      const sharedKey = `${o.limit?.armyWide ? "army" : bi.key}:${shared}`;
      if (taken > allowed && !sharedReported.has(sharedKey)) {
        sharedReported.add(sharedKey);
        const noun =
          o.scope === "regiment" ? (taken === 1 ? "regiment" : "regiments") : unitNoun(nation, o.appliesTo, taken);
        const limit = o.scope === "regiment" ? null : limitText(nation, o);
        issues.push({
          level: "error",
          brigadeKey: o.limit?.armyWide ? undefined : bi.key,
          message: `${o.limit?.armyWide ? "Army" : bt.name}: ${o.label} on ${taken} ${noun}, only ${allowed} allowed${limit ? ` (${limit})` : ""}`,
        });
      }
      // A cap across the army on top of the brigade's own limit, reported once
      if (o.limit?.armyMax !== undefined && !armyMaxReported.has(o.id)) {
        armyMaxReported.add(o.id);
        const inArmy = optionTakenInArmy(o, roster.brigadeInstances);
        if (inArmy > o.limit.armyMax) {
          issues.push({
            level: "error",
            message: `Army: ${o.label} on ${inArmy} ${unitNoun(nation, o.appliesTo, inArmy)}, only ${o.limit.armyMax} allowed in the army`,
          });
        }
      }
    }

    for (const { line, regiment } of brigadeUnitLines(bi)) {
      const mine = (bt.options ?? []).filter((o) => line.options?.includes(o.id) || regiment?.options?.includes(o.id));
      const unitName = nation.units.find((u) => u.id === line.unitId)?.name ?? line.unitId;
      const clashes = new Set<string>();
      for (const a of mine) {
        for (const b of mine) {
          if (a === b) continue;
          const sameGroup = !!a.group && a.group === b.group && a.scope !== "regiment" && b.scope !== "regiment";
          if (sameGroup || a.excludes?.includes(b.id)) clashes.add([a.label, b.label].sort().join(" and "));
        }
      }
      for (const pair of clashes) {
        issues.push({
          level: "error",
          brigadeKey: bi.key,
          message: `${bt.name}: a ${unitName} can't be both ${pair}`,
        });
      }
    }
  }

  // ─── Batteries per brigade, counting army batteries attached to it ─────────
  const attach = attachRule(nation);
  if (attach) {
    for (const bi of attachTargets(nation, roster.brigadeInstances)) {
      const count = batteriesIn(nation, roster.brigadeInstances, bi.key);
      if (attach.maxPerBrigade !== undefined && count > attach.maxPerBrigade) {
        const bt = nation.brigades.find((b) => b.id === bi.brigadeTypeId);
        issues.push({
          level: "error",
          brigadeKey: bi.key,
          message: `${bt?.name ?? "Brigade"}: ${count} batteries, attached ones included; a brigade can have no more than ${attach.maxPerBrigade}`,
        });
      }
    }
  }

  // ─── Brigade types that can't be taken together (Prussia 1815: Cavalry or Landwehr Cavalry) ──
  for (const bt of nation.brigades) {
    if (!bt.excludesBrigadeTypes || !roster.brigadeInstances.some((bi) => bi.brigadeTypeId === bt.id)) continue;
    const clash = nation.brigades.find(
      (other) => bt.excludesBrigadeTypes!.includes(other.id) && roster.brigadeInstances.some((bi) => bi.brigadeTypeId === other.id)
    );
    // Reported once for the pair
    if (clash && bt.id < clash.id) {
      issues.push({ level: "error", message: `${bt.name} and ${clash.name} can't be taken together; choose one or the other` });
    }
  }

  // ─── Regiment balance across the army (Austria: no more Hungarian than German) ──
  for (const rule of nation.regimentBalance ?? []) {
    const more = regimentsHolding(roster.brigadeInstances, rule.atMost);
    const fewer = regimentsHolding(roster.brigadeInstances, rule.atLeastAs);
    if (more > fewer) issues.push({ level: "error", message: `${rule.label} (have ${more} against ${fewer})` });
  }

  // ─── Per brigade: one kind can't outnumber another, choices, battery capacity, slot and regiment caps ──
  for (const bi of roster.brigadeInstances) {
    const bt = nation.brigades.find((b) => b.id === bi.brigadeTypeId);
    if (!bt) continue;
    if (bt.atLeastAsMany) {
      const have = countUnitsInInstance(bi, bt.atLeastAsMany.unitIds);
      const against = countUnitsInInstance(bi, bt.atLeastAsMany.asUnitIds);
      if (against > have) {
        issues.push({ level: "error", brigadeKey: bi.key, message: `${bt.name}: ${bt.atLeastAsMany.label} (have ${have} against ${against})` });
      }
    }
    if (bt.maxChoices) {
      const taken = choicesTaken(bt, bi);
      if (taken > bt.maxChoices.max) {
        issues.push({ level: "error", brigadeKey: bi.key, message: `${bt.name}: ${bt.maxChoices.label} (have ${taken})` });
      }
    }
    if (bt.maxBatteries !== undefined) {
      const count = batteriesIn(nation, roster.brigadeInstances, bi.key);
      if (count > bt.maxBatteries) {
        issues.push({ level: "error", brigadeKey: bi.key, message: `${bt.name}: ${count} batteries, attached ones included; it can have no more than ${bt.maxBatteries}` });
      }
    }
  }
  for (const bt of nation.brigades) {
    const instances = roster.brigadeInstances.filter((bi) => bi.brigadeTypeId === bt.id);
    if (instances.length === 0) continue;
    bt.slots.forEach((slot, i) => {
      for (const cap of slot.unitGroupCaps ?? []) {
        const have = instances.reduce((s, bi) => s + (bi.slotLines[i] ?? []).filter((l) => cap.unitIds.includes(l.unitId)).reduce((t, l) => t + l.qty, 0), 0);
        if (have > cap.armyMax) issues.push({ level: "error", message: `${bt.name}: maximum ${cap.armyMax} ${cap.label} in the army (have ${have})` });
      }
      const above = slot.regiment?.limitBrigadesAbove;
      if (above) {
        const brigades = instances.filter((bi) => (bi.regimentSlots?.[i]?.length ?? 0) > above.count).length;
        if (brigades > above.maxBrigades) {
          issues.push({
            level: "error",
            message: `${bt.name}: only ${above.maxBrigades} brigade${above.maxBrigades === 1 ? "" : "s"} may take more than ${above.count} ${slot.regiment!.label}${above.count === 1 ? "" : "s"} (have ${brigades})`,
          });
        }
      }
    });
  }

  // ─── Brigade commanders' Staff Ratings (e.g. half of Russia's must be 7) ──
  const ratingRule = nation.brigadeCommanderRating;
  if (ratingRule) {
    const ratings = roster.brigadeInstances.flatMap((bi) => {
      const line = bi.commanderLine;
      const unit = line && nation.units.find((u) => u.id === line.unitId);
      const rating = unit?.staffRating ?? unit?.variants?.find((v) => v.label === line?.variantLabel)?.staffRating;
      return rating === undefined ? [] : [rating];
    });
    const above = ratings.filter((r) => r > ratingRule.maxRating).length;
    const allowed = Math.floor(ratings.length * ratingRule.maxShareAbove);
    if (above > allowed) {
      issues.push({
        level: "error",
        message: `${ratingRule.label}: ${above} of ${ratings.length} brigade commanders are rated above ${ratingRule.maxRating}, only ${allowed} may be`,
      });
    }
  }

  // ─── Army-wide points-percentage caps (e.g. Imperial Guard ≤ 25% of army) ──
  for (const cap of nation.pointsCaps ?? []) {
    if (armyTotalPoints === 0) continue;

    const cappedTotal = roster.brigadeInstances
      .filter((bi) => cap.brigadeTypeIds.includes(bi.brigadeTypeId))
      .reduce((sum, bi) => sum + brigadeTotal(nation, bi, freeLines(nation, roster)), 0);
    if (cappedTotal === 0) continue;

    const percent = (cappedTotal / armyTotalPoints) * 100;
    if (percent > cap.maxPercent) {
      const label = cap.label ?? "these brigades";
      issues.push({
        level: "error",
        message: `${label}: may not exceed ${cap.maxPercent}% of the army (currently ${Math.round(percent)}%, ${cappedTotal} of ${armyTotalPoints} pts)`,
      });
    }
  }

  // ─── Army-wide unit ratio caps (e.g. 1 Light battery per 6 battalions) ─────
  // ─── Units limited across the army, whichever brigade types they're in ───
  for (const cap of nation.armyUnitCaps ?? []) {
    const have = countUnitsInArmy(roster.brigadeInstances, cap.unitIds);
    if (have > cap.max) {
      issues.push({ level: "error", message: `Army: up to ${cap.max} ${cap.label} (have ${have})` });
    }
  }

  for (const cap of nation.unitRatioCaps ?? []) {
    const capCount = countUnitsInArmy(
      roster.brigadeInstances.filter((bi) => !cap.brigadeTypeIds || cap.brigadeTypeIds.includes(bi.brigadeTypeId)),
      cap.capUnitIds
    );
    if (capCount === 0) continue;
    const perCount = countUnitsInArmy(roster.brigadeInstances, cap.perUnitIds);
    const allowed = Math.floor(perCount / cap.ratio);
    if (capCount > allowed) {
      const label = cap.label ?? "these units";
      issues.push({
        level: "error",
        message: `${label}: maximum ${allowed} allowed (1 per ${cap.ratio}; have ${capCount}, based on ${perCount} qualifying units)`,
      });
    }
  }

  return issues;
}

/** "2nd Infantry Brigade" when the army has more than one of that type, otherwise just "Infantry Brigade" */
export function brigadeDisplayName(nation: Nation, roster: RosterState, brigadeKey: string): string {
  const bi = roster.brigadeInstances.find((b) => b.key === brigadeKey);
  const name = nation.brigades.find((b) => b.id === bi?.brigadeTypeId)?.name ?? "Brigade";
  if (!bi) return name;
  // A brigade the player has named goes by that name, with its type after it
  if (bi.name?.trim()) return `${bi.name.trim()} (${name})`;
  const sameType = roster.brigadeInstances.filter((b) => b.brigadeTypeId === bi.brigadeTypeId);
  if (sameType.length < 2) return name;
  const n = sameType.indexOf(bi) + 1;
  const suffix = n % 10 === 1 && n % 100 !== 11 ? "st" : n % 10 === 2 && n % 100 !== 12 ? "nd" : n % 10 === 3 && n % 100 !== 13 ? "rd" : "th";
  return `${n}${suffix} ${name}`;
}

/** "attached to 2nd Infantry Brigade", for a battery attached to a brigade still in the army */
export function attachedText(nation: Nation, roster: RosterState, attachedTo: string | undefined): string | null {
  if (!attachedTo || !roster.brigadeInstances.some((b) => b.key === attachedTo)) return null;
  return `attached to ${brigadeDisplayName(nation, roster, attachedTo)}`;
}

/** An issue's message without the brigade name in front, for showing on that brigade's own card */
export function brigadeIssueText(message: string, brigadeName: string): string {
  const text = message.startsWith(`${brigadeName}: `)
    ? message.slice(brigadeName.length + 2)
    : message.startsWith(`${brigadeName} → `)
      ? message.slice(brigadeName.length + 3)
      : message;
  return text.charAt(0).toUpperCase() + text.slice(1);
}

/** Asks the builder to open a brigade's card and scroll to it, e.g. from the roster's issue list */
export const REVEAL_BRIGADE_EVENT = "army-builder:reveal-brigade";

/** A brigade's own name if the player has given it one, otherwise its type, e.g. "Infantry Brigade" */
export function brigadeLabel(bi: { name?: string }, typeName: string): string {
  return bi.name?.trim() || typeName;
}

/**
 * What a list has from outside its campaign period, once one is chosen: a brigade, a slot's units, a unit
 * in a slot, an upgrade or a commander's Staff Rating from another period. Uses the period view of the
 * nation (`nationForPeriod`), which marks them.
 */
function periodIssues(nation: Nation, roster: RosterState): ValidationIssue[] {
  const period = nation.periods?.find((p) => p.id === roster.period);
  if (!period) return [];
  const notIn = `not in the ${period.label} period`;
  const issues: ValidationIssue[] = [];
  const variantIssue = (line: RosterUnitLine | null | undefined, where: string, brigadeKey?: string) => {
    if (!line) return;
    const variant = nation.units.find((u) => u.id === line.unitId)?.variants?.find((v) => v.label === line.variantLabel);
    if (variant?.periodBlocked) {
      issues.push({ level: "error", brigadeKey, message: `${where}: ${variant.label}, ${notIn}` });
    }
  };
  roster.commandItems.forEach((line) => variantIssue(line, "Army Command"));

  for (const bi of roster.brigadeInstances) {
    const bt = nation.brigades.find((b) => b.id === bi.brigadeTypeId);
    if (!bt) continue;
    if (bt.periodBlocked) {
      issues.push({ level: "error", brigadeKey: bi.key, message: `${bt.name}: ${notIn} (${bt.periodBlocked})` });
    }
    variantIssue(bi.commanderLine, bt.name, bi.key);
    bt.slots.forEach((slot, i) => {
      const lines = bi.slotLines[i] ?? [];
      if (slot.periodBlocked && lines.length) {
        issues.push({ level: "error", brigadeKey: bi.key, message: `${bt.name} → ${slot.label}: ${notIn} (${slot.periodBlocked})` });
        return;
      }
      for (const unitId of new Set(lines.map((l) => l.unitId))) {
        const why = unitPeriodBlocked(nation, slot, unitId, roster.period);
        const name = nation.units.find((u) => u.id === unitId)?.name ?? unitId;
        if (why) issues.push({ level: "error", brigadeKey: bi.key, message: `${bt.name}: ${name}, ${notIn} (${why})` });
      }
    });
    const taken = new Set(
      brigadeUnitLines(bi).flatMap(({ line, regiment }) => [...(line.options ?? []), ...(regiment?.options ?? [])])
    );
    for (const o of bt.options ?? []) {
      if (o.periodBlocked && taken.has(o.id)) {
        issues.push({ level: "error", brigadeKey: bi.key, message: `${bt.name}: ${o.label}, ${notIn}` });
      }
    }
  }
  return issues;
}
