import { appIconImage } from "@/lib/appIcon";

// The installed app's icons, named in manifest.ts. Built once at build time; any other name is a 404.
const ICONS: Record<string, { size: number; markScale: number }> = {
  "icon-192.png": { size: 192, markScale: 150 / 180 },
  "icon-512.png": { size: 512, markScale: 150 / 180 },
  // Android may crop a maskable icon to a circle 80% across, so the mark sits well inside that
  "maskable-512.png": { size: 512, markScale: 0.62 },
};

export const dynamicParams = false;

export function generateStaticParams() {
  return Object.keys(ICONS).map((icon) => ({ icon }));
}

export async function GET(_request: Request, { params }: { params: Promise<{ icon: string }> }) {
  const icon = ICONS[(await params).icon];
  if (!icon) return new Response("Not found", { status: 404 });
  return appIconImage(icon.size, icon.markScale);
}
