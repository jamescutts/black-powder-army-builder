import Link from "next/link";
import { Badge, Card, Group, Stack, Text } from "@mantine/core";
import type { CampaignSummary } from "@/data/battles";
import type { HistoricalCampaign } from "@/data/types";
import { campaignHref } from "@/lib/forces";

function CampaignArt({ art }: { art: HistoricalCampaign["art"] }) {
  return (
    <div className="home-card-photo" data-empty={!art || undefined}>
      {art && (
        <img src={art.src} alt={`${art.title}, ${art.artist}`} loading="lazy" style={{ objectPosition: art.focus }} />
      )}
    </div>
  );
}

/** A campaign's card: its painting, dates, summary and sides, opening the campaign's own page */
export function CampaignCard({ c }: { c: CampaignSummary }) {
  if (c.soon) {
    return (
      <Card withBorder radius="md" padding={0} className="home-card campaign-soon">
        <CampaignArt art={c.art} />
        <Stack gap={6} p="lg" pb={0}>
          <Text ff="heading" fw={600} fz={24} lh={1.2} c="brown.8">
            {c.name}
          </Text>
          <Text size="sm" fw={600} c="brown.8">
            {c.dates}
          </Text>
          <Text size="sm" c="brown.9" style={{ lineHeight: 1.55 }}>
            {c.summary}
          </Text>
        </Stack>
        <Group justify="flex-end" p="lg" style={{ marginTop: "auto" }}>
          <Badge color="gray" variant="light" size="lg">
            Coming soon
          </Badge>
        </Group>
      </Card>
    );
  }
  return (
    <Card withBorder radius="md" padding={0} className="picker-card home-card saved-list-card">
      {/* A painting across the top, as the book cards on the home page have */}
      <CampaignArt art={c.art} />
      <Stack gap={6} p="lg" pb={0}>
        {/* The card's link: it covers the whole card (see .saved-list-link) */}
        <Link href={campaignHref(c.id)} className="saved-list-link">
          <Text ff="heading" fw={600} fz={24} lh={1.2} c="brown.8">
            {c.name}
          </Text>
        </Link>
        <Group gap="xs" justify="space-between" wrap="nowrap">
          <Text size="sm" fw={600} c="brown.8">
            {c.dates}
          </Text>
          {c.forces === 0 && (
            <Badge color="gray" variant="light" size="sm">
              Forces to come
            </Badge>
          )}
        </Group>
        <Text size="sm" c="brown.9" style={{ lineHeight: 1.55 }}>
          {c.summary}
        </Text>
      </Stack>
      {c.sides && (
        <div style={{ marginTop: "auto", padding: "var(--mantine-spacing-lg)" }}>
          <CampaignSides sides={c.sides} />
        </div>
      )}
    </Card>
  );
}

/** A campaign's two sides, as rows of their nations' flags with "against" between them */
function CampaignSides({ sides }: { sides: NonNullable<HistoricalCampaign["sides"]> }) {
  return (
    <div className="campaign-sides">
      {sides.map((side, i) => (
        <Group key={side.name} gap={6} wrap="nowrap" className="campaign-side">
          {i > 0 && (
            <Text span size="xs" fs="italic" c="brown.8" mr={2}>
              against
            </Text>
          )}
          <Group gap={5} wrap="wrap" role="img" aria-label={`${side.name}: ${side.flags.map((f) => f.name).join(", ")}`}>
            {side.flags.map((flag) => (
              <span key={flag.name} className="campaign-flag" title={flag.name}>
                <img src={flag.src} alt="" />
              </span>
            ))}
          </Group>
        </Group>
      ))}
    </div>
  );
}
