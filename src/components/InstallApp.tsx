"use client";

import { useEffect, useState, type ReactNode } from "react";
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

/**
 * How this browser installs the site: "prompt" where it can with one click (Chrome, Edge, Samsung
 * Internet and others), "ios" or "mac-safari" where it takes the menu steps, null where it can't (or
 * already is the installed app).
 */
export type InstallMode = "prompt" | "ios" | "mac-safari" | null;

/** The selling point, the same wherever the site offers to install */
export const INSTALL_PITCH =
  "Installed, Army Builder opens in its own window and works with no signal, so your armies are there at the club or a show.";

/**
 * Everything a call to install needs: whether to show it, what to do when it's pressed, and the help
 * dialog for Apple's browsers (render `help` alongside the button).
 */
export function useInstallApp(): { mode: InstallMode; install: () => void; help: ReactNode } {
  const [mode, setMode] = useState<InstallMode>(null);
  const [helpOpen, setHelpOpen] = useState(false);

  useEffect(() => {
    const standalone =
      window.matchMedia("(display-mode: standalone)").matches ||
      (navigator as Navigator & { standalone?: boolean }).standalone === true;
    if (standalone) return;

    const ua = navigator.userAgent;
    const isIos = /iPhone|iPad|iPod/.test(ua) || (/Macintosh/.test(ua) && navigator.maxTouchPoints > 1);
    const isMacSafari = /Macintosh/.test(ua) && /Safari\//.test(ua) && !/Chrome|Chromium|Edg|Firefox|OPR/.test(ua);

    const update = () => setMode(window.__installPrompt ? "prompt" : isIos ? "ios" : isMacSafari ? "mac-safari" : null);
    const installed = () => {
      window.__installPrompt = undefined;
      setMode(null);
    };
    update();
    window.addEventListener("installpromptready", update);
    window.addEventListener("appinstalled", installed);
    return () => {
      window.removeEventListener("installpromptready", update);
      window.removeEventListener("appinstalled", installed);
    };
  }, []);

  const install = async () => {
    const prompt = window.__installPrompt;
    if (mode !== "prompt" || !prompt) {
      setHelpOpen(true);
      return;
    }
    await prompt.prompt();
    const { outcome } = await prompt.userChoice;
    // The browser only offers each prompt once; it fires a fresh one if the site can still be installed
    window.__installPrompt = undefined;
    window.dispatchEvent(new Event(outcome === "accepted" ? "appinstalled" : "installpromptready"));
  };

  const help = (
    <InstallHelp mode={mode} opened={helpOpen} onClose={() => setHelpOpen(false)} />
  );

  return { mode, install, help };
}

/** The menu steps, for Apple's browsers, which have no install button a page can press */
function InstallHelp({ mode, opened, onClose }: { mode: InstallMode; opened: boolean; onClose: () => void }) {
  return (
    <Modal
      opened={opened}
      onClose={onClose}
      title="Install Army Builder"
      centered
      size="sm"
      styles={{ title: { fontFamily: "var(--font-heading), Georgia, serif", fontWeight: 600, fontSize: "1.15rem" } }}
    >
      <Text size="sm" mb="sm">
        {INSTALL_PITCH}
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
        <Button variant="default" onClick={onClose} data-autofocus>
          Done
        </Button>
      </Group>
    </Modal>
  );
}

/** "Install the app", as a link-like button (the footer). Hidden where the browser can't install. */
export function InstallApp({ className, children = "Install the app" }: { className?: string; children?: ReactNode }) {
  const { mode, install, help } = useInstallApp();
  if (!mode) return null;
  return (
    <>
      <button type="button" className={className} onClick={install}>
        {children}
      </button>
      {help}
    </>
  );
}
