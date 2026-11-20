import { appIconImage } from "@/lib/appIcon";

// Home-screen icon for iPhones and iPads: the same mark as icon.svg, on a full square (the phone rounds the corners)
export const size = { width: 180, height: 180 };
export const contentType = "image/png";

export default function AppleIcon() {
  return appIconImage(size.width, 150 / 180);
}
