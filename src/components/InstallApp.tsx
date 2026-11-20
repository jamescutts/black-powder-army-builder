"use client";

import { useEffect, useState } from "react";
import { Button, Group, List, Modal, Text } from "@mantine/core";

// The browser's install prompt, kept on window.__installPrompt by an inline script (lib/installPrompt.ts)
interface InstallPromptEvent extends Event {
  prompt(): Promise<void>;
  userChoice: Promise<{ outcome: "accepted" | "dismissed" }>;
}

declare global {
  interface Window {
    __installPrompt?: InstallPromptEvent;
  }
}

type Mode = "prompt" | "ios" | "mac-safari" | null;

/**
 * "Install the app", in the footer. Where the browser can install it with one click (Chrome, Edge,
 * Samsung Internet and others), it asks the browser. Apple's browsers have no such button, so there it
 * explains the menu steps instead. Hidden in the installed app itself and in browsers that can't install.
 */
export function InstallApp({ className }: { className?: string }) {
  const [mode, setMode] = useState<Mode>(null);
  const [helpOpen, setHelpOpen] = useState(false);

  useEffect(() => {
    const standalone =
      window.matchMedia("(display-mode: standalone)").matches ||
      (navigator as Navigator & { standalone?: boolean }).standalone === true;
    if (standalone) return;

    const ua = navigator.userAgent;
    const isIos = /iPhone|iPad|iPod/.test(ua) || (/Macintosh/.test(ua) && navigator.maxTouchPoints > 1);
    const isMacSafari = /Macintosh/.test(ua) && /Safari\//.test(ua) && !/Chrome|Chromium|Edg|Firefox|OPR/.test(ua);

    const fromPrompt = () => setMode(window.__installPrompt ? "prompt" : isIos ? "ios" : isMacSafari ? "mac-safari" : null);
    const installed = () => {
      window.__installPrompt = undefined;
      setMode(null);
    };
    fromPrompt();
    window.addEventListener("installpromptready", fromPrompt);
    window.addEventListener("appinstalled", installed);
    return () => {
      window.removeEventListener("installpromptready", fromPrompt);
      window.removeEventListener("appinstalled", installed);
    };
  }, []);

  if (!mode) return null;

  const onClick = async () => {
    const prompt = window.__installPrompt;
    if (mode !== "prompt" || !prompt) {
      setHelpOpen(true);
      return;
    }
    await prompt.prompt();
    const { outcome } = await prompt.userChoice;
    // The browser only offers each prompt once; it fires a fresh one if the site can still be installed
    window.__installPrompt = undefined;
    if (outcome === "accepted") setMode(null);
  };

  return (
    <>
      <button type="button" className={className} onClick={onClick}>
        Install the app
      </button>
      <Modal
        opened={helpOpen}
        onClose={() => setHelpOpen(false)}
        title="Install Army Builder"
        centered
        size="sm"
        styles={{ title: { fontFamily: "var(--font-heading), Georgia, serif", fontWeight: 600, fontSize: "1.15rem" } }}
      >
        <Text size="sm" mb="sm">
          Installed, Army Builder opens in its own window and works without a connection, so you can build and
          check an army at the club even with no signal.
        </Text>
        {mode === "ios" ? (
          <List type="ordered" size="sm" spacing={4} mb="sm">
            <List.Item>
              Tap the <strong>Share</strong> button (a square with an arrow pointing up). If you can&apos;t see it,
              tap the <strong>•••</strong> button first.
            </List.Item>
            <List.Item>
              Scroll down and tap <strong>Add to Home Screen</strong>.
            </List.Item>
            <List.Item>
              Tap <strong>Add</strong>.
            </List.Item>
          </List>
        ) : (
          <List type="ordered" size="sm" spacing={4} mb="sm">
            <List.Item>
              In Safari&apos;s menu bar, choose <strong>File</strong>, then <strong>Add to Dock</strong>.
            </List.Item>
            <List.Item>
              Click <strong>Add</strong>.
            </List.Item>
          </List>
        )}
        {mode === "ios" && (
          <Text size="xs" c="dimmed" mb="md">
            The app keeps its own saved armies, separate from the browser&apos;s, so armies you saved in the browser
            won&apos;t appear in it.
          </Text>
        )}
        <Group justify="flex-end">
          <Button variant="default" onClick={() => setHelpOpen(false)} data-autofocus>
            Done
          </Button>
        </Group>
      </Modal>
    </>
  );
}
