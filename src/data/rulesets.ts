/** A game system the site builds army lists for, shown on the home page and in site search */
export interface Ruleset {
  id: string;
  name: string;
  blurb: string;
  href: string;
}

export const RULESETS: Ruleset[] = [
  {
    id: "black-powder",
    name: "Black Powder",
    blurb: "Warlord Games' mass-battle rules for horse-and-musket warfare, 1700-1900.",
    href: "/black-powder",
  },
];
