// Sharing images (Open Graph cards): dark brown like the header, the site name in its script, and the page's
// own title in Spectral. Rendered at build time by the opengraph-image files.

import { readFile } from "node:fs/promises";
import { join } from "node:path";
import { ImageResponse } from "next/og";

export const OG_SIZE = { width: 1200, height: 630 };

const INK = "#33200f";
const CREAM = "#f2ecd6";
const GOLD = "#e0bf74";

const fontFile = (name: string) => readFile(join(process.cwd(), "src/app/og-fonts", name));

async function fonts() {
  const [spectral, tangerine] = await Promise.all([
    fontFile("Spectral-SemiBold.ttf"),
    fontFile("Tangerine-Bold.ttf"),
  ]);
  return [
    { name: "Spectral", data: spectral, weight: 600 as const, style: "normal" as const },
    { name: "Tangerine", data: tangerine, weight: 700 as const, style: "normal" as const },
  ];
}

/** A flag from /public as a data address, so the image renderer can draw it */
export async function flagDataUrl(publicPath: string) {
  const svg = await readFile(join(process.cwd(), "public", publicPath.replace(/^\//, "")));
  return `data:image/svg+xml;base64,${svg.toString("base64")}`;
}

/** The site card: the name large in its script, the tagline and what's covered */
export async function siteCard({ tagline, stats }: { tagline: string; stats: string }) {
  return new ImageResponse(
    (
      <div
        style={{
          width: "100%",
          height: "100%",
          display: "flex",
          flexDirection: "column",
          alignItems: "center",
          justifyContent: "center",
          background: INK,
          color: CREAM,
          fontFamily: "Spectral",
        }}
      >
        <div style={{ display: "flex", position: "absolute", top: 28, left: 28, right: 28, bottom: 28, border: `1.5px solid rgba(242, 236, 214, 0.3)` }} />
        <div style={{ fontFamily: "Tangerine", fontSize: 190, lineHeight: 1 }}>Army Builder</div>
        <div style={{ fontSize: 40, marginTop: 18, color: "rgba(242, 236, 214, 0.85)" }}>{tagline}</div>
        <div style={{ fontSize: 28, marginTop: 36, color: GOLD, letterSpacing: 3, textTransform: "uppercase" }}>
          {stats}
        </div>
      </div>
    ),
    { ...OG_SIZE, fonts: await fonts() }
  );
}

/** A page card: the site name small, then a gold label, the page's title and any flags beside it */
export async function pageCard({ kicker, title, flags = [] }: { kicker: string; title: string; flags?: string[] }) {
  const flagSrcs = await Promise.all(flags.map(flagDataUrl));
  const flagWidth = flagSrcs.length > 1 ? 180 : 240;

  return new ImageResponse(
    (
      <div
        style={{
          width: "100%",
          height: "100%",
          display: "flex",
          flexDirection: "column",
          padding: "64px 72px",
          background: INK,
          color: CREAM,
          fontFamily: "Spectral",
        }}
      >
        <div style={{ display: "flex", position: "absolute", top: 28, left: 28, right: 28, bottom: 28, border: `1.5px solid rgba(242, 236, 214, 0.3)` }} />
        <div style={{ fontFamily: "Tangerine", fontSize: 76, lineHeight: 1 }}>Army Builder</div>

        <div style={{ display: "flex", flex: 1, alignItems: "flex-end", justifyContent: "space-between", gap: 48 }}>
          <div style={{ display: "flex", flexDirection: "column", maxWidth: flagSrcs.length ? 760 : 1056 }}>
            <div style={{ fontSize: 28, color: GOLD, letterSpacing: 3, textTransform: "uppercase" }}>{kicker}</div>
            <div style={{ fontSize: title.length > 40 ? 62 : 78, lineHeight: 1.1, marginTop: 14 }}>{title}</div>
          </div>
          {flagSrcs.length > 0 && (
            <div style={{ display: "flex", flexDirection: "column", gap: 20, marginBottom: 8 }}>
              {flagSrcs.map((src) => (
                // eslint-disable-next-line @next/next/no-img-element
                <img
                  key={src.slice(-24)}
                  src={src}
                  alt=""
                  width={flagWidth}
                  height={(flagWidth * 2) / 3}
                  style={{ objectFit: "cover", borderRadius: 6, border: "2px solid rgba(242, 236, 214, 0.5)" }}
                />
              ))}
            </div>
          )}
        </div>
      </div>
    ),
    { ...OG_SIZE, fonts: await fonts() }
  );
}
