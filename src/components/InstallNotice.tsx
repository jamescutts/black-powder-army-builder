"use client";

import { useEffect, useState } from "react";
import { Notification } from "@mantine/core";

/**
 * Confirms an install. Chrome on Android only shows "Installing…" and then quietly adds the icon (often
 * to the app list rather than the home screen), so say where to find it.
 */
export function InstallNotice() {
  const [shown, setShown] = useState(false);

  useEffect(() => {
    const onInstalled = () => setShown(true);
    window.addEventListener("appinstalled", onInstalled);
    return () => window.removeEventListener("appinstalled", onInstalled);
  }, []);

  useEffect(() => {
    if (!shown) return;
    const timer = window.setTimeout(() => setShown(false), 10000);
    return () => window.clearTimeout(timer);
  }, [shown]);

  if (!shown) return null;
  return (
    <div className="undo-toast" role="status">
      <Notification withBorder color="brown" title="Army Builder is installed" onClose={() => setShown(false)}>
        Open it from your home screen or app list.
      </Notification>
    </div>
  );
}
