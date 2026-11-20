import { ImageResponse } from "next/og";

const INK = "#33200f";
const CREAM = "#f2ecd6";

/**
 * The site's mark (the same drawing as app/icon.svg) in cream on the header's dark ink, as a square PNG.
 * `mark` is how much of the square the drawing fills. `rounded` gives the square soft corners, for desktops
 * that show the icon as it is; phones round or mask the square themselves, so their icons stay full.
 */
export function appIcon({ size, mark, rounded = false }: { size: number; mark: number; rounded?: boolean }) {
  const markSize = Math.round(size * mark);
  return new ImageResponse(
    (
      <div
        style={{
          width: "100%",
          height: "100%",
          display: "flex",
          alignItems: "center",
          justifyContent: "center",
          background: INK,
          borderRadius: rounded ? Math.round(size * 0.2) : 0,
        }}
      >
        <svg width={markSize} height={markSize} viewBox="0 0 32 32">
          <circle cx="16" cy="16" r="13.4" fill="none" stroke={CREAM} strokeWidth="1.1" />
          <circle cx="16" cy="19.4" r="5.8" fill={CREAM} />
          <rect x="14.3" y="12.1" width="3.4" height="1.8" rx="0.3" fill={CREAM} />
          <path
            d="M16 11.4c-1.5-1.7-0.7-3.6 0-5.1 0.7 1.5 1.5 3.4 0 5.1z"
            fill={CREAM}
            stroke={CREAM}
            strokeWidth="0.6"
            strokeLinejoin="round"
          />
          <path
            d="M14.9 11.7c-1.9-0.6-2.8-2.3-2.8-3.8 1.1 0.8 2.4 1.7 2.8 3.8z"
            fill={CREAM}
            stroke={CREAM}
            strokeWidth="0.6"
            strokeLinejoin="round"
          />
          <path
            d="M17.1 11.7c1.9-0.6 2.8-2.3 2.8-3.8-1.1 0.8-2.4 1.7-2.8 3.8z"
            fill={CREAM}
            stroke={CREAM}
            strokeWidth="0.6"
            strokeLinejoin="round"
          />
        </svg>
      </div>
    ),
    { width: size, height: size }
  );
}
