import { ImageResponse } from "next/og";

// Home-screen icon for phones: the same mark as icon.svg, on a full square (the phone rounds the corners)
export const size = { width: 180, height: 180 };
export const contentType = "image/png";

export default function AppleIcon() {
  return new ImageResponse(
    (
      <div
        style={{
          width: "100%",
          height: "100%",
          display: "flex",
          alignItems: "center",
          justifyContent: "center",
          background: "#33200f",
        }}
      >
        <svg width="150" height="150" viewBox="0 0 32 32">
          <circle cx="16" cy="16" r="13.4" fill="none" stroke="#f2ecd6" strokeWidth="1.1" />
          <circle cx="16" cy="19.4" r="5.8" fill="#f2ecd6" />
          <rect x="14.3" y="12.1" width="3.4" height="1.8" rx="0.3" fill="#f2ecd6" />
          <path
            d="M16 11.4c-1.5-1.7-0.7-3.6 0-5.1 0.7 1.5 1.5 3.4 0 5.1z"
            fill="#f2ecd6"
            stroke="#f2ecd6"
            strokeWidth="0.6"
            strokeLinejoin="round"
          />
          <path
            d="M14.9 11.7c-1.9-0.6-2.8-2.3-2.8-3.8 1.1 0.8 2.4 1.7 2.8 3.8z"
            fill="#f2ecd6"
            stroke="#f2ecd6"
            strokeWidth="0.6"
            strokeLinejoin="round"
          />
          <path
            d="M17.1 11.7c1.9-0.6 2.8-2.3 2.8-3.8-1.1 0.8-2.4 1.7-2.8 3.8z"
            fill="#f2ecd6"
            stroke="#f2ecd6"
            strokeWidth="0.6"
            strokeLinejoin="round"
          />
        </svg>
      </div>
    ),
    size
  );
}
