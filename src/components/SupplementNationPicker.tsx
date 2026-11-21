"use client";

import { useEffect, useRef, useState } from "react";
import { flushSync } from "react-dom";
import { useRouter } from "next/navigation";
import {
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
import { supplements, getSupplement, getNationsForSupplement } from "@/data";
import type { Supplement } from "@/data/types";
import type { Nation } from "@/data/types";

/**
 * Shared supplement/nation picker used both at /black-powder (no supplement chosen yet) and
 * /black-powder/[supplement] (supplement fixed by the URL, nation still to be chosen).
 */
export function SupplementNationPicker({ initialSupplementId }: { initialSupplementId?: string }) {
  const router = useRouter();
  const initialSupplement = initialSupplementId ? getSupplement(initialSupplementId) ?? null : null;
  const [selectedSupplement, setSelectedSupplement] = useState<Supplement | null>(initialSupplement);
  const [selectedNation, setSelectedNation] = useState<Nation | null>(null);

  const nations = selectedSupplement
    ? getNationsForSupplement(selectedSupplement.id)
    : [];

  // Choosing a book shows its armies below it, which on a phone are below the bottom of the window. So
  // the page scrolls down to them, if they aren't already in view. It happens here, with the armies
  // drawn at once (flushSync), as the new address then draws the page afresh, in the same place.
  const nationsRef = useRef<HTMLDivElement>(null);
  function handleSupplementSelect(supplement: Supplement) {
    if (selectedSupplement?.id === supplement.id) return;
    flushSync(() => {
      setSelectedSupplement(supplement);
      setSelectedNation(null);
    });
    revealSection(nationsRef.current);
    router.replace(`/black-powder/${supplement.id}`, { scroll: false });
  }

  function handleNationSelect(nation: Nation) {
    setSelectedNation(nation);
  }

  function handleStart() {
    if (!selectedSupplement || !selectedNation) return;
    router.push(`/black-powder/${selectedSupplement.id}/${selectedNation.id}`);
  }

  // Keep local state in sync if the URL's supplement segment changes (e.g. back/forward nav).
  useEffect(() => {
    setSelectedSupplement(initialSupplementId ? getSupplement(initialSupplementId) ?? null : null);
    setSelectedNation(null);
  }, [initialSupplementId]);

  return (
    <>
      <Container size="lg" className="picker-page">
        <Stack gap={48} className="picker-stack">
          {/* The rule set's name and what this page is for, centred like the picker below */}
          <Stack gap={6} align="center" ta="center" maw={640} mx="auto">
            <Title order={1} fz={{ base: 26, sm: 32 }} fw={600} c="brown.7" lh={1.2} className="picker-title">
              Black Powder
            </Title>
            <Text c="dimmed" style={{ lineHeight: 1.6 }} className="picker-intro">
              Warlord Games&apos; mass-battle rules for horse-and-musket warfare. Choose a supplement, then the army
              you want to build.
            </Text>
          </Stack>

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
                    component="button"
                    type="button"
                    withBorder
                    radius="md"
                    padding="lg"
                    className="picker-card"
                    data-selected={isSelected || undefined}
                    aria-pressed={isSelected}
                    onClick={() => handleSupplementSelect(supplement)}
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
            <Stack gap="md" ref={nationsRef} className="picker-section">
              <Title order={3} fz={18} fw={600} c="brown.8" ta="center">
                Choose a nation
              </Title>
              {/* Equal-height rows, with a short last row centred (see .nation-grid) */}
              <div className="nation-grid">
                {nations.map((nation) => {
                  const isSelected = selectedNation?.id === nation.id;
                  return (
                    <Card
                      key={nation.id}
                      component="button"
                      type="button"
                      withBorder
                      radius="md"
                      padding="md"
                      className="picker-card"
                      data-selected={isSelected || undefined}
                      aria-pressed={isSelected}
                      onClick={() => handleNationSelect(nation)}
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
                          {nation.attribution && (
                            <Text size="xs" c="brown.6" fs="italic" ta="center">
                              Community list by {nation.attribution.author}
                            </Text>
                          )}
                        </Stack>
                      </Stack>
                    </Card>
                  );
                })}
              </div>
            </Stack>
          )}

          {/* CTA */}
          {selectedNation && (
            <Center className="picker-build">
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
    </>
  );
}

/**
 * Scrolls a section that's just appeared to the top of the window, unless its heading and the start of
 * its contents are already in view. Smoothly, unless the device asks for less motion.
 */
function revealSection(el: HTMLElement | null) {
  if (!el) return;
  if (el.getBoundingClientRect().top + 160 <= window.innerHeight) return;
  const reduce = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  el.scrollIntoView({ behavior: reduce ? "auto" : "smooth", block: "start" });
}
