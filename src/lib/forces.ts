import type { BrigadeType, ForceUnit, HistoricalForce, Nation } from "@/data/types";
import type { RosterBrigadeInstance, RosterRegimentInstance, RosterState, RosterUnitLine } from "@/types/army";
import { defaultVariantLabel } from "@/lib/units";

/**
 * A historical force as a list: its brigades and units placed in their slots, named as they fought.
 * Keys are made from the force's id and each brigade's place in it, so the same force always builds
 * the same keys, and a list started from it can be compared with it (see `validateRoster`).
 * `problems` says what couldn't be placed, for `npm run check:forces`; the builder just leaves it out.
 */
export function rosterFromForce(nation: Nation, force: HistoricalForce): { roster: RosterState; problems: string[] } {
  const problems: string[] = [];
  const unitById = new Map(nation.units.map((u) => [u.id, u]));

  const line = (fu: ForceUnit, key: string, where: string): RosterUnitLine | null => {
    const unit = unitById.get(fu.unit);
    if (!unit) {
      problems.push(`${where}: no unit "${fu.unit}" in ${nation.name}`);
      return null;
    }
    let variantLabel = defaultVariantLabel(unit);
    if (fu.variant) {
      if (unit.variants?.some((v) => v.label === fu.variant)) variantLabel = fu.variant;
      else problems.push(`${where}: ${unit.name} has no choice "${fu.variant}"`);
    }
    return {
      key,
      unitId: unit.id,
      variantLabel,
      qty: 1,
      options: fu.options?.length ? [...fu.options] : undefined,
      name: fu.name,
    };
  };

  const brigadeInstances = force.brigades.flatMap((fb, bIdx): RosterBrigadeInstance[] => {
    const where = fb.name ?? `Brigade ${bIdx + 1}`;
    const bt: BrigadeType | undefined = nation.brigades.find((b) => b.id === fb.type);
    if (!bt) {
      problems.push(`${where}: no brigade type "${fb.type}" in ${nation.name}`);
      return [];
    }
    const key = `${force.id}-b${bIdx}`;
    const commanderUnit = bt.commanderUnitId ? unitById.get(bt.commanderUnitId) : undefined;
    const commanderLine = commanderUnit
      ? line({ unit: commanderUnit.id, variant: fb.commander?.variant, name: fb.commander?.name }, `${key}-cmd`, where)
      : null;

    const slotLines: RosterUnitLine[][] = bt.slots.map(() => []);
    (fb.units ?? []).forEach((fu, uIdx) => {
      const takes = bt.slots
        .map((s, i) => ({ s, i }))
        .filter(({ s, i }) => !s.regiment && (fu.slot === undefined ? s.unitIds.includes(fu.unit) : i === fu.slot));
      const target = takes.find(({ s, i }) => slotLines[i].length < s.max) ?? takes[0];
      if (!target) {
        problems.push(`${where}: no slot in ${bt.name} takes "${fu.unit}"`);
        return;
      }
      const l = line(fu, `${key}-u${uIdx}`, where);
      if (l) slotLines[target.i].push(l);
    });

    const regimentSlots: (RosterRegimentInstance[] | null)[] = bt.slots.map((s) => (s.regiment ? [] : null));
    (fb.regiments ?? []).forEach((fr, rIdx) => {
      const fits = bt.slots
        .map((s, i) => ({ s, i }))
        .filter(({ s, i }) =>
          s.regiment &&
          (fr.slot === undefined ? fr.units.every((u) => s.regiment!.slots.some((sub) => sub.unitIds.includes(u.unit))) : i === fr.slot)
        );
      const target = fits.find(({ s, i }) => regimentSlots[i]!.length < s.regiment!.max) ?? fits[0];
      if (!target) {
        problems.push(`${where}: no regiment slot in ${bt.name} takes ${fr.name ?? `regiment ${rIdx + 1}`}`);
        return;
      }
      const subs = target.s.regiment!.slots;
      const reg: RosterRegimentInstance = {
        key: `${key}-r${rIdx}`,
        name: fr.name,
        options: fr.options?.length ? [...fr.options] : undefined,
        slotLines: subs.map(() => []),
      };
      fr.units.forEach((fu, uIdx) => {
        const takes = subs.map((s, i) => ({ s, i })).filter(({ s, i }) => (fu.slot === undefined ? s.unitIds.includes(fu.unit) : i === fu.slot));
        const sub = takes.find(({ s, i }) => reg.slotLines[i].length < s.max) ?? takes[0];
        if (!sub) {
          problems.push(`${where}: no place in ${target.s.regiment!.label} for "${fu.unit}"`);
          return;
        }
        const l = line(fu, `${reg.key}-u${uIdx}`, where);
        if (l) reg.slotLines[sub.i].push(l);
      });
      regimentSlots[target.i]!.push(reg);
    });

    return [{ key, brigadeTypeId: bt.id, name: fb.name, commanderLine, slotLines, regimentSlots }];
  });

  const commandItems = (force.command ?? []).flatMap((fu, i) => {
    const l = line(fu, `${force.id}-c${i}`, "Army command");
    return l ? [l] : [];
  });

  if (force.period && !nation.periods?.some((p) => p.id === force.period)) {
    problems.push(`${nation.name} has no period "${force.period}"`);
  }

  return {
    roster: {
      nationId: nation.id,
      armyName: force.name,
      period: force.period,
      sourceForceId: force.id,
      commandItems,
      brigadeInstances,
    },
    problems,
  };
}

/** Where a historical force is opened from: the army's page, which starts a new list from it */
export function forceHref(supplementId: string, force: HistoricalForce): string {
  return `/black-powder/${supplementId}/${force.nationId}?force=${encodeURIComponent(force.id)}`;
}
