import type { HistoricalBattle, HistoricalCampaign, HistoricalForce } from "../types";
import { getNation } from "../index";
import ligny from "./ligny.json";
import quatreBras from "./quatre-bras.json";
import waterloo from "./waterloo.json";
import wavre from "./wavre.json";

/**
 * Campaigns, each with its battles in the order they were fought, whose historical forces can be opened
 * as new lists. To add a battle, write src/data/battles/<battle-id>.json (a HistoricalBattle naming its
 * campaign's id) and import it here. Run `npm run check:forces` to see that every force builds and what
 * it breaks of its list's rules.
 */
export const campaigns: HistoricalCampaign[] = [
  {
    id: "hundred-days",
    name: "The Hundred Days",
    dates: "June 1815",
    summary:
      "Napoleon's return from Elba ended in four days in Belgium. He struck between Wellington's Anglo-allied army and Blücher's Prussians, beating the Prussians at Ligny while Ney held Wellington at Quatre Bras; two days later the allies joined to defeat him at Waterloo, while Grouchy fought the Prussian rearguard at Wavre.",
  },
];

const allBattles: HistoricalBattle[] = [ligny, quatreBras, waterloo, wavre] as HistoricalBattle[];

// Only the forces whose army lists this build shows (community lists can be switched off)
export const battles: HistoricalBattle[] = allBattles
  .map((b) => ({ ...b, forces: b.forces.filter((f) => getNation(f.nationId)) }))
  .filter((b) => b.forces.length > 0);

export function getCampaign(id: string): HistoricalCampaign | undefined {
  return campaigns.find((c) => c.id === id);
}

/** A campaign's battles, in the order they were fought */
export function battlesIn(campaignId: string): HistoricalBattle[] {
  return battles.filter((b) => b.campaign === campaignId);
}

export function getForce(id: string): HistoricalForce | undefined {
  for (const b of battles) {
    const force = b.forces.find((f) => f.id === id);
    if (force) return force;
  }
  return undefined;
}

export function battleOf(forceId: string): HistoricalBattle | undefined {
  return battles.find((b) => b.forces.some((f) => f.id === forceId));
}

/** One army list's historical forces, with their battles */
export function forcesFor(nationId: string): { battle: HistoricalBattle; force: HistoricalForce }[] {
  return battles.flatMap((battle) =>
    battle.forces.filter((f) => f.nationId === nationId).map((force) => ({ battle, force }))
  );
}
