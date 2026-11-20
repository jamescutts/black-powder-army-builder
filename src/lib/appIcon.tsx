import { ImageResponse } from "next/og";

/** The header band's dark brown, behind the cream mark */
export const ICON_BACKGROUND = "#33200f";
const MARK = "#f2ecd6";

/**
 * The site's mark (a flaming grenade in a ring, as in icon.svg) on a full square, as a PNG. The phone
 * rounds or crops the square itself. `markScale` is the mark's width as a share of the square: about
 * 0.83 for an ordinary icon, and smaller for a maskable one, whose outer edge Android may crop away.
 */
export function appIconImage(size: number, markScale: number) {
  const mark = Math.round(size * markScale);
  return new ImageResponse(
    (
      <div
        style={{
          width: "100%",
          height: "100%",
          display: "flex",
          alignItems: "center",
          justifyContent: "center",
          background: ICON_BACKGROUND,
        }}
      >
        <svg width={mark} height={mark} viewBox="0 0 32 32">
          <circle cx="16" cy="16" r="13.4" fill="none" stroke={MARK} strokeWidth="1.1" />
          <circle cx="16" cy="19.4" r="5.8" fill={MARK} />
          <rect x="14.3" y="12.1" width="3.4" height="1.8" rx="0.3" fill={MARK} />
          <path
            d="M16 11.4c-1.5-1.7-0.7-3.6 0-5.1 0.7 1.5 1.5 3.4 0 5.1z"
            fill={MARK}
            stroke={MARK}
            strokeWidth="0.6"
            strokeLinejoin="round"
          />
          <path
            d="M14.9 11.7c-1.9-0.6-2.8-2.3-2.8-3.8 1.1 0.8 2.4 1.7 2.8 3.8z"
            fill={MARK}
            stroke={MARK}
            strokeWidth="0.6"
            strokeLinejoin="round"
          />
          <path
            d="M17.1 11.7c1.9-0.6 2.8-2.3 2.8-3.8-1.1 0.8-2.4 1.7-2.8 3.8z"
            fill={MARK}
            stroke={MARK}
            strokeWidth="0.6"
            strokeLinejoin="round"
          />
        </svg>
      </div>
    ),
    { width: size, height: size }
  );
}
