// Chrome, Edge and other Chromium browsers fire "beforeinstallprompt" when the site can be installed,
// often before the page's scripts have started. This inline script for the root layout keeps it on
// window.__installPrompt for the "Install the app" button (components/InstallApp.tsx).
export const CATCH_INSTALL_PROMPT =
  "window.addEventListener('beforeinstallprompt',function(e){window.__installPrompt=e;window.dispatchEvent(new Event('installpromptready'))})";
