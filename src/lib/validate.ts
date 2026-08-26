import type { Nation } from "@/data/types";
import type { RosterState } from "@/types/army";
import { countByType, effectiveMax, requirementMet, requirementLabel } from "@/lib/brigadeLimits";

export interface ValidationIssue {
  level: "error";
  message: string;
}

export function validateRoster(nation: Nation, roster: RosterState): ValidationIssue[] {
  const issues: ValidationIssue[] = [];

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
      }

      for (const cap of slot.unitCaps ?? []) {
        const total = instances.reduce((sum, bi) => {
          const lines = bi.slotLines[i] ?? [];
          return sum + lines.filter((l) => l.unitId === cap.unitId).reduce((s, l) => s + l.qty, 0);
        }, 0);
        if (total > cap.armyMax) {
          const unitName = nation.units.find((u) => u.id === cap.unitId)?.name ?? cap.unitId;
          issues.push({
            level: "error",
            message: `${unitName}: maximum ${cap.armyMax} in the army across all ${bt.name} brigades (have ${total})`,
          });
        }
      }
    });
  }

  return issues;
}
