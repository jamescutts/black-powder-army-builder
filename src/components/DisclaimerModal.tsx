"use client";

import { useEffect, useState } from "react";
import { Button, Modal, Stack, Text } from "@mantine/core";
import { IconExternalLink } from "@tabler/icons-react";

const STORAGE_KEY = "bp-disclaimer-acknowledged-at";
const EXPIRY_MS = 7 * 24 * 60 * 60 * 1000; // 7 days

export function DisclaimerModal() {
  const [opened, setOpened] = useState(false);

  useEffect(() => {
    try {
      const acknowledgedAt = Number(localStorage.getItem(STORAGE_KEY));
      const isValid =
        Number.isFinite(acknowledgedAt) &&
        acknowledgedAt > 0 &&
        Date.now() - acknowledgedAt < EXPIRY_MS;
      if (!isValid) {
        setOpened(true);
      }
    } catch {
      // localStorage unavailable (private mode / SSR) — show it anyway
      setOpened(true);
    }
  }, []);

  function handleClose() {
    try {
      localStorage.setItem(STORAGE_KEY, String(Date.now()));
    } catch {
      // ignore write failures
    }
    setOpened(false);
  }

  return (
    <Modal
      opened={opened}
      onClose={handleClose}
      title="Disclaimer"
      centered
      withCloseButton={false}
      closeOnClickOutside={false}
      closeOnEscape={false}
      styles={{
        title: {
          fontWeight: 700,
          color: "var(--mantine-color-brown-8)",
        },
      }}
    >
      <Stack gap="md">
        <Text size="sm" c="dimmed" style={{ lineHeight: 1.6 }}>
          This is an unofficial, fan-made tool and is not affiliated with,
          endorsed by, or associated with{" "}
          <a
            href="https://www.warlordgames.com"
            target="_blank"
            rel="noreferrer"
            style={{ color: "var(--mantine-color-brown-7)" }}
          >
            Warlord Games
          </a>{" "}
          in any way.
        </Text>
        <Text size="sm" c="dimmed" style={{ lineHeight: 1.6 }}>
          <em>Black Powder</em>, all supplement titles, army list content, and
          associated intellectual property are copyright &copy; Warlord Games.
          All rights reserved.
        </Text>
        <Text size="sm" c="dimmed" style={{ lineHeight: 1.6 }}>
          The <em>Black Powder</em> rulebook and relevant supplements are
          required to play.
        </Text>
        <Text size="sm" c="dimmed" style={{ lineHeight: 1.6 }}>
          By continuing, you acknowledge that you own the relevant supplements
          in order to use this tool.
        </Text>
        <Stack gap="xs">
          <Button
            variant="outline"
            size="sm"
            color="brown.7"
            component="a"
            href="https://store.warlordgames.com/collections/rules-books/black-powder"
            target="_blank"
            rel="noreferrer"
            fullWidth
            rightSection={<IconExternalLink size={16} />}
          >
            Buy the rulebook &amp; supplements
          </Button>
          <Button color="brown.7" onClick={handleClose} fullWidth>
            I understand
          </Button>
        </Stack>
      </Stack>
    </Modal>
  );
}
