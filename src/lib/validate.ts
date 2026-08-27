import type { Nation } from "@/data/types";
import type { RosterState } from "@/types/army";
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
      for (const bi of instances) {
        const lines = bi.slotLines[i] ?? [];
        const total = lines.reduce((s, l) => s + l.qty, 0);
        if (total < slot.min) {
          issues.push({
            level: "error",
            message: `${bt.name} → ${slot.label}: needs at least ${slot.min} (have ${total})`,
          });
        }
        if (total > slot.max) {
          issues.push({
            level: "error",
            message: `${bt.name} → ${slot.label}: maximum ${slot.max} allowed (have ${total})`,
          });
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

  return issues;
}
