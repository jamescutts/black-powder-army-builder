import { createTheme, Paper, type MantineColorsTuple } from "@mantine/core";

// Warm brown accent — pulled from the supplement's ink/heading colour (dark saddle-brown on cream).
const brown: MantineColorsTuple = [
  "#f7ede1",
  "#eed9c0",
  "#dfbb8d",
  "#cf9c5c",
  "#c07f38",
  "#a66526",
  "#8a4f1c",
  "#6b3d17",
  "#4d2c11",
  "#33200f",
];

// Warm sepia "gray" replaces Mantine's cool default gray so borders, dividers and dimmed text
// stay in the same parchment family instead of looking bluish.
const warmGray: MantineColorsTuple = [
  "#f7f3ea",
  "#efe8d8",
  "#ddd2b8",
  "#c9b997",
  "#b39f7c",
  "#9c8563",
  "#7d6a4c",
  "#5f5038",
  "#453a28",
  "#2c2417",
];

export const theme = createTheme({
  primaryColor: "brown",
  primaryShade: 6,
  colors: { brown, gray: warmGray },
  // Mantine derives the light-mode page/surface background from `white` and body text from `black`.
  white: "#f2ecd6",
  black: "#2b1f14",
  fontFamily: "var(--font-body), Georgia, 'Times New Roman', serif",
  fontFamilyMonospace: "ui-monospace, SFMono-Regular, monospace",
  headings: {
    fontFamily: "var(--font-heading), Georgia, serif",
    fontWeight: "600",
  },
  defaultRadius: "md",
});
