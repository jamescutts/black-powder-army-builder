import type { Nation } from "@/data/types";
import type { RosterBrigadeInstance, RosterState } from "@/types/army";
import { unitCost } from "@/lib/units";
import {
  countByType,
  effectiveMax,
  requirementMet,
  requirementLabel,
  unitCapRequirementMet,
  effectiveUnitCapMax,
  slotFillRequirementMet,
  slotUnitCount,
  armyUnitCountRequirementMet,
  countUnitsInArmy,
} from "@/lib/brigadeLimits";

/** Total points for a single brigade instance (commander + flat slots + regiment sub-slots). */
function brigadeInstancePoints(nation: Nation, bi: RosterBrigadeInstance): number {
  const unitLinePoints = (unitId: string, variantLabel: string | undefined, qty: number) => {
    const unit = nation.units.find((u) => u.id === unitId);
    return unit ? unitCost(unit, variantLabel) * qty : 0;
  };
  let total = 0;
  if (bi.commanderLine) {
    total += unitLinePoints(bi.commanderLine.unitId, bi.commanderLine.variantLabel, bi.commanderLine.qty);
  }
  for (const lines of bi.slotLines) {
    for (const l of lines) total += unitLinePoints(l.unitId, l.variantLabel, l.qty);
  }
  for (const regSlot of bi.regimentSlots ?? []) {
    if (!regSlot) continue;
    for (const reg of regSlot) {
      for (const lines of reg.slotLines) {
        for (const l of lines) total += unitLinePoints(l.unitId, l.variantLabel, l.qty);
      }
    }
  }
  return total;
}

export interface ValidationIssue {
  level: "error";
  message: string;
}

export function validateRoster(nation: Nation, roster: RosterState): ValidationIssue[] {
  const issues: ValidationIssue[] = [];

  // Determine which Command units are army-level (not tied to a brigade as its required commander)
  const brigadeCommanderIds = new Set(
    nation.brigades.map((b) => b.commanderUnitId).filter((id): id is string => Boolean(id))
  );
  const hasArmyCommandUnits = nation.units.some(
    (u) => u.category === "Command" && !brigadeCommanderIds.has(u.id)
  );

  const commandTotal = roster.commandItems.reduce((s, l) => s + l.qty, 0);
  if (hasArmyCommandUnits && commandTotal === 0) {
    issues.push({
      level: "error",
      message: "Army Command: an army commander is required",
    });
  }
  if (commandTotal > 1) {
    issues.push({
      level: "error",
      message: `Army Command: only one army commander allowed (have ${commandTotal})`,
    });
  }

  // Army total points (used for per-points caps like Earthworks "1 per 500 points")
  const armyTotalPoints =
    roster.commandItems.reduce((sum, l) => {
      const unit = nation.units.find((u) => u.id === l.unitId);
      return sum + (unit ? unitCost(unit, l.variantLabel) * l.qty : 0);
    }, 0) +
    roster.brigadeInstances.reduce((sum, bi) => sum + brigadeInstancePoints(nation, bi), 0);

  for (const bt of nation.brigades) {
    const count = countByType(roster.brigadeInstances, bt.id);
    if (count < bt.min) {
      issues.push({
        level: "error",
        message: `${bt.name}: needs at least ${bt.min} (have ${count})`,
      });
    }
    const max = effectiveMax(bt, roster.brigadeInstances);
    if (count > max) {
      issues.push({
        level: "error",
        message: `${bt.name}: maximum ${max} allowed right now (have ${count})${
          bt.maxRatio ? ` — capped by ${bt.maxRatio.brigadeTypeIds.join("/")} taken` : ""
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
          level: "error",
          message: `${bt.name}: ${missing} brigade${missing === 1 ? "" : "s"} missing a Brigade Commander`,
        });
      }
    }

    bt.slots.forEach((slot, i) => {
      // ─── Regiment-based slot ───────────────────────────────────────────
      if (slot.regiment) {
        const regDef = slot.regiment;
        for (const bi of instances) {
          const regiments = bi.regimentSlots?.[i] ?? [];
          // Check regiment count
          if (regiments.length < regDef.min) {
            issues.push({
              level: "error",
              message: `${bt.name} → ${slot.label}: needs at least ${regDef.min} ${regDef.label}${regDef.min > 1 ? "s" : ""} (have ${regiments.length})`,
            });
          }
          if (regiments.length > regDef.max) {
            issues.push({
              level: "error",
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
                  level: "error",
                  message: `${bt.name} → ${regDef.label} #${regIdx + 1} → ${subSlot.label}: needs at least ${subSlot.min} (have ${total})`,
                });
              }
              if (total > subSlot.max) {
                issues.push({
                  level: "error",
                  message: `${bt.name} → ${regDef.label} #${regIdx + 1} → ${subSlot.label}: maximum ${subSlot.max} allowed (have ${total})`,
                });
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
            level: "error",
            message: `${bt.name} → ${slot.label}: needs at least ${slot.min} (have ${total})`,
          });
        }
        if (total > slotMax) {
          const reason = slot.maxPerPoints ? ` (1 per ${slot.maxPerPoints.perPoints} pts, army is ${armyTotalPoints} pts)` : "";
          issues.push({
            level: "error",
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
              message: `${bt.name} → ${slot.label}: cannot mix types (have ${names.join(", ")})`,
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
              message: `${bt.name} → ${slot.label}: maximum ${grp.max} ${label} combined per brigade (have ${grpTotal})`,
            });
          }
        }
        // Check slot-level prerequisite (e.g. "artillery only if 6+ battalions in this brigade")
        if (total > 0 && !slotFillRequirementMet(slot, bi)) {
          const needed = slot.requiresSlotFill!.min;
          const have = slot.requiresSlotFill!.slotIndices.reduce(
            (sum, idx) => sum + slotUnitCount(bi, idx), 0
          );
          issues.push({
            level: "error",
            message: `${bt.name} → ${slot.label}: requires ${needed} units in this brigade first (have ${have})`,
          });
        }
        // Check army-wide unit count prerequisite (e.g. "requires 8+ infantry battalions in the army")
        if (total > 0 && !armyUnitCountRequirementMet(slot, roster.brigadeInstances)) {
          const needed = slot.requiresArmyUnitCount!.min;
          const have = countUnitsInArmy(roster.brigadeInstances, slot.requiresArmyUnitCount!.unitIds);
          issues.push({
            level: "error",
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
          const reqMin = cap.requiresBrigades!.min;
          issues.push({
            level: "error",
            message: `${unitName}: requires ${reqMin} brigades taken before it can be fielded (have ${total})`,
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

  // ─── Army-wide points-percentage caps (e.g. Imperial Guard ≤ 25% of army) ──
  for (const cap of nation.pointsCaps ?? []) {
    if (armyTotalPoints === 0) continue;

    const cappedTotal = roster.brigadeInstances
      .filter((bi) => cap.brigadeTypeIds.includes(bi.brigadeTypeId))
      .reduce((sum, bi) => sum + brigadeInstancePoints(nation, bi), 0);
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
  for (const cap of nation.unitRatioCaps ?? []) {
    const capCount = countUnitsInArmy(roster.brigadeInstances, cap.capUnitIds);
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
