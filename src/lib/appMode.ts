// Marks the page when it's running as the installed app (its own window, not a browser tab), so the
// design can differ there. In order of preference:
//   - className="app-hidden" or "app-only" on any element or Mantine component (app/globals.css)
//   - @mixin app { … } or @mixin browser { … } in CSS (postcss.config.cjs)
//   - useIsApp() in a component, for differences that aren't styling (lib/useIsApp.ts)
// An inline script for the root layout's <head>, so the mark is there before the page first draws and
// app-only styles never flash.
//
// Most browsers match "(display-mode: standalone)" in the app. Older iOS home-screen apps only set
// navigator.standalone. Chrome can move a tab into an app window without reloading, so it watches for
// that and fires "appmodechange" for useIsApp().
//
// While developing, ?app=1 on any address makes the tab act as the app until ?app=0, so the app's
// design can be checked without installing it. Production builds leave this out.
const FAKE_IN_DEV =
  process.env.NODE_ENV === "production"
    ? "false"
    : "(function(){try{var q=new URLSearchParams(location.search).get('app');" +
      "if(q==='1')sessionStorage.setItem('fakeApp','1');else if(q==='0')sessionStorage.removeItem('fakeApp');" +
      "return sessionStorage.getItem('fakeApp')==='1'}catch(e){return false}})()";

export const MARK_APP_MODE =
  "(function(){var m=window.matchMedia('(display-mode: standalone)'),r=document.documentElement,f=" +
  FAKE_IN_DEV +
  ";function u(){var a=f||m.matches||navigator.standalone===true;if(a===r.hasAttribute('data-app'))return;" +
  "if(a)r.setAttribute('data-app','');else r.removeAttribute('data-app');" +
  "window.dispatchEvent(new Event('appmodechange'))}" +
  "u();if(m.addEventListener)m.addEventListener('change',u)})()";

/** Whether the page is running as the installed app. Only in the browser (always false on the server). */
export function isAppMode(): boolean {
  return typeof document !== "undefined" && document.documentElement.hasAttribute("data-app");
}
