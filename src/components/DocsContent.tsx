"use client";

import Link from "next/link";
import {
  Anchor,
  Card,
  Code,
  Container,
  Divider,
  List,
  Stack,
  Table,
  Text,
  Title,
} from "@mantine/core";

function CodeBlock({ children }: { children: string }) {
  return (
    <Code
      block
      style={{
        fontSize: "var(--mantine-font-size-xs)",
        overflowX: "auto",
        whiteSpace: "pre",
      }}
    >
      {children.trim()}
    </Code>
  );
}

function Section({
  id,
  title,
  children,
}: {
  id: string;
  title: string;
  children: React.ReactNode;
}) {
  return (
    <Stack gap="sm" id={id} style={{ scrollMarginTop: 24 }}>
      <Title order={2} fz={22} fw={700} c="brown.8">
        {title}
      </Title>
      {children}
    </Stack>
  );
}

function SubHeading({ children }: { children: React.ReactNode }) {
  return (
    <Title order={3} fz={16} fw={600} c="brown.7" mt="xs">
      {children}
    </Title>
  );
}

const TOC = [
  { id: "overview", label: "Overview" },
  { id: "folder-layout", label: "Folder layout" },
  { id: "supplement-file", label: "The supplement file" },
  { id: "nation-file", label: "The nation file" },
  { id: "special-rules", label: "Special rules vs. notes" },
  { id: "allies", label: "Allied contingents" },
  { id: "units", label: "Defining units" },
  { id: "brigades", label: "Defining brigades" },
  { id: "slots", label: "Slots: what goes in a brigade" },
  { id: "regiments", label: "Regiments (nested slots)" },
  { id: "conditional-slots", label: "Conditional & scaling slots" },
  { id: "brigade-rules", label: "Brigade-level rules" },
  { id: "army-rules", label: "Army-wide rules" },
  { id: "community-lists", label: "Community lists" },
  { id: "registering", label: "Registering your files" },
  { id: "checklist", label: "Checklists" },
];

