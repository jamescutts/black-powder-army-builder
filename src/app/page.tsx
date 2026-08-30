"use client";

import { useState } from "react";
import { useRouter } from "next/navigation";
import Link from "next/link";
import {
  Anchor,
  Box,
  Button,
  Card,
  Center,
  Container,
  Group,
  Stack,
  Text,
  Title,
} from "@mantine/core";
import { IconArrowRight } from "@tabler/icons-react";

interface Ruleset {
  id: string;
  name: string;
  blurb: string;
  href: string;
}

// A small engraved-style fleuron, in the spirit of the rule-divider ornaments printed
// between sections in period rulebooks and title pages.
function PeriodOrnament() {
  return (
    <svg
      viewBox="0 0 200 40"
      width={140}
      height={28}
      fill="none"
      stroke="currentColor"
      strokeWidth={1.5}
      strokeLinecap="round"
    >
      <path d="M4 20 C 40 4, 68 4, 96 20" opacity={0.85} />
      <path d="M104 20 C 132 4, 160 4, 196 20" opacity={0.85} />
      <path d="M4 20 C 40 36, 68 36, 96 20" opacity={0.45} />
      <path d="M104 20 C 132 36, 160 36, 196 20" opacity={0.45} />
      <circle cx="100" cy="20" r="3.5" fill="currentColor" stroke="none" />
      <circle cx="4" cy="20" r="1.5" fill="currentColor" stroke="none" />
      <circle cx="196" cy="20" r="1.5" fill="currentColor" stroke="none" />
    </svg>
  );
}

const RULESETS: Ruleset[] = [
  {
    id: "black-powder",
    name: "Black Powder",
    blurb: "Warlord Games' mass-battle rules for horse-and-musket warfare, 1700-1900.",
    href: "/black-powder",
  },
];

export default function HomePage() {
  const router = useRouter();
  const [selectedRuleset, setSelectedRuleset] = useState<Ruleset | null>(null);

  function handleStart() {
    if (!selectedRuleset) return;
    router.push(selectedRuleset.href);
  }

  return (
    <Container size="lg" py={60}>
      <Stack gap={48}>
        {/* Header */}
        <Center>
          <Stack gap={4} align="center">
            <Title
              order={1}
              fz={{ base: 44, sm: 64 }}
              fw={800}
              c="brown.7"
              ta="center"
              style={{ fontFamily: "var(--font-script), cursive", lineHeight: 1.1, WebkitTextStroke: "0.5px currentColor" }}
            >
              Army Builder
            </Title>
            <Text c="dimmed" size="sm" ta="center">
              Points calculators for tabletop wargame army lists.
            </Text>
          </Stack>
        </Center>

        {/* Ruleset selection */}
        <Stack gap="md">
          <Title order={3} fz={18} fw={600} c="brown.8" ta="center">
            Choose a rule set
          </Title>
          <Group justify="center" gap="md" wrap="wrap">
            {RULESETS.map((ruleset) => {
              const isSelected = selectedRuleset?.id === ruleset.id;
              return (
                <Card
                  key={ruleset.id}
                  withBorder
                  radius="md"
                  padding="lg"
                  onClick={() => setSelectedRuleset(ruleset)}
                  style={{
                    cursor: "pointer",
                    width: 260,
                    borderColor: isSelected ? "var(--mantine-color-brown-6)" : undefined,
                    borderWidth: isSelected ? 2 : 1,
                    backgroundColor: isSelected
                      ? "var(--mantine-color-brown-0)"
                      : "var(--mantine-color-white)",
                    transition: "border-color 120ms ease, background-color 120ms ease, box-shadow 120ms ease",
                    boxShadow: isSelected
                      ? "0 2px 12px color-mix(in srgb, var(--mantine-color-brown-6) 20%, transparent)"
                      : undefined,
                  }}
                >
                  <Stack gap={10} align="center">
                    <Box c={isSelected ? "brown.6" : "brown.4"}>
                      <PeriodOrnament />
                    </Box>
                    <Text
                      fw={600}
                      fz="md"
                      c={isSelected ? "brown.7" : "brown.9"}
                      ta="center"
                      style={{ lineHeight: 1.3 }}
                    >
                      {ruleset.name}
                    </Text>
                    <Text size="xs" c="dimmed" ta="center" style={{ lineHeight: 1.5 }}>
                      {ruleset.blurb}
                    </Text>
                  </Stack>
                </Card>
              );
            })}
          </Group>
        </Stack>

        {/* CTA */}
        {selectedRuleset && (
          <Center>
            <Box>
              <Button
                size="lg"
                color="brown.7"
                rightSection={<IconArrowRight size={18} />}
                onClick={handleStart}
                px={40}
              >
                Continue
              </Button>
            </Box>
          </Center>
        )}

        <Center>
          <Text size="xs" c="dimmed">
            <Anchor component={Link} href="/docs" c="brown.7">
              Docs: adding a new supplement or army list
            </Anchor>
          </Text>
        </Center>
      </Stack>
    </Container>
  );
}
