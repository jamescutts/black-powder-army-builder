// Marks the page when there's no connection, so the design can say so and quieten what needs one:
//   - className="offline-only" or "needs-network" on any element (app/globals.css)
//   - @mixin offline { … } or @mixin online { … } in CSS (postcss.config.cjs)
//   - useIsOffline() in a component, for differences that aren't styling (lib/useIsOffline.ts)
// An inline script for the root layout's <head>, like the app mark (lib/appMode.ts).
//
// Two signals. The browser's own flag is sure when it says offline (flight mode, no signal) but not when
// it says online: one bar of signal, or club Wi-Fi with a sign-in page, still counts. So the service
// worker also reports when the network fails it, or takes too long, and when it answers again
// (reportNetwork, from components/OfflineSupport.tsx); either one marks the page offline. The browser
// saying it's back online clears the worker's report too, until the worker says otherwise.
//
// While developing, ?offline=1 on any address makes the tab act offline until ?offline=0, as the service
// worker doesn't run then. Production builds leave this out.
const FAKE_IN_DEV =
  process.env.NODE_ENV === "production"
    ? "false"
    : "(function(){try{var q=new URLSearchParams(location.search).get('offline');" +
      "if(q==='1')sessionStorage.setItem('fakeOffline','1');else if(q==='0')sessionStorage.removeItem('fakeOffline');" +
      "return sessionStorage.getItem('fakeOffline')==='1'}catch(e){return false}})()";

export const MARK_OFFLINE =
  "(function(){var r=document.documentElement,n=false,f=" +
  FAKE_IN_DEV +
  ";function u(){var o=f||n||navigator.onLine===false;if(o===r.hasAttribute('data-offline'))return;" +
  "if(o)r.setAttribute('data-offline','');else r.removeAttribute('data-offline');" +
  "window.dispatchEvent(new Event('offlinechange'))}" +
  "window.__networkFailed=function(v){n=!!v;u()};" +
  "addEventListener('online',function(){n=false;u()});addEventListener('offline',u);u()})()";

declare global {
  interface Window {
    __networkFailed?: (failed: boolean) => void;
  }
}

/** Whether the page has no connection. Only in the browser (always false on the server). */
export function isOffline(): boolean {
  return typeof document !== "undefined" && document.documentElement.hasAttribute("data-offline");
}

/** What the service worker last found: whether the network answered it */
export function reportNetwork(ok: boolean) {
  window.__networkFailed?.(!ok);
}
