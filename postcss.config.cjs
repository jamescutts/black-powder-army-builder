module.exports = {
  plugins: {
    "postcss-preset-mantine": {
      // Like Mantine's own @mixin light / @mixin dark: rules for the installed app only (`@mixin app`) or
      // for the site in a browser tab only (`@mixin browser`). The mark they test is set by lib/appMode.ts.
      mixins: {
        app: { "[data-app] &": { "@mixin-content": {} } },
        browser: { ":root:not([data-app]) &": { "@mixin-content": {} } },
      },
    },
    "postcss-simple-vars": {
      variables: {
        "mantine-breakpoint-xs": "36em",
        "mantine-breakpoint-sm": "48em",
        "mantine-breakpoint-md": "62em",
        "mantine-breakpoint-lg": "75em",
        "mantine-breakpoint-xl": "88em",
      },
    },
  },
};