export function DocsContent() {
  return (
    <Container size="md" py={48}>
      <Stack gap={48}>
        <Stack gap={4}>
          <Title
            order={1}
            fz={{ base: 34, sm: 44 }}
            fw={800}
            c="brown.7"
            style={{ fontFamily: "var(--font-script), cursive", lineHeight: 1.1 }}
          >
            Adding army lists
          </Title>
          <Text c="dimmed" size="sm">
            How the army lists in this builder are structured, and how to add a new supplement,
            nation, or community list of your own. No code required — every army list is a JSON
            data file.
          </Text>
          <Text size="sm">
            <Anchor component={Link} href="/black-powder">
              ← Back to the army builder
            </Anchor>
          </Text>
        </Stack>

        <Card withBorder radius="md" padding="lg">
          <Stack gap={6}>
            <Text fw={600} fz="sm" c="brown.8">
              On this page
            </Text>
            <List size="sm" spacing={4}>
              {TOC.map((t) => (
                <List.Item key={t.id}>
                  <Anchor href={`#${t.id}`} c="brown.7">
                    {t.label}
                  </Anchor>
                </List.Item>
              ))}
            </List>
          </Stack>
        </Card>

        <Section id="overview" title="Overview">
          <Text size="sm">
            Every army list — a nation, faction, or force within a supplement — is described
            entirely by a JSON file. There is no code to write. A JSON file lists the{" "}
            <strong>units</strong> a nation can field (infantry, cavalry, artillery, commanders,
            support options) and the <strong>brigades</strong> those units can be organised into,
            along with the min/max counts and special rules that govern each one.
          </Text>
          <Text size="sm">
            The app reads these files, builds the roster-building UI from them automatically, and
            enforces the rules you describe (minimums, maximums, "one per X points", "requires 2
            of these first", and so on) without any extra plumbing. Getting a new army list into
            the builder is a matter of writing the JSON correctly and pointing the app at it.
          </Text>
        </Section>

        <Section id="folder-layout" title="Folder layout">
          <Text size="sm">
            Army lists live under{" "}
            <Code>src/data/supplements/&lt;supplement-id&gt;/</Code>. Each supplement is a folder
            containing one <Code>supplement.json</Code> file and a <Code>nations/</Code> folder
            with one JSON file per army list:
          </Text>
          <CodeBlock>{`
src/data/supplements/
  clash-of-eagles/
    supplement.json
    nations/
      russia.json
      france.json
      austria.json
      ...
  albion-triumphant-2/
    supplement.json
    nations/
      brunswick.json
      french-army-corps.json
      ...
  community-lists/
    supplement.json
    nations/
      ottoman-empire.json
      prussia-1806.json
`}</CodeBlock>
          <Text size="sm">
            Which supplement a nation belongs to is determined <em>purely by which folder it sits
            in</em> — a nation's own JSON file never states its supplement id. This is important:
            renaming a supplement folder moves every nation inside it, and copying a nation file
            into a different supplement folder re-parents it.
          </Text>
        </Section>

        <Section id="supplement-file" title="The supplement file">
          <Text size="sm">
            <Code>supplement.json</Code> is small — it just describes the book (or, for community
            lists, the collection) that a group of nations belongs to:
          </Text>
          <CodeBlock>{`
{
  "id": "community-lists",
  "name": "Community Lists",
  "blurb": "Fan-created Black Powder army lists shared by the community, not part of an official Warlord Games supplement. Each list credits its author."
}
`}</CodeBlock>
          <Table withTableBorder withColumnBorders verticalSpacing="xs" fz="sm">
            <Table.Thead>
              <Table.Tr>
                <Table.Th>Field</Table.Th>
                <Table.Th>What it's for</Table.Th>
              </Table.Tr>
            </Table.Thead>
            <Table.Tbody>
              <Table.Tr>
                <Table.Td><Code>id</Code></Table.Td>
                <Table.Td>Unique short id, kebab-case. Should match the folder name.</Table.Td>
              </Table.Tr>
              <Table.Tr>
                <Table.Td><Code>name</Code></Table.Td>
                <Table.Td>Full title shown in the supplement picker.</Table.Td>
              </Table.Tr>
              <Table.Tr>
                <Table.Td><Code>blurb</Code></Table.Td>
                <Table.Td>One or two sentences describing the book/collection.</Table.Td>
              </Table.Tr>
            </Table.Tbody>
          </Table>
        </Section>

        <Section id="nation-file" title="The nation file">
          <Text size="sm">
            A nation file has a handful of top-level fields, then the two big lists —{" "}
            <Code>units</Code> and <Code>brigades</Code> — covered in their own sections below.
          </Text>
          <CodeBlock>{`
{
  "id": "ottoman-empire",
  "name": "Ottoman Empire",
  "blurb": "Napoleonic-era Ottoman army: Janissary corps, Sipahi and Deli cavalry, ...",
  "flagFile": "/flags/ottoman-empire.svg",
  "attribution": {
    "author": "Napoleonic Wargames",
    "sourceUrl": "https://www.youtube.com/watch?v=..."
  },
  "units": [ /* ... see "Defining units" ... */ ],
  "brigades": [ /* ... see "Defining brigades" ... */ ],
  "pointsCaps": [ /* optional, see "Army-wide rules" */ ],
  "unitRatioCaps": [ /* optional, see "Army-wide rules" */ ],
  "notes": [
    "Freeform bullet points shown to the player summarising the force-org rules."
  ],
  "specialRules": [
    "In-game special rules with a battlefield effect — see below."
  ],
  "alliesRules": [
    { "maxPercent": 25, "nationIds": ["some-other-nation-id"] }
  ]
}
`}</CodeBlock>
          <Table withTableBorder withColumnBorders verticalSpacing="xs" fz="sm">
            <Table.Thead>
              <Table.Tr>
                <Table.Th>Field</Table.Th>
                <Table.Th>Required?</Table.Th>
                <Table.Th>What it's for</Table.Th>
              </Table.Tr>
            </Table.Thead>
            <Table.Tbody>
              <Table.Tr>
                <Table.Td><Code>id</Code></Table.Td>
                <Table.Td>Yes</Table.Td>
                <Table.Td>Unique short id, kebab-case. Used in the URL.</Table.Td>
              </Table.Tr>
              <Table.Tr>
                <Table.Td><Code>name</Code></Table.Td>
                <Table.Td>Yes</Table.Td>
                <Table.Td>Display name in the nation picker and roster header.</Table.Td>
              </Table.Tr>
              <Table.Tr>
                <Table.Td><Code>blurb</Code></Table.Td>
                <Table.Td>Yes</Table.Td>
                <Table.Td>Short description shown on the nation's card.</Table.Td>
              </Table.Tr>
              <Table.Tr>
                <Table.Td><Code>flagFile</Code> / <Code>flagFiles</Code></Table.Td>
                <Table.Td>No</Table.Td>
                <Table.Td>
                  Path under <Code>public/flags/</Code> to an SVG flag. Use{" "}
                  <Code>flagFiles</Code> (an array) instead when one entry covers several
                  historical states, e.g. the Confederation of the Rhine.
                </Table.Td>
              </Table.Tr>
              <Table.Tr>
                <Table.Td><Code>attribution</Code></Table.Td>
                <Table.Td>Community lists only</Table.Td>
                <Table.Td>
                  <Code>{`{ author, sourceUrl? }`}</Code> — credits whoever wrote the list. See{" "}
                  <Anchor href="#community-lists" c="brown.7">Community lists</Anchor>.
                </Table.Td>
              </Table.Tr>
              <Table.Tr>
                <Table.Td><Code>notes</Code></Table.Td>
                <Table.Td>Yes (array, can be empty)</Table.Td>
                <Table.Td>
                  Freeform bullet points reminding the player of <em>force-organisation</em> rules
                  that aren't (or can't be) structurally enforced — ratios, per-points scaling,
                  unimplemented upgrades/downgrades. Not for in-game special rules or allied
                  contingents — see <Code>specialRules</Code> and <Code>alliesRules</Code> below.
                </Table.Td>
              </Table.Tr>
              <Table.Tr>
                <Table.Td><Code>specialRules</Code></Table.Td>
                <Table.Td>No</Table.Td>
                <Table.Td>
                  National special rules with an actual <em>in-game effect</em> — special
                  formations, commander traits, unique unit interactions. Shown to the player in
                  their own "Special Rules" section, separate from the force-org notes. See{" "}
                  <Anchor href="#special-rules" c="brown.7">Special rules vs. notes</Anchor>.
                </Table.Td>
              </Table.Tr>
              <Table.Tr>
                <Table.Td><Code>alliesRules</Code></Table.Td>
                <Table.Td>No</Table.Td>
                <Table.Td>
                  Structured allied-contingent allowances (max % of points, which nations). Shown
                  in its own "Allied Contingents" section. See{" "}
                  <Anchor href="#allies" c="brown.7">Allied contingents</Anchor>.
                </Table.Td>
              </Table.Tr>
            </Table.Tbody>
          </Table>
        </Section>

        <Section id="special-rules" title="Special rules vs. notes">
          <Text size="sm">
            Both fields are freeform string arrays on the nation, but they're shown to the player
            in different places and mean different things — keep them separate rather than lumping
            everything into <Code>notes</Code>:
          </Text>
          <List size="sm" spacing={4}>
            <List.Item>
              <Code>notes</Code> is for <strong>force-organisation</strong> reminders — things
              about how the army list is built (min/max counts, "1 per N points", allied
              percentages, periods, upgrades this builder doesn't model yet). It's shown under a
              "Force organisation reference" disclaimer, because none of it is structurally
              checked.
            </List.Item>
            <List.Item>
              <Code>specialRules</Code> is for <strong>battlefield</strong> rules — things that
              change how a unit or the army plays once the game starts. It's shown under its own
              "National special rules" heading.
            </List.Item>
          </List>
          <Text size="sm">Some real examples of what belongs in each:</Text>
          <Table withTableBorder withColumnBorders verticalSpacing="xs" fz="sm">
            <Table.Thead>
              <Table.Tr>
                <Table.Th>Field</Table.Th>
                <Table.Th>Example</Table.Th>
              </Table.Tr>
            </Table.Thead>
            <Table.Tbody>
              <Table.Tr>
                <Table.Td><Code>notes</Code></Table.Td>
                <Table.Td>
                  "0 to 1 Earthworks per 500 points." — a force-org scaling rule, already
                  structurally enforced via <Code>maxPerPoints</Code> but restated for clarity.
                </Table.Td>
              </Table.Tr>
              <Table.Tr>
                <Table.Td><Code>specialRules</Code></Table.Td>
                <Table.Td>
                  "'No prisoners! No pity!': against a French army, all Prussian infantry and
                  cavalry count as Tough Fighters." — a rule that changes how units fight.
                </Table.Td>
              </Table.Tr>
              <Table.Tr>
                <Table.Td><Code>specialRules</Code></Table.Td>
                <Table.Td>
                  "Angriffskolonne (Assault Column) and Zug Column (Column of Companies) represent
                  Prussian attack and manoeuvre formations." — special formations available on the
                  tabletop.
                </Table.Td>
              </Table.Tr>
              <Table.Tr>
                <Table.Td><Code>specialRules</Code></Table.Td>
                <Table.Td>
                  "The C-in-C may be the Sultan himself (+25 pts on top of Staff Rating), giving
                  all commanders +1 to their C-in-C re-rolls. …" — a commander trait with a
                  gameplay effect, even though it also unlocks force-org options.
                </Table.Td>
              </Table.Tr>
            </Table.Tbody>
          </Table>
          <Text size="sm">
            When in doubt: if it changes what happens on the tabletop, it's a special rule; if
            it's about which units you're allowed to buy and how many, it's a note.
          </Text>
        </Section>

        <Section id="allies" title="Allied contingents">
          <Text size="sm">
            Rather than a freeform "Allies: up to 25%..." note, allied allowances are structured
            as <Code>alliesRules</Code> — an array on the nation, since a nation can have more than
            one allowance (see France 1812 below, which gets a separate 25% for its Imperial Guard
            and a further 25% for any other ally). Each entry has a max percentage of the army's
            points, and either a list of specific allied nation ids or a freeform{" "}
            <Code>note</Code> when the book doesn't name a specific list:
          </Text>
          <CodeBlock>{`
"alliesRules": [
  { "maxPercent": 25, "nationIds": ["french-imperial-guard"] },
  { "maxPercent": 25, "note": "any other allied list" }
]
`}</CodeBlock>
          <Text size="sm">
            <Code>nationIds</Code> reference other nations' <Code>id</Code> fields in this same
            data set (they don't have to be in the same supplement — Austria's allies span both{" "}
            <Code>france</Code> and <Code>saxony</Code>, from two different supplements). The app
            resolves these to clickable links to that nation's own list. Use <Code>note</Code>{" "}
            alone, with no <Code>nationIds</Code>, for a generic grant like "any one allied list"
            that isn't tied to a specific nation:
          </Text>
          <CodeBlock>{`
"alliesRules": [
  { "maxPercent": 25, "note": "any one allied list" }
]
`}</CodeBlock>
          <Text size="sm">
            <Code>note</Code> can also carry extra conditions alongside specific{" "}
            <Code>nationIds</Code>, e.g. the French Army of the North Imperial Guard (1815), whose
            allied Corps brigades still enforce that Corps list's own minimums:
          </Text>
          <CodeBlock>{`
"alliesRules": [
  {
    "maxPercent": 25,
    "nationIds": ["french-army-corps"],
    "note": "any minimums from that list apply to the points spent here (e.g. taking a Guard Heavy Cavalry Brigade needs three Corps infantry brigades first)"
  }
]
`}</CodeBlock>
          <Text size="sm" c="dimmed">
            The roster builder doesn't support actually adding allied brigades to a list yet —{" "}
            <Code>alliesRules</Code> is reference information only, shown in its own "Allied
            Contingents" section alongside the special rules and force-org notes.
          </Text>
        </Section>

        <Section id="units" title="Defining units">
          <Text size="sm">
            Each entry in <Code>units</Code> is one troop type, commander, or support option the
            nation can field. It defines the stat line shown to the player and the cost(s) it can
            be taken for. A plain infantry unit with a single fixed cost:
          </Text>
          <CodeBlock>{`
{
  "id": "fr-line-infantry",
  "name": "French Line Infantry",
  "category": "Infantry",
  "type": "Regular Infantry",
  "armament": "Smoothbore Musket",
  "handToHand": "6",
  "shooting": "3",
  "morale": "4",
  "stamina": "3",
  "special": ["Pas de Charge"],
  "cost": 38
}
`}</CodeBlock>
          <Text size="sm">
            <Code>category</Code> must be one of <Code>Command</Code>, <Code>Infantry</Code>,{" "}
            <Code>Cavalry</Code>, <Code>Artillery</Code>, or <Code>Support</Code> — this is what
            slots a unit id can be listed in later. <Code>type</Code> and <Code>armament</Code>{" "}
            are free text shown on the stat line. <Code>handToHand</Code>, <Code>shooting</Code>,{" "}
            <Code>morale</Code>, <Code>stamina</Code>, and <Code>special</Code> are optional and
            omitted where they don't apply (e.g. a support option with no combat stats).
          </Text>
          <SubHeading>Units with priced options (variants)</SubHeading>
          <Text size="sm">
            When a unit has several priced choices — a weapon option, a commander's staff rating,
            half vs. full battery — use <Code>variants</Code> instead of a flat <Code>cost</Code>.
            Each variant is one choice the player picks from a dropdown:
          </Text>
          <CodeBlock>{`
{
  "id": "ot-cinc-commander",
  "name": "(Divisional) Commander",
  "category": "Command",
  "type": "Command",
  "armament": "-",
  "variants": [
    { "label": "Staff Rating 6", "cost": 0, "staffRating": 6 },
    { "label": "Staff Rating 7", "cost": 25, "staffRating": 7 },
    { "label": "Staff Rating 8", "cost": 50, "staffRating": 8 }
  ]
}
`}</CodeBlock>
          <Text size="sm">
            A variant's <Code>label</Code> is what's shown in the picker; <Code>cost</Code> is
            what that choice adds to the army total. <Code>staffRating</Code> is used for
            commanders. <Code>handToHand</Code>/<Code>shooting</Code> can also be overridden per
            variant when a weapon option changes a unit's stat line.
          </Text>
        </Section>

        <Section id="brigades" title="Defining brigades">
          <Text size="sm">
            <Code>brigades</Code> is the force-organisation chart: the list of brigade{" "}
            <em>types</em> a player can add to their army, and how many of each. A brigade type
            has an id/name, a min/max count, an optional commander requirement, and a list of{" "}
            <Code>slots</Code> describing what can go inside one instance of it:
          </Text>
          <CodeBlock>{`
{
  "id": "fac-infantry-brigade",
  "name": "Infantry Brigade",
  "min": 1,
  "max": 6,
  "commanderUnitId": "fac-brig-cmd",
  "slots": [
    {
      "label": "Line Infantry Battalion (3-7 per brigade)",
      "unitIds": ["fac-line"],
      "min": 3,
      "max": 7
    }
  ]
}
`}</CodeBlock>
          <Text size="sm">
            <Code>min</Code>/<Code>max</Code> on the brigade itself cap how many instances of this
            brigade type the whole army can take (e.g. "1 to 6 Infantry Brigades"). If a brigade
            needs its own commander (most combat brigades do), set{" "}
            <Code>commanderUnitId</Code> to the id of a <Code>Command</Code>-category unit; leave
            it out for pooled/attached support brigades (reserve artillery, earthworks) that don't
            carry their own commander.
          </Text>
        </Section>

        <Section id="slots" title="Slots: what goes in a brigade">
          <Text size="sm">
            The simplest slot just lists eligible unit ids and a count range, as above. From
            there, a slot can add per-unit and per-group limits within that same range:
          </Text>
          <SubHeading>Per-unit limits</SubHeading>
          <Text size="sm">
            <Code>unitLimits</Code> caps how many of one specific unit id can fill the slot, on
            top of the slot's overall min/max:
          </Text>
          <CodeBlock>{`
{
  "label": "Heavy Cavalry Regiments (up to 2 Carabinier + 3 Cuirassier, OR up to 4 Dragoon)",
  "unitIds": ["fr-carabinier", "fr-cuirassier", "fr-dragoon"],
  "min": 1,
  "max": 4,
  "unitLimits": [
    { "unitId": "fr-carabinier", "max": 2 },
    { "unitId": "fr-cuirassier", "max": 3 },
    { "unitId": "fr-dragoon", "max": 4 }
  ],
  "unitGroupLimits": [
    { "unitIds": ["fr-carabinier", "fr-cuirassier"], "max": 3, "label": "Carabinier/Cuirassier combined" }
  ],
  "mutuallyExclusiveGroups": [
    { "unitIds": ["fr-carabinier", "fr-cuirassier"], "label": "Carabinier/Cuirassier" },
    { "unitIds": ["fr-dragoon"], "label": "Dragoon" }
  ]
}
`}</CodeBlock>
          <Text size="sm">
            <Code>unitGroupLimits</Code> caps the <em>combined</em> quantity of several unit ids
            together — here, Carabinier + Cuirassier together can't exceed 3, even though each
            alone is allowed up to its own limit. <Code>mutuallyExclusiveGroups</Code> takes this
            further: it says only one of the listed groups may actually be used at all (you can
            take Carabinier/Cuirassier <em>or</em> Dragoon, never both in the same brigade). Set{" "}
            <Code>maxGroups</Code> on the first group's entry to allow "up to N of the following"
            instead of strictly one — see the Austrian example below, which allows up to 2 of 3
            option groups:
          </Text>
          <CodeBlock>{`
{
  "label": "Additional Troops (choose up to 2 options: 1-2 Grenadier, up to 2 Grenz, or 1 6-pdr Battery)",
  "unitIds": ["at-grenadier", "at-grenz", "at-6pdr-brigade-battery"],
  "min": 0,
  "max": 4,
  "unitLimits": [
    { "unitId": "at-grenadier", "max": 2 },
    { "unitId": "at-grenz", "max": 2 },
    { "unitId": "at-6pdr-brigade-battery", "max": 1 }
  ],
  "mutuallyExclusiveGroups": [
    { "unitIds": ["at-grenadier"], "label": "Grenadier battalions", "maxGroups": 2 },
    { "unitIds": ["at-grenz"], "label": "Large Grenz battalions" },
    { "unitIds": ["at-6pdr-brigade-battery"], "label": "6-pdr Brigade battery" }
  ]
}
`}</CodeBlock>
          <SubHeading>Requiring one unit type only</SubHeading>
          <Text size="sm">
            <Code>singleUnitType: true</Code> means every unit taken in the slot must be the{" "}
            <em>same</em> id — you can fill a "Spanish, Portuguese, or Rhinbund" slot with
            Spanish battalions or Portuguese battalions, but not a mix of the two.
          </Text>
        </Section>

        <Section id="regiments" title="Regiments (nested slots)">
          <Text size="sm">
            Some brigades (most Napoleonic infantry brigades) aren't just a flat list of
            battalions — they're organised into regiments, and each regiment has its own
            battalion count. For this, a slot carries a <Code>regiment</Code> block instead of a
            flat <Code>unitIds</Code>/<Code>min</Code>/<Code>max</Code>. The outer slot's own{" "}
            <Code>unitIds</Code>/<Code>min</Code>/<Code>max</Code> are ignored once{" "}
            <Code>regiment</Code> is present — set them to <Code>[]</Code>/<Code>0</Code>/
            <Code>0</Code> as placeholders:
          </Text>
          <CodeBlock>{`
{
  "label": "Line Infantry Regiments",
  "unitIds": [],
  "min": 0,
  "max": 0,
  "regiment": {
    "label": "Line Infantry Regiment",
    "min": 0,
    "max": 3,
    "slots": [
      {
        "label": "Line Infantry Battalion (1-5)",
        "unitIds": ["fr-line-infantry"],
        "min": 1,
        "max": 5
      }
    ]
  }
}
`}</CodeBlock>
          <Text size="sm">
            This reads as: "0 to 3 Line Infantry Regiments, each containing 1 to 5 Line Infantry
            battalions." The regiment's own <Code>slots</Code> array uses the same shape as a
            brigade slot (label/unitIds/min/max, plus <Code>singleUnitType</Code> and{" "}
            <Code>unitLimits</Code> where needed) — this is how a "Foreign Infantry Regiment" can
            require one nationality only per regiment:
          </Text>
          <CodeBlock>{`
{
  "label": "Foreign Infantry Regiment",
  "min": 0,
  "max": 1,
  "slots": [
    {
      "label": "Spanish (1-2), Portuguese (1-2), or Rhinbund (1) — one type only",
      "unitIds": ["fr-spanish-infantry", "fr-portuguese-infantry", "fr-rheinbund-infantry"],
      "min": 1,
      "max": 2,
      "singleUnitType": true,
      "unitLimits": [{ "unitId": "fr-rheinbund-infantry", "max": 1 }]
    }
  ]
}
`}</CodeBlock>
          <Text size="sm">
            A regiment can also cap itself across the <em>whole army</em> (not just per brigade)
            with <Code>armyMax</Code> — e.g. "max 1 Light Infantry Regiment in the entire army":
          </Text>
          <CodeBlock>{`
{
  "label": "Light Infantry Regiment",
  "min": 0,
  "max": 1,
  "armyMax": 1,
  "slots": [
    { "label": "Light Infantry Battalion (1-5)", "unitIds": ["fr-light-infantry"], "min": 1, "max": 5 }
  ]
}
`}</CodeBlock>
        </Section>

        <Section id="conditional-slots" title="Conditional & scaling slots">
          <Text size="sm">
            A slot can be locked behind a condition, or have its available quantity scale with
            something else in the army, instead of using a fixed number.
          </Text>
          <SubHeading>Unlocked by what else is in the same brigade</SubHeading>
          <Text size="sm">
            <Code>requiresBrigadeCount</Code> only makes a slot available once the combined
            quantity of the listed unit ids <em>within the same brigade instance</em> reaches a
            minimum — counted across every slot in that brigade, flat or regiment. For example,
            a Small Lancer Regiment that needs 2+ heavy cavalry regiments already taken:
          </Text>
          <CodeBlock>{`
{
  "label": "Small Lancer Regiment (0-1, requires 2+ heavy cavalry regiments)",
  "unitIds": ["fr-lancer-small"],
  "min": 0,
  "max": 1,
  "requiresBrigadeCount": {
    "unitIds": ["fr-carabinier", "fr-cuirassier", "fr-dragoon"],
    "min": 2
  }
}
`}</CodeBlock>
          <SubHeading>Unlocked by what's in the whole army</SubHeading>
          <Text size="sm">
            <Code>requiresArmyUnitCount</Code> works the same way but counts across every brigade
            in the army, not just this one — used for pooled/reserve artillery that only becomes
            available once the army has enough infantry or cavalry:
          </Text>
          <CodeBlock>{`
{
  "label": "Foot Artillery Battery (up to 1, if 6+ battalions in army)",
  "unitIds": ["fr-foot-arty"],
  "min": 0,
  "max": 1,
  "requiresArmyUnitCount": {
    "unitIds": ["fr-line-infantry", "fr-light-infantry", "fr-combined-grenadier", "fr-voltigeurs"],
    "min": 6
  }
}
`}</CodeBlock>
          <SubHeading>Scaling with the army's points total</SubHeading>
          <Text size="sm">
            <Code>maxPerPoints</Code> makes the slot's effective maximum grow with the army's
            total points, e.g. earthworks at "1 per 500 points":
          </Text>
          <CodeBlock>{`
{
  "label": "Earthworks (1 per 500 points)",
  "unitIds": ["ru-earthworks-standard", "ru-earthworks-large-1", "ru-earthworks-large-2"],
  "min": 1,
  "max": 1,
  "maxPerPoints": { "perPoints": 500 }
}
`}</CodeBlock>
          <SubHeading>Scaling with battalions taken in this brigade</SubHeading>
          <Text size="sm">
            <Code>dynamicUnitLimits</Code> is for regimental-artillery-style rules where the
            available quantity of one unit id depends on how many battalions or regiments are
            already in the <em>same brigade</em>. Two shapes are supported: <Code>perBattalions</Code>{" "}
            (max = battalions counted in the given slots ÷ ratio, rounded down) and{" "}
            <Code>perQualifyingRegiment</Code> (max = number of regiments, among the given
            regiment slots, that have reached a minimum battalion count):
          </Text>
          <CodeBlock>{`
{
  "label": "Regimental Artillery (section per 2 battalions, OR battery per regiment of 3+)",
  "unitIds": ["fr-regimental-arty-section", "fr-regimental-battery"],
  "min": 0,
  "max": 3,
  "singleUnitType": true,
  "dynamicUnitLimits": [
    {
      "unitId": "fr-regimental-arty-section",
      "perBattalions": { "countSlotIndices": [0, 1, 2], "ratio": 2 }
    },
    {
      "unitId": "fr-regimental-battery",
      "perQualifyingRegiment": { "regimentSlotIndices": [0, 1, 2], "minBattalions": 3 }
    }
  ]
}
`}</CodeBlock>
          <Text size="sm">
            The index arrays (<Code>countSlotIndices</Code>, <Code>regimentSlotIndices</Code>)
            refer to the position of slots within this same brigade's <Code>slots</Code> array —
            in this example, indices 0, 1, and 2 are the brigade's three infantry regiment slots.
          </Text>
        </Section>

        <Section id="brigade-rules" title="Brigade-level rules">
          <Text size="sm">
            These fields sit on the brigade type itself (alongside <Code>slots</Code>), not on an
            individual slot.
          </Text>
          <Table withTableBorder withColumnBorders verticalSpacing="xs" fz="sm">
            <Table.Thead>
              <Table.Tr>
                <Table.Th>Field</Table.Th>
                <Table.Th>What it does</Table.Th>
              </Table.Tr>
            </Table.Thead>
            <Table.Tbody>
              <Table.Tr>
                <Table.Td><Code>maxBattalions</Code></Table.Td>
                <Table.Td>
                  Caps the total unit count across all (or selected) slots in a single brigade
                  instance, e.g. "max 10 battalions per Infantry Brigade" →{" "}
                  <Code>{`{ max: 10, countSlotIndices: [0,1,2] }`}</Code>.
                </Table.Td>
              </Table.Tr>
              <Table.Tr>
                <Table.Td><Code>maxRegimentsTotal</Code></Table.Td>
                <Table.Td>
                  Caps the combined number of regiments across several regiment slots, e.g.
                  "1-3 Infantry Regiments total" across the Line/Light/Foreign slots →{" "}
                  <Code>{`{ slotIndices: [0,1,2], max: 3, min: 1 }`}</Code>.
                </Table.Td>
              </Table.Tr>
              <Table.Tr>
                <Table.Td><Code>requires</Code></Table.Td>
                <Table.Td>
                  This brigade type can't be added until other brigade types reach a combined
                  minimum count, e.g. Heavy Cavalry requiring 2 Infantry Brigades first →{" "}
                  <Code>{`{ brigadeTypeIds: ["fr-infantry-brigade"], min: 2 }`}</Code>.
                </Table.Td>
              </Table.Tr>
              <Table.Tr>
                <Table.Td><Code>maxRatio</Code></Table.Td>
                <Table.Td>
                  Caps how many of this brigade type you can take relative to other brigade
                  types, e.g. "max 1 Light Cavalry Brigade per 2 Infantry Brigades" →{" "}
                  <Code>{`{ brigadeTypeIds: ["fr-infantry-brigade"], ratio: 2 }`}</Code>.
                </Table.Td>
              </Table.Tr>
              <Table.Tr>
                <Table.Td><Code>minPerPoints</Code></Table.Td>
                <Table.Td>
                  Requires at least one of this brigade type per N points in the army (in
                  addition to <Code>min</Code>), e.g. "at least 1 Line Brigade per 500 points" →{" "}
                  <Code>{`{ perPoints: 500 }`}</Code>.
                </Table.Td>
              </Table.Tr>
              <Table.Tr>
                <Table.Td><Code>unitCaps</Code></Table.Td>
                <Table.Td>
                  Per-unit caps that apply across <em>every</em> instance of this brigade type in
                  the army (not just one brigade). Optional <Code>requiresBrigades</Code> gates the
                  unit behind another brigade type being taken first; optional{" "}
                  <Code>maxRatio</Code> makes the army-wide cap scale with another brigade type's
                  count.
                </Table.Td>
              </Table.Tr>
              <Table.Tr>
                <Table.Td><Code>note</Code></Table.Td>
                <Table.Td>
                  Freeform text for rules that aren't (or can't easily be) structurally enforced —
                  shown to the player as a reminder.
                </Table.Td>
              </Table.Tr>
            </Table.Tbody>
          </Table>
          <Text size="sm">
            A <Code>unitCaps</Code> example, from the Ottoman Deli Brigade — Mamelukes are capped
            at 6 across the whole army, but only once at least one Deli Brigade has been taken:
          </Text>
          <CodeBlock>{`
"unitCaps": [
  {
    "unitId": "ot-mameluke",
    "armyMax": 6,
    "requiresBrigades": { "brigadeTypeIds": ["ot-deli-brigade"], "min": 1 }
  }
]
`}</CodeBlock>
        </Section>

        <Section id="army-rules" title="Army-wide rules">
          <Text size="sm">
            Two optional fields sit on the nation itself, alongside <Code>units</Code> and{" "}
            <Code>brigades</Code>, for rules that span multiple brigade types.
          </Text>
          <SubHeading>Points percentage caps</SubHeading>
          <Text size="sm">
            <Code>pointsCaps</Code> limits a group of brigade types to a percentage of the army's
            total points — e.g. Imperial Guard brigades capped at 25% of the army:
          </Text>
          <CodeBlock>{`
"pointsCaps": [
  {
    "brigadeTypeIds": ["ru-guard-infantry-brigade", "ru-guard-light-cavalry-brigade", "ru-guard-heavy-cavalry-brigade"],
    "maxPercent": 25,
    "label": "Imperial Guard brigades"
  }
]
`}</CodeBlock>
          <SubHeading>Unit-to-unit ratio caps</SubHeading>
          <Text size="sm">
            <Code>unitRatioCaps</Code> limits the army-wide quantity of one group of units to a
            ratio of another group, regardless of which brigades they're in — e.g. "1 Grenz
            battalion per 4 line infantry battalions":
          </Text>
          <CodeBlock>{`
"unitRatioCaps": [
  {
    "capUnitIds": ["at-grenz"],
    "perUnitIds": ["at-infantry-german", "at-infantry-hungarian"],
    "ratio": 4,
    "label": "Grenz battalions (max 1 per 4 line infantry battalions)"
  }
]
`}</CodeBlock>
        </Section>

        <Section id="community-lists" title="Community lists">
          <Text size="sm">
            Fan-created lists that aren't from an official Warlord Games supplement go in{" "}
            <Code>src/data/supplements/community-lists/nations/</Code>. The only difference from
            an official list is the <Code>attribution</Code> field, which credits the original
            author and links to their source:
          </Text>
          <CodeBlock>{`
{
  "id": "ottoman-empire",
  "name": "Ottoman Empire",
  "attribution": {
    "author": "Napoleonic Wargames",
    "sourceUrl": "https://www.youtube.com/watch?v=BphFMuBJvtM"
  },
  ...
}
`}</CodeBlock>
          <Text size="sm">
            This shows a "Community list by …" credit on the nation's card, linking out to{" "}
            <Code>sourceUrl</Code> (a video, PDF, or forum post) when provided. Everything else —
            units, brigades, army-wide rules — works exactly the same as an official list.
          </Text>
          <Text size="sm">
            The whole Community Lists supplement is hidden unless the{" "}
            <Code>NEXT_PUBLIC_SHOW_COMMUNITY_LISTS</Code> environment variable is set to{" "}
            <Code>true</Code> (see <Code>.env.example</Code>) — set it in whichever environments
            should show fan-made lists (e.g. a preview/staging deployment), and leave it unset in
            production until you're ready to show them there too.
          </Text>
        </Section>

        <Section id="registering" title="Registering your files">
          <Text size="sm">
            JSON files aren't picked up automatically — they're imported explicitly in{" "}
            <Code>src/data/index.ts</Code>. To add a brand-new supplement:
          </Text>
          <List size="sm" spacing={4} type="ordered">
            <List.Item>
              Create <Code>src/data/supplements/&lt;supplement-id&gt;/supplement.json</Code>.
            </List.Item>
            <List.Item>
              Create <Code>src/data/supplements/&lt;supplement-id&gt;/nations/&lt;nation-id&gt;.json</Code>{" "}
              for each army list (no supplement reference needed inside the file — the folder is
              the source of truth).
            </List.Item>
            <List.Item>
              In <Code>src/data/index.ts</Code>, import <Code>supplement.json</Code> and each
              nation file, add the supplement to the <Code>supplements</Code> array, and add a{" "}
              <Code>withSupplement(...)</Code> block for its nations, appended to the{" "}
              <Code>nations</Code> array.
            </List.Item>
          </List>
          <Text size="sm">
            To add a new nation to an <em>existing</em> supplement, just add step 2 and 3's import
            (drop the file into that supplement's <Code>nations/</Code> folder, import it in{" "}
            <Code>index.ts</Code>, and add it to that supplement's <Code>withSupplement(...)</Code>{" "}
            list).
          </Text>
          <Text size="sm">
            If the nation has a flag, add the SVG under <Code>public/flags/</Code> and reference
            it from <Code>flagFile</Code> (or <Code>flagFiles</Code>) in the nation JSON.
          </Text>
        </Section>

        <Divider />

        <Section id="checklist" title="Checklists">
          <SubHeading>Adding a nation to an existing supplement</SubHeading>
          <List size="sm" spacing={4}>
            <List.Item>Write <Code>units</Code>: every troop type, with stats and cost(s).</List.Item>
            <List.Item>Write <Code>brigades</Code>: the force-org chart built from those unit ids.</List.Item>
            <List.Item>Add <Code>notes</Code> summarising anything not structurally enforced.</List.Item>
            <List.Item>Add <Code>specialRules</Code> for any in-game special rules (see <Anchor href="#special-rules" c="brown.7">Special rules vs. notes</Anchor>).</List.Item>
            <List.Item>Add <Code>alliesRules</Code> for any allied-contingent allowances (see <Anchor href="#allies" c="brown.7">Allied contingents</Anchor>).</List.Item>
            <List.Item>Add a flag SVG to <Code>public/flags/</Code> (optional).</List.Item>
            <List.Item>
              Save the file under the right supplement's <Code>nations/</Code> folder, import it
              in <Code>src/data/index.ts</Code>, and add it to that supplement's list.
            </List.Item>
          </List>
          <SubHeading>Adding a brand-new supplement</SubHeading>
          <List size="sm" spacing={4}>
            <List.Item>Create the supplement folder and <Code>supplement.json</Code>.</List.Item>
            <List.Item>Add one or more nation files as above.</List.Item>
            <List.Item>
              Import the supplement and its nations in <Code>src/data/index.ts</Code>; add the
              supplement to <Code>supplements</Code> and its nations via{" "}
              <Code>withSupplement(...)</Code>.
            </List.Item>
          </List>
          <SubHeading>Adding a community list</SubHeading>
          <List size="sm" spacing={4}>
            <List.Item>Same as "adding a nation", but under <Code>community-lists/nations/</Code>.</List.Item>
            <List.Item>
              Include an <Code>attribution</Code> field crediting the original author, with a{" "}
              <Code>sourceUrl</Code> where possible.
            </List.Item>
          </List>
          <Text size="sm" c="dimmed">
            Every field described on this page is defined with more detail in{" "}
            <Code>src/data/types.ts</Code>, which is the definitive reference if you get stuck.
          </Text>
        </Section>
      </Stack>
    </Container>
  );
}
