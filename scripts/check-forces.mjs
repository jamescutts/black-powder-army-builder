// Builds every historical force (src/data/battles) and checks it against its army list: every unit,
// option and Staff Rating must exist and find a slot, and whatever the force breaks of the list's
// rules (or lacks of them) is printed as its historical departures, which its notes should explain.
// Fails on a force that doesn't build, lacks a commander, or departs from the rules with no notes.
//
//   npm run check:forces
//
// Runs the app's own TypeScript with Node's type stripping, resolving the "@/" alias and JSON imports.
import { registerHooks } from "node:module";
import { existsSync, readFileSync } from "node:fs";
import { fileURLToPath, pathToFileURL } from "node:url";
import path from "node:path";

const src = path.resolve(path.dirname(fileURLToPath(import.meta.url)), "../src");

registerHooks({
  resolve(specifier, context, next) {
    let target = specifier.startsWith("@/") ? path.join(src, specifier.slice(2)) : null;
    if (!target && specifier.startsWith(".") && context.parentURL?.startsWith("file:")) {
      target = path.resolve(path.dirname(fileURLToPath(context.parentURL)), specifier);
    }
    if (target) {
      for (const candidate of [target, `${target}.ts`, path.join(target, "index.ts")]) {
        if (existsSync(candidate) && !candidate.endsWith(path.sep) && path.extname(candidate)) {
          return { url: pathToFileURL(candidate).href, shortCircuit: true };
        }
      }
    }
    return next(specifier, context);
  },
  load(url, context, next) {
    if (url.endsWith(".json")) {
      return { format: "module", source: `export default ${readFileSync(fileURLToPath(url), "utf8")};`, shortCircuit: true };
    }
    return next(url, context);
  },
});

const { battles } = await import("@/data/battles");
const { getNation } = await import("@/data");
const { rosterFromForce } = await import("@/lib/forces");
const { validateRoster } = await import("@/lib/validate");
const { rosterTotal, unitCount } = await import("@/lib/points");
const { nationForPeriod } = await import("@/lib/periods");

let failed = 0;
const ids = new Set();
for (const battle of battles) {
  console.log(`\n${battle.name} (${battle.date})`);
  for (const force of battle.forces) {
    const problems = [];
    if (ids.has(force.id)) problems.push(`another force is also "${force.id}"`);
    ids.add(force.id);
    const base = getNation(force.nationId);
    if (!base) {
      console.log(`  ✗ ${force.name}: no army list "${force.nationId}"`);
      failed++;
      continue;
    }
    const nation = nationForPeriod(base, force.period);
    const built = rosterFromForce(nation, force);
    problems.push(...built.problems);
    // Options the brigade doesn't have, or that don't apply to the unit
    for (const bi of built.roster.brigadeInstances) {
      const bt = nation.brigades.find((b) => b.id === bi.brigadeTypeId);
      const lines = [...bi.slotLines.flat(), ...bi.regimentSlots.flatMap((r) => r ?? []).flatMap((r) => r.slotLines.flat())];
      for (const l of lines) {
        for (const o of l.options ?? []) {
          const opt = bt?.options?.find((x) => x.id === o);
          if (!opt) problems.push(`${bi.name}: ${bt?.name} has no option "${o}"`);
          else if (!opt.appliesTo.includes(l.unitId)) problems.push(`${bi.name}: "${o}" doesn't apply to ${l.unitId}`);
        }
      }
    }
    // As a plain list, what the force breaks of the rules or lacks (a cavalry division has no infantry
    // brigade): its historical departures. A force missing its commander is unfinished, not history.
    const raw = validateRoster(nation, { ...built.roster, sourceForceId: undefined });
    for (const t of raw.filter((i) => /commander/i.test(i.message))) problems.push(`unfinished: ${t.message}`);
    const departures = raw.filter((i) => !/commander/i.test(i.message));
    if (departures.length > 0 && !force.notes?.length) problems.push("breaks the list's rules but has no notes saying why");
    // Started from the force, every one of those should read as the history, not a mistake
    const marked = validateRoster(nation, built.roster).filter((i) => i.level !== "historical");
    for (const m of marked) problems.push(`not recognised as historical: ${m.message}`);

    const ok = problems.length === 0;
    if (!ok) failed++;
    console.log(
      `  ${ok ? "✓" : "✗"} ${force.name} · ${nation.name} · ${rosterTotal(nation, built.roster)} pts, ${unitCount(built.roster)} units, ${built.roster.brigadeInstances.length} brigades`
    );
    for (const p of problems) console.log(`      problem: ${p}`);
    for (const d of departures) console.log(`      departure${d.level === "todo" ? " (lacks)" : ""}: ${d.message}`);
  }
}
console.log(failed ? `\n${failed} force(s) need fixing` : "\nEvery force builds");
process.exit(failed ? 1 : 0);
