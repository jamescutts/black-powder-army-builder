import { appIcon } from "@/lib/appIcon";

// The installed app's icons, listed in the manifest (app/manifest.ts). Drawn once at build time.
//  - icon-*: rounded squares, for desktops and launchers that show the icon as it is
//  - maskable-*: full squares with the mark inside the middle 80%, for Android, which crops them to its
//    own shape (circle, squircle, ...)
const ICONS: Record<string, { size: number; mark: number; rounded?: boolean }> = {
  "icon-192.png": { size: 192, mark: 0.78, rounded: true },
  "icon-512.png": { size: 512, mark: 0.78, rounded: true },
  "maskable-192.png": { size: 192, mark: 0.66 },
  "maskable-512.png": { size: 512, mark: 0.66 },
};

export const dynamic = "force-static";
export const dynamicParams = false;

export function generateStaticParams() {
  return Object.keys(ICONS).map((icon) => ({ icon }));
}

export async function GET(_req: Request, { params }: { params: Promise<{ icon: string }> }) {
  const spec = ICONS[(await params).icon];
  if (!spec) return new Response("Not found", { status: 404 });
  return appIcon(spec);
}
