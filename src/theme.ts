import { createTheme, type MantineColorsTuple } from "@mantine/core";

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
// gray[6] is used by Mantine for "dimmed" — darkened to ensure ≥4.5:1 contrast on parchment bg.
const warmGray: MantineColorsTuple = [
  "#f7f3ea",
  "#efe8d8",
  "#d6c9ad",
  "#b8a582",
  "#9a8560",
  "#7d6a4c",
  "#63523a",
  "#4d3e2b",
  "#3a2e20",
  "#2c2417",
];

// Deep burgundy red based on #701626.
const red: MantineColorsTuple = [
  "#fbeced",
  "#f3d4d8",
  "#e4a3ab",
  "#d56f7c",
  "#c54455",
  "#a62b3c",
  "#882030",
  "#701626",
  "#5a101e",
  "#430b16",
];

// Warm amber yellow based on #fab11e.
const yellow: MantineColorsTuple = [
  "#fff8e1",
  "#ffecb3",
  "#fddf80",
  "#fcd24d",
  "#fbc626",
  "#fab11e",
  "#f9a318",
  "#f08f0f",
  "#e57d0a",
  "#d46503",
];

// Warm olive green to complement the parchment/brown palette.
const green: MantineColorsTuple = [
  "#eef3e2",
  "#dbe6c1",
  "#b8d08a",
  "#96b858",
  "#7aa23a",
  "#628a2d",
  "#4f7125",
  "#3f5a1e",
  "#304316",
  "#212e0f",
];

export const theme = createTheme({
  primaryColor: "brown",
  primaryShade: 6,
  colors: { brown, gray: warmGray, red, yellow, green },
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
