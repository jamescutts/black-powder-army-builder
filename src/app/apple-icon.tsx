import { appIcon } from "@/lib/appIcon";

// Home-screen icon for iPhones and iPads: the site's mark on a full square (the phone rounds the corners)
export const size = { width: 180, height: 180 };
export const contentType = "image/png";

export default function AppleIcon() {
  return appIcon({ size: 180, mark: 150 / 180 });
}
