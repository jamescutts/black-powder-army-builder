// The PDF export's two libraries, loaded only when someone first exports. Kept in one place so the
// export and the offline warm-up (OfflineSupport) load the very same files, which the service worker
// then has saved for when there's no connection.
export async function loadPdfLibs() {
  const [{ default: html2canvas }, { jsPDF }] = await Promise.all([import("html2canvas-pro"), import("jspdf")]);
  return { html2canvas, jsPDF };
}
