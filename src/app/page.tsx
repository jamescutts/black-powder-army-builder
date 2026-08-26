"use client";

import { useState } from "react";
import { useRouter } from "next/navigation";
import {
  Anchor,
  Box,
  Button,
  Card,
  Center,
  Container,
  Group,
  SimpleGrid,
  Stack,
  Text,
  Title,
} from "@mantine/core";
import { IconArrowRight } from "@tabler/icons-react";
import { supplements, getNationsForSupplement } from "@/data";
import type { Supplement } from "@/data/types";
import type { Nation } from "@/data/types";

export default function HomePage() {
  const router = useRouter();
  const [selectedSupplement, setSelectedSupplement] = useState<Supplement | null>(null);
  const [selectedNation, setSelectedNation] = useState<Nation | null>(null);

  const nations = selectedSupplement
    ? getNationsForSupplement(selectedSupplement.id)
    : [];

  function handleSupplementSelect(supplement: Supplement) {
    if (selectedSupplement?.id === supplement.id) return;
    setSelectedSupplement(supplement);
    setSelectedNation(null);
  }

  function handleNationSelect(nation: Nation) {
    setSelectedNation(nation);
  }

  function handleStart() {
    if (!selectedNation) return;
    router.push(`/builder?nation=${selectedNation.id}`);
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
              fw={700}
              c="brown.7"
              ta="center"
              style={{ fontFamily: "var(--font-script), cursive", lineHeight: 1.1 }}
            >
              Black Powder Army Builder
            </Title>
            <Text c="dimmed" size="sm" ta="center">
              Points calculator for{" "}
              <Anchor
                href="https://www.warlordgames.com"
                target="_blank"
                rel="noreferrer"
                c="brown.7"
              >
                Black Powder
              </Anchor>{" "}
              supplement army lists.
            </Text>
          </Stack>
        </Center>

        {/* Supplement selection */}
        <Stack gap="md">
          <Title order={3} fz={18} fw={600} c="brown.8" ta="center">
            Choose a supplement
          </Title>
          <SimpleGrid cols={{ base: 1, sm: 3 }} spacing="md">
            {supplements.map((supplement) => {
              const isSelected = selectedSupplement?.id === supplement.id;
              return (
                <Card
                  key={supplement.id}
                  withBorder
                  radius="md"
                  padding="lg"
                  onClick={() => handleSupplementSelect(supplement)}
                  style={{
                    cursor: "pointer",
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
                  <Stack gap={6} align="center">
                    <Text
                      fw={600}
                      fz="md"
                      c={isSelected ? "brown.7" : "brown.9"}
                      ta="center"
                      style={{ lineHeight: 1.3 }}
                    >
                      {supplement.name}
                    </Text>
                    <Text size="xs" c="dimmed" ta="center" style={{ lineHeight: 1.5 }}>
                      {supplement.blurb}
                    </Text>
                  </Stack>
                </Card>
              );
            })}
          </SimpleGrid>
        </Stack>

        {/* Nation selection — only shown once a supplement is picked */}
        {selectedSupplement && (
          <Stack gap="md">
            <Title order={3} fz={18} fw={600} c="brown.8" ta="center">
              Choose a nation
            </Title>
            <SimpleGrid
                cols={{ base: 2, sm: 3, md: 4 }}
                spacing="md"
                className="nation-grid"
              >
              {nations.map((nation) => {
                const isSelected = selectedNation?.id === nation.id;
                return (
                  <Card
                    key={nation.id}
                    withBorder
                    radius="md"
                    padding="md"
                    onClick={() => handleNationSelect(nation)}
                    style={{
                      cursor: "pointer",
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
                    <Stack gap={8} align="center">
                      {(() => {
                        const flags = nation.flagFiles ?? (nation.flagFile ? [nation.flagFile] : []);
                        if (flags.length === 0) return null;
                        return (
                          <Group gap={flags.length === 1 ? 4 : 8} justify="center" align="center" wrap="nowrap" style={{ width: "100%", height: 56, paddingInline: flags.length > 1 ? 8 : 0 }}>
                            {flags.map((f, i) => (
                              <div
                                key={i}
                                style={{
                                  position: "relative",
                                  height: flags.length === 1 ? 56 : 32,
                                  aspectRatio: "3 / 2",
                                  borderRadius: 4,
                                  border: "1px solid var(--mantine-color-gray-3)",
                                  overflow: "hidden",
                                  flexShrink: 0,
                                }}
                              >
                                <img
                                  src={f}
                                  alt=""
                                  style={{
                                    width: "100%",
                                    height: "100%",
                                    objectFit: "cover",
                                    display: "block",
                                  }}
                                />
                                {/* Weathered overlay: sepia tint + edge vignette */}
                                <div style={{
                                  position: "absolute",
                                  inset: 0,
                                  background: [
                                    "radial-gradient(ellipse at center, transparent 40%, rgba(60,30,5,0.35) 100%)",
                                    "linear-gradient(135deg, rgba(180,130,60,0.18) 0%, rgba(120,70,20,0.22) 100%)",
                                  ].join(", "),
                                  mixBlendMode: "multiply",
                                  pointerEvents: "none",
                                }} />
                              </div>
                            ))}
                          </Group>
                        );
                      })()}
                      <Stack gap={4} align="center">
                        <Text
                          fw={600}
                          fz="sm"
                          c={isSelected ? "brown.7" : "brown.9"}
                          ta="center"
                          style={{ lineHeight: 1.3 }}
                        >
                          {nation.name}
                        </Text>
                        {nation.blurb && (
                          <Text size="xs" c="dimmed" ta="center" lineClamp={2} style={{ lineHeight: 1.5 }}>
                            {nation.blurb}
                          </Text>
                        )}
                      </Stack>
                    </Stack>
                  </Card>
                );
              })}
            </SimpleGrid>
          </Stack>
        )}

        {/* CTA */}
        {selectedNation && (
          <Center>
            <Box>
              <Button
                size="lg"
                color="brown.7"
                rightSection={<IconArrowRight size={18} />}
                onClick={handleStart}
                px={40}
              >
                Build army
              </Button>
            </Box>
          </Center>
        )}
      </Stack>
    </Container>
  );
}
