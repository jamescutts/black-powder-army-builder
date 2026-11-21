"use client";

import { useState, type ReactNode } from "react";
import { Anchor, Button, Grid, Group, Modal, Stack, Text, ThemeIcon, Title } from "@mantine/core";
import {
  IconChevronRight,
  IconDeviceMobile,
  IconDownload,
  IconLayoutList,
  IconWifiOff,
  IconWorld,
} from "@tabler/icons-react";
import { useInstallApp } from "@/components/InstallApp";
import { HERO, type HomeArmy } from "@/components/HomeView";

const FEATURES: { icon: ReactNode; title: string }[] = [
  { icon: <IconWifiOff size={18} />, title: "Works with no signal" },
  { icon: <IconLayoutList size={18} />, title: "Your armies first" },
  { icon: <IconDeviceMobile size={18} />, title: "Its own window" },
]

const PLATFORMS: { name: string; how: string }[] = [
  {
    name: "Chrome, Edge or Samsung Internet",
    how: "On Android, Windows, Mac or a Chromebook: use the Install button, or Install in the browser's menu.",
  },
  { name: "iPhone and iPad", how: "Tap Share, then Add to Home Screen." },
  { name: "Safari on a Mac", how: "Choose File, then Add to Dock." },
  { name: "Firefox", how: "On Android, Add to Home screen in the menu. Firefox on a computer can't install apps." },
];

// People who decide to install often look in the app stores first, and find nothing
const NO_STORE_NOTE =
  "Army Builder isn't in the App Store or Google Play. It installs straight from your browser, free, in a few seconds.";

const SEPARATE_ARMIES_NOTE =
  "On iPhone and iPad the app keeps its own armies, separate from Safari's, so armies you've saved in the browser won't appear in it.";

/** Every device's steps, with the note about iPhone and iPad keeping their own armies */
function PlatformSteps() {
  return (
    <>
      <Text size="sm" mb="md" className="app-callout-no-store">
        {NO_STORE_NOTE}
      </Text>
      <Stack gap="sm">
        {PLATFORMS.map((p) => (
          <div key={p.name}>
            <Text size="sm" fw={600}>
              {p.name}
            </Text>
            <Text size="sm" c="dimmed" style={{ lineHeight: 1.5 }}>
              {p.how}
            </Text>
          </div>
        ))}
      </Stack>
      <Text size="xs" c="dimmed" mt="md" pt="sm" className="app-callout-note">
        {SEPARATE_ARMIES_NOTE}
      </Text>
    </>
  );
}

/** "How to install" for every device, in a pop-up */
function InstallStepsModal({ opened, onClose }: { opened: boolean; onClose: () => void }) {
  return (
    <Modal
      opened={opened}
      onClose={onClose}
      title="How to install Army Builder"
      centered
      size="md"
      styles={{ title: { fontFamily: "var(--font-heading), Georgia, serif", fontWeight: 600, fontSize: "1.15rem" } }}
    >
      <PlatformSteps />
    </Modal>
  );
}

/**
 * The install button, where the browser can install from the page: one click on Chrome, Edge and the
 * like, the step-by-step guide on Apple's browsers. Nothing elsewhere.
 */
function InstallButton({ size = "md" }: { size?: "sm" | "md" }) {
  const { mode, install, help } = useInstallApp();
  if (!mode) return null;
  return (
    <>
      <Button color="brown.7" size={size} leftSection={<IconDownload size={size === "sm" ? 16 : 18} />} onClick={install}>
        {mode === "prompt" ? "Install the app" : "Show me how to install"}
      </Button>
      {help}
    </>
  );
}

// The phone preview's Your armies, as someone might have them, and its army tiles, by army list. Their
// flags come from the army lists themselves (the home page's featured armies), so they follow any change.
const PREVIEW_ARMIES = [
  { id: "france", name: "Davout's I Corps", list: "The French 1812", points: 1250 },
  { id: "peninsular-british", name: "Wellington at Talavera", list: "The Peninsular British", points: 980 },
];
const PREVIEW_TILES = ["grand-duchy-of-warsaw", "austria", "prussians-1815", "bavaria"];

/** A small drawing of the app's home page in a phone. Decorative. */
function PhonePreview({ armies }: { armies: HomeArmy[] }) {
  const flagOf = (id: string) => armies.find((a) => a.href.endsWith(`/${id}`))?.flags[0];
  const tiles = PREVIEW_TILES.map(flagOf).filter((f) => f !== undefined);
  return (
    <div className="app-phone" aria-hidden>
      <div className="app-phone-header">
        <span className="app-phone-brand">Army Builder</span>
      </div>
      <div className="app-phone-screen">
        <div className="app-phone-banner">
          <img src={HERO.small} alt="" />
          <span>Build your army lists</span>
        </div>
        <div className="app-phone-heading">Your armies</div>
        <div className="app-phone-list">
          {PREVIEW_ARMIES.map((a) => (
            <div key={a.name} className="app-phone-row">
              {flagOf(a.id) && <img src={flagOf(a.id)} alt="" />}
              <span className="app-phone-row-text">
                <b>{a.name}</b>
                <small>{a.list}</small>
              </span>
              <span className="app-phone-points">{a.points}</span>
            </div>
          ))}
          <div className="app-phone-row app-phone-more">
            View my armies <IconChevronRight size={12} />
          </div>
        </div>
        <div className="app-phone-heading">All armies</div>
        <div className="app-phone-tiles">
          {tiles.map((f) => (
            <div key={f} className="app-phone-tile">
              <img src={f} alt="" />
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}

/**
 * The browser home page's case for the app, shown rather than described: a phone with the app's home page
 * in it beside three short reasons to install, the install button (where the browser can install from
 * here) and a link to every device's steps.
 */
export function AppCallout({ armies }: { armies: HomeArmy[] }) {
  const [stepsOpen, setStepsOpen] = useState(false);
  return (
    <Grid gap="xl" align="center">
      <Grid.Col span={{ base: 12, sm: 5 }} order={{ base: 2, sm: 1 }}>
        <PhonePreview armies={armies} />
      </Grid.Col>
      <Grid.Col span={{ base: 12, sm: 7 }} order={{ base: 1, sm: 2 }}>
        <Stack gap="md">
          <Stack gap={6}>
            <Text size="xs" c="dimmed" fw={600} tt="uppercase">
              The app
            </Text>
            <Title order={2} c="brown.8">
              Take it to the table
            </Title>
            <Text style={{ lineHeight: 1.6 }} maw="52ch">
              Install Army Builder and your armies are on your phone, tablet or computer, signal or not.
            </Text>
          </Stack>
          <Stack gap={10}>
            {FEATURES.map((f) => (
              <Group key={f.title} gap="sm" wrap="nowrap">
                <ThemeIcon variant="light" color="brown" size={30} radius="xl">
                  {f.icon}
                </ThemeIcon>
                <Text fw={600} c="brown.8">
                  {f.title}
                </Text>
              </Group>
            ))}
          </Stack>
          <Group gap="md" align="center">
            <InstallButton />
            <Anchor component="button" type="button" c="brown.7" size="sm" onClick={() => setStepsOpen(true)}>
              How to install on your device
            </Anchor>
          </Group>
          <Text size="sm" c="dimmed" maw="52ch" className="app-callout-no-store">
            <IconWorld size={16} aria-hidden />
            {NO_STORE_NOTE}
          </Text>
        </Stack>
      </Grid.Col>
      <InstallStepsModal opened={stepsOpen} onClose={() => setStepsOpen(false)} />
    </Grid>
  );
}
