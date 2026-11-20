import coreWebVitals from "eslint-config-next/core-web-vitals";
import typescript from "eslint-config-next/typescript";

// Flat config for ESLint 9, replacing .eslintrc.json (which ESLint 9 no longer reads). Same rules as
// before: Next's core web vitals set, plus its TypeScript rules.
const config = [
  ...coreWebVitals,
  ...typescript,
  {
    files: ["**/*.{js,jsx,ts,tsx}"],
    rules: {
      // Several components read browser storage (saved lists, dismissed notices) once the page has
      // loaded, which has to set state in an effect so the server's page and the first render agree.
      // Kept as a warning so new cases still show up.
      "react-hooks/set-state-in-effect": "warn",
      // A leading underscore marks a value that's deliberately unused
      "@typescript-eslint/no-unused-vars": ["warn", { argsIgnorePattern: "^_", varsIgnorePattern: "^_" }],
    },
  },
  {
    ignores: [".next/**", ".open-next/**", ".wrangler/**", "node_modules/**", "next-env.d.ts"],
  },
];

export default config;
