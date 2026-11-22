"use client";

import "leaflet/dist/leaflet.css";
import { useEffect, useRef, useState } from "react";
import { useRouter } from "next/navigation";
import type * as Leaflet from "leaflet";
import { Text, UnstyledButton } from "@mantine/core";
import { isPlanned, scheduleIn } from "@/data/battles";
import { battlePlaces, campaignMaps, type LabelSide, type LatLng, type MapRoute, type MapSide } from "@/data/battles/geo";
import { battleHref } from "@/lib/forces";

// A campaign's theatre on a map, as on Fleet Ledger's war pages: each battle a marked, labelled point
// (those with forces open their page; those still to come are paler), and the armies' main movements as
// arrowed lines, coloured and dashed by side. Leaflet over Esri's physical basemap, which needs no key.

// Relief and land cover only: no roads, borders or modern names, so with a sepia wash it reads as an old atlas
const TILES = {
  physical: {
    url: "https://server.arcgisonline.com/ArcGIS/rest/services/World_Physical_Map/MapServer/tile/{z}/{y}/{x}",
    maxNativeZoom: 8,
    attribution: "Tiles &copy; Esri, US National Park Service",
  },
  // Hill shading alone, with finer tiles, for a theatre as close as Waterloo's
  relief: {
    url: "https://server.arcgisonline.com/ArcGIS/rest/services/World_Shaded_Relief/MapServer/tile/{z}/{y}/{x}",
    maxNativeZoom: 13,
    attribution: "Tiles &copy; Esri",
  },
};

const OFFSET: Record<LabelSide, [number, number]> = {
  top: [0, -8],
  bottom: [0, 8],
  left: [-8, 0],
  right: [8, 0],
};

type Px = { x: number; y: number };

/** A line moved d pixels to the right of its direction of travel, its corners mitred */
function offsetLine(pts: Px[], d: number): [number, number][] {
  const normals = pts.slice(1).map((p, i) => {
    const dx = p.x - pts[i].x;
    const dy = p.y - pts[i].y;
    const len = Math.hypot(dx, dy) || 1;
    return [-dy / len, dx / len];
  });
  return pts.map((p, i) => {
    const a = normals[Math.max(0, i - 1)];
    const b = normals[Math.min(normals.length - 1, i)];
    let nx = a[0] + b[0];
    let ny = a[1] + b[1];
    const len = Math.hypot(nx, ny) || 1;
    nx /= len;
    ny /= len;
    const cos = Math.max(0.5, nx * b[0] + ny * b[1]);
    return [p.x + (nx * d) / cos, p.y + (ny * d) / cos];
  });
}

/** Where along a line, in pixels, to put its chevrons every `every` pixels, and its arrowhead at the end;
 * each with its heading in degrees clockwise from up */
function chevrons(pts: [number, number][], every: number): { at: [number, number]; angle: number; end?: boolean }[] {
  const heading = (a: [number, number], b: [number, number]) => (Math.atan2(b[0] - a[0], a[1] - b[1]) * 180) / Math.PI;
  const lengths = pts.slice(1).map((p, i) => Math.hypot(p[0] - pts[i][0], p[1] - pts[i][1]));
  const total = lengths.reduce((a, b) => a + b, 0);
  const out: { at: [number, number]; angle: number; end?: boolean }[] = [];
  // Spread evenly, none too near either end
  const count = Math.floor((total - 40) / every);
  const gap = count > 0 ? (total - 40) / (count + 1) : 0;
  let seg = 0;
  let done = 0;
  for (let k = 1; k <= count; k++) {
    const want = 20 + gap * k;
    while (seg < lengths.length - 1 && done + lengths[seg] < want) done += lengths[seg++];
    const t = lengths[seg] ? (want - done) / lengths[seg] : 0;
    const a = pts[seg];
    const b = pts[seg + 1];
    out.push({ at: [a[0] + (b[0] - a[0]) * t, a[1] + (b[1] - a[1]) * t], angle: heading(a, b) });
  }
  const n = pts.length;
  out.push({ at: pts[n - 1], angle: heading(pts[n - 2], pts[n - 1]), end: true });
  return out;
}

function escape(s: string): string {
  return s.replace(/[&<>"]/g, (c) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" })[c]!);
}

// A battle's mark is sized by the men engaged, against the largest battle of its campaign: by the square
// root, so a skirmish still shows beside a Borodino
const SMALLEST = 20;
const LARGEST = 44;
const markSize = (engaged: number, most: number) =>
  Math.round(SMALLEST + (LARGEST - SMALLEST) * Math.sqrt(Math.min(1, engaged / most)));

/** A battle's mark, as on an old atlas: two crossed light cavalry sabres, their curved blades solid and
 * tapering, with knuckle-bow guards, inked in burgundy for a battle with forces or a fainter sepia for one
 * still to come, and haloed in parchment so they stand off the lines under them */
export function swords(soon: boolean, size?: number): string {
  const ink = soon ? "#5e4d36" : "#5a101e";
  const dims = size ? ` width="${size}" height="${size}"` : "";
  // One sabre, point at the top left and hilt at the bottom right, in a light cavalry sabre's proportions:
  // a long slim blade with a gentle curve, tapering to its point, then a short grip, a thin stirrup guard
  // and a small pommel cap; the other is its mirror image
  const sabre = (colour: string, halo: number) =>
    `<path d="M2.6 2.6 Q12.8 7.1 17.75 16.65 L16.65 17.75 Q11.7 8.3 2.6 2.6 Z" fill="${colour}" stroke="${colour}" stroke-width="${halo || 0.3}" stroke-linejoin="round"/>` +
    `<path d="M15.8 18.6 L18.6 15.8 Q21.7 17.5 20.6 20.6" fill="none" stroke="${colour}" stroke-width="${1.05 + halo}" stroke-linecap="round" stroke-linejoin="round"/>` +
    `<path d="M17.2 17.2 L20 20" fill="none" stroke="${colour}" stroke-width="${2.05 + halo}" stroke-linecap="round"/>` +
    `<circle cx="20.3" cy="20.3" r="${1 + halo / 2}" fill="${colour}"/>`;
  const pair = (colour: string, halo: number) =>
    `<g>${sabre(colour, halo)}</g><g transform="matrix(-1 0 0 1 24 0)">${sabre(colour, halo)}</g>`;
  return `<svg viewBox="0 0 24 24"${dims} aria-hidden="true">${pair("#fbf6e9", 2.2)}${pair(ink, 0)}</svg>`;
}

const MONTHS: Record<string, string> = {
  January: "Jan", February: "Feb", March: "Mar", April: "Apr", May: "May", June: "Jun",
  July: "Jul", August: "Aug", September: "Sep", October: "Oct", November: "Nov", December: "Dec",
};

/** A battle's date, short enough for the map: "16–18 August 1812" as "16–18 Aug" */
function shortDate(date: string): string {
  return date
    .replace(/,?\s*\d{4}/g, "")
    .replace(/\b(January|February|March|April|May|June|July|August|September|October|November|December)\b/g, (m) => MONTHS[m])
    .trim();
}

export function hasCampaignMap(campaignId: string): boolean {
  return campaignId in campaignMaps;
}

/** Distance in km between two points, near enough at a campaign's scale */
function km(a: LatLng, b: LatLng): number {
  const cos = Math.cos(((a[0] + b[0]) / 2) * (Math.PI / 180));
  return Math.hypot((b[1] - a[1]) * 111.32 * cos, (b[0] - a[0]) * 110.57);
}

/** How near a route passes to a point, in km */
function kmFromRoute(at: LatLng, path: LatLng[]): number {
  const cos = Math.cos(at[0] * (Math.PI / 180));
  const xy = (p: LatLng): [number, number] => [(p[1] - at[1]) * 111.32 * cos, (p[0] - at[0]) * 110.57];
  let best = Infinity;
  for (let i = 0; i < path.length - 1; i++) {
    const [ax, ay] = xy(path[i]);
    const [bx, by] = xy(path[i + 1]);
    const dx = bx - ax;
    const dy = by - ay;
    const t = Math.max(0, Math.min(1, -(ax * dx + ay * dy) / (dx * dx + dy * dy || 1)));
    best = Math.min(best, Math.hypot(ax + dx * t, ay + dy * t));
  }
  return best;
}

/** The marches that led to a battle or away from it: those passing within 5 km of it, or, where none does,
 * the nearest within 50 km */
export function routesAt(campaignId: string, battleId: string): MapRoute[] {
  const data = campaignMaps[campaignId];
  const place = battlePlaces[battleId];
  if (!data || !place) return [];
  const near = data.routes.map((r) => ({ r, d: kmFromRoute(place.at, r.path) }));
  const close = near.filter((n) => n.d <= 5);
  if (close.length) return close.map((n) => n.r);
  const nearest = Math.min(...near.map((n) => n.d));
  return nearest <= 50 ? near.filter((n) => n.d <= nearest + 5).map((n) => n.r) : [];
}

/**
 * A campaign's map, or, given a battle to focus on, that battle's: centred on it and the country around
 * it, its sabres larger, the marches that led to it and away from it drawn full and the rest faded back
 */
export function CampaignMap({ campaignId, focus }: { campaignId: string; focus?: string }) {
  const data = campaignMaps[campaignId];
  const mapRef = useRef<Leaflet.Map | null>(null);
  const router = useRouter();
  const holder = useRef<HTMLDivElement>(null);
  const routeLayers = useRef<Map<string, Leaflet.LayerGroup>>(new Map());
  const [hidden, setHidden] = useState<Set<string>>(new Set());
  const [ready, setReady] = useState(false);

  useEffect(() => {
    if (!data || !holder.current) return;
    let map: Leaflet.Map | undefined;
    let resize: ResizeObserver | undefined;
    let cancelled = false;
    const layers = routeLayers.current;

    import("leaflet").then(({ default: L }) => {
      if (cancelled || !holder.current) return;
      const tiles = TILES[data.tiles ?? "physical"];
      // A battle's map opens no closer than its tiles' finest, so the land stays crisp; it can still be zoomed
      // in a step beyond
      map = L.map(holder.current, { scrollWheelZoom: false, zoomSnap: 0.25, maxZoom: tiles.maxNativeZoom + 1 });
      mapRef.current = map;
      const battles = scheduleIn(campaignId);
      const placed = battles.filter((b) => battlePlaces[b.id]);
      const focused = focus ? battlePlaces[focus] : undefined;
      const through = new Set(focus ? routesAt(campaignId, focus) : data.routes);
      // The view first, as Leaflet can't draw a line on a map with none: the battles, and the towns and
      // frontiers around them too where there's room
      const wide = holder.current.clientWidth >= 640;
      let points: LatLng[] = [
        ...placed.map((b) => battlePlaces[b.id].at),
        ...(wide ? data.places.map((p) => p.at) : []),
        ...data.routes.filter((r) => r.start).map((r) => r.path[0]),
      ];
      // For one battle, the country within reach of it: a fraction of the campaign's breadth, or more where
      // its nearest neighbour is further off; and whatever of its marches, battles and towns lie in that
      if (focused) {
        const lats = placed.map((b) => battlePlaces[b.id].at[0]);
        const lngs = placed.map((b) => battlePlaces[b.id].at[1]);
        const breadth = km([Math.min(...lats), Math.min(...lngs)], [Math.max(...lats), Math.max(...lngs)]);
        const others = placed.filter((b) => b.id !== focus).map((b) => km(focused.at, battlePlaces[b.id].at));
        const reach = Math.max(breadth * 0.15, Math.min(...others, Infinity) * 1.2, 8);
        const within = (p: LatLng) => km(focused.at, p) <= reach;
        const near = [
          ...[...through].flatMap((r) => r.path).filter(within),
          ...placed.map((b) => battlePlaces[b.id].at).filter(within),
        ];
        // Mirrored about the battle, so it sits in the middle of its map
        const [lat, lng] = focused.at;
        points = [focused.at, ...near, ...near.map(([a, b]): LatLng => [2 * lat - a, 2 * lng - b])];
      }      const bounds = L.latLngBounds(points);
      if (focused && points.length === 1) bounds.extend(L.latLng(focused.at[0] + 0.3, focused.at[1] + 0.5)).extend(L.latLng(focused.at[0] - 0.3, focused.at[1] - 0.5));
      let fitZoom = 0;
      const fit = () => {
        // Clear of the key over the map's foot, however many rows it runs to
        const key = holder.current?.parentElement?.querySelector<HTMLElement>(".map-legend");
        const foot = (key?.offsetHeight ?? 48) + 36;
        map!.fitBounds(bounds, {
          paddingTopLeft: [40, 24],
          paddingBottomRight: [24, foot],
          maxZoom: focus ? tiles.maxNativeZoom : undefined,
          animate: false,
        });
        fitZoom = map!.getZoom();
      };
      fit();
      // Fit again when its box settles or changes size (the page's layout, a turned phone), until it's
      // been moved by hand
      let moved = false;
      map.on("dragstart", () => (moved = true));
      holder.current.querySelector(".leaflet-control-zoom")?.addEventListener("click", () => (moved = true));
      resize = new ResizeObserver(() => {
        map!.invalidateSize({ animate: false });
        if (!moved) fit();
      });
      resize.observe(holder.current);
      // On a narrow map the whole theatre is too small for every name: until it's zoomed in, only the
      // battles with forces and the states keep theirs
      const sparse = () => {
        const narrow = map!.getSize().x < 640 && map!.getZoom() < fitZoom + 0.75;
        holder.current?.toggleAttribute("data-sparse", narrow);
      };
      sparse();
      map.on("zoomend resize", sparse);
      // Where names would overlap, the less important gives way: where the campaign's march begins first,
      // then the battles with forces, the battles still to come, the cities, and the towns last
      const RANK = ["map-label-focus", "map-label-start", "map-label-battle", "map-label-soon", "map-label-city", "map-label-town"];
      const declutter = () => {
        const labels = [...(holder.current?.querySelectorAll<HTMLElement>(".leaflet-tooltip.map-label") ?? [])];
        const rank = (el: HTMLElement) => RANK.findIndex((c) => el.classList.contains(c));
        labels.sort((a, b) => rank(a) - rank(b));
        const kept: DOMRect[] = [];
        const frame = holder.current?.getBoundingClientRect();
        for (const el of labels) {
          el.style.visibility = "";
          if (getComputedStyle(el).display === "none") continue;
          const r = el.getBoundingClientRect();
          // A name cut off by the map's edge gives way too, until the map is moved to show it
          const cut = !!frame && (r.left < frame.left || r.right > frame.right || r.top < frame.top || r.bottom > frame.bottom);
          if (cut || kept.some((k) => r.left < k.right && k.left < r.right && r.top < k.bottom && k.top < r.bottom)) {
            el.style.visibility = "hidden";
          } else kept.push(r);
        }
      };
      map.on("zoomend moveend resize", () => requestAnimationFrame(declutter));
      L.tileLayer(tiles.url, {
        maxNativeZoom: tiles.maxNativeZoom,
        maxZoom: tiles.maxNativeZoom + 1,
        attribution: tiles.attribution,
      }).addTo(map);

      // The frontiers of the time, in their own pane under the routes; the names of states, provinces and
      // seas under those
      map.createPane("borders").style.zIndex = "390";
      const regionPane = map.createPane("regions");
      regionPane.style.zIndex = "380";
      regionPane.style.pointerEvents = "none";
      const borderRenderer = L.svg({ pane: "borders" });
      for (const border of data.borders) {
        L.polyline(border, {
          renderer: borderRenderer,
          color: "#a62b3c",
          weight: 7,
          opacity: 0.16,
          lineJoin: "round",
          interactive: false,
        }).addTo(map);
        L.polyline(border, {
          renderer: borderRenderer,
          color: "#701626",
          weight: 1.6,
          opacity: 0.75,
          dashArray: "7 3 1.5 3",
          lineJoin: "round",
          interactive: false,
        }).addTo(map);
      }
      for (const region of data.regions) {
        L.marker(region.at, {
          pane: "regions",
          interactive: false,
          keyboard: false,
          icon: L.divIcon({
            className: `map-region map-region-${region.kind}`,
            iconSize: [0, 0],
            html: `<span>${escape(region.name)}</span>`,
          }),
        }).addTo(map);
      }

      const sideOf = new Map(data.sides.map((s) => [s.id, s]));
      const routeGroups = new Map<string, Leaflet.LayerGroup>();
      for (const side of data.sides) routeGroups.set(side.id, L.layerGroup().addTo(map));

      const routePopup = (r: MapRoute) =>
        `<div class="map-pop"><strong>${escape(r.name)}</strong><div class="map-pop-date">${escape(r.dates)}</div><p>${escape(r.note)}</p></div>`;

      // Each route is drawn once and laid out afresh at every zoom (layout, below)
      const drawn: {
        route: MapRoute;
        side: MapSide;
        lines: Leaflet.Polyline[];
        start: Leaflet.CircleMarker;
        marks: Leaflet.LayerGroup;
        main?: boolean;
      }[] = [];
      for (const route of data.routes) {
        const side = sideOf.get(route.side)!;
        const group = routeGroups.get(route.side)!;
        const lines: Leaflet.Polyline[] = [];
        // On a battle's map, only the marches that led to it and away from it, drawn as the main ones
        if (!through.has(route)) continue;
        const main = focus ? true : route.main;
        // A main army's march is drawn heavier, edged in parchment, so it can be followed through the rest
        if (main) {
          lines.push(
            L.polyline(route.path, {
              color: "#fbf6e9",
              weight: 8,
              opacity: 0.85,
              lineCap: "round",
              lineJoin: "round",
              interactive: false,
            }).addTo(group)
          );
        }
        lines.push(
          L.polyline(route.path, {
            color: side.colour,
            weight: main ? 4.5 : 3,
            opacity: main ? 0.95 : 0.85,
            dashArray: side.dash,
            lineCap: "round",
            lineJoin: "round",
            interactive: false,
          }).addTo(group)
        );
        // A wide clear line over each route, so it's easy to tap
        lines.push(
          L.polyline(route.path, { color: side.colour, weight: 14, opacity: 0, interactive: true })
            .bindPopup(routePopup(route))
            .addTo(group)
        );
        // Where it begins: a dot in the side's colour, named where the data names it
        const start = L.circleMarker(route.path[0], {
          radius: 4.5,
          color: "#fbf6e9",
          weight: 1.5,
          fillColor: side.colour,
          fillOpacity: 1,
          interactive: false,
        });
        if (route.start) {
          const at = route.startLabel ?? "right";
          // Beside the dot and a little below, clear of the line leaving it
          const below = at === "left" || at === "right" ? 12 : 0;
          start.bindTooltip(`<span style="color: ${side.colour}">${escape(route.start).replace(/\n/g, "<br>")}</span>`, {
            permanent: true,
            direction: at,
            offset: [OFFSET[at][0], OFFSET[at][1] + below],
            className: "map-label map-label-start",
          });
        }
        start.addTo(group);
        drawn.push({ route, side, lines, start, marks: L.layerGroup().addTo(group), main });
      }

      // Lay the routes out for the map's zoom. Each runs a few pixels to the right of its direction of travel
      // (further for a side given a wider lane), so an advance and a retreat along the same road, or two
      // armies on it, run side by side instead of on top of each other; and chevrons along it, at a steady
      // spacing on screen, show which way it went, with an arrowhead where it ends
      const layout = () => {
        for (const { route, side, lines, start, marks, main } of drawn) {
          const pts = offsetLine(
            route.path.map((p) => map!.latLngToLayerPoint(p)),
            side.lane ?? 3
          );
          const latlngs = pts.map((p) => map!.layerPointToLatLng(p));
          for (const line of lines) line.setLatLngs(latlngs);
          start.setLatLng(latlngs[0]);
          marks.clearLayers();
          for (const c of chevrons(pts, main ? 80 : 100)) {
            const end = c.end;
            const size = end ? 16 : 12;
            marks.addLayer(
              L.marker(map!.layerPointToLatLng(c.at), {
                interactive: false,
                keyboard: false,
                icon: L.divIcon({
                  className: "map-arrow",
                  iconSize: [size, size],
                  iconAnchor: [size / 2, size / 2],
                  // The head stops just short of where the route ends, clear of the battle or town there
                  html: end
                    ? `<svg width="16" height="16" viewBox="0 0 14 14" style="transform: rotate(${c.angle}deg) translateY(12px)"><path d="M7 1 L12.5 12 L7 9 L1.5 12 Z" fill="${side.colour}" stroke="#fbf6e9" stroke-width="1"/></svg>`
                    : `<svg width="12" height="12" viewBox="0 0 12 12" style="transform: rotate(${c.angle}deg)"><path d="M2.5 8.5 L6 4 L9.5 8.5" fill="none" stroke="#fbf6e9" stroke-width="4" stroke-linecap="round" stroke-linejoin="round"/><path d="M2.5 8.5 L6 4 L9.5 8.5" fill="none" stroke="${side.colour}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/></svg>`,
                }),
              })
            );
          }
        }
      };
      layout();
      map.on("zoomend viewreset", layout);
      layers.clear();
      routeGroups.forEach((g, id) => layers.set(id, g));

      // Towns, for bearings, the great cities larger; not those a battle or siege already marks
      for (const place of data.places) {
        if (placed.some((b) => km(battlePlaces[b.id].at, place.at) < 3)) continue;
        L.circleMarker(place.at, {
          radius: place.city ? 3.5 : 2.5,
          color: place.city ? "#fbf6e9" : "#4d3e2b",
          weight: place.city ? 1.5 : 1,
          fillColor: place.city ? "#33200f" : "#4d3e2b",
          fillOpacity: 1,
          interactive: false,
        })
          .bindTooltip(escape(place.name), {
            permanent: true,
            direction: place.label ?? "right",
            offset: OFFSET[place.label ?? "right"],
            className: place.city ? "map-label map-label-city" : "map-label map-label-town",
          })
          .addTo(map);
      }

      // Battles on top, those with forces above those still to come, and smaller marks above larger ones
      // so each can be pressed
      const ordered = [...placed.filter(isPlanned), ...placed.filter((b) => !isPlanned(b))];
      const most = Math.max(...placed.map((b) => battlePlaces[b.id].engaged));
      for (const battle of ordered) {
        const { at, engaged, label = "right", nudge = [0, 0] } = battlePlaces[battle.id];
        const soon = isPlanned(battle);
        // A battle's own map shows it larger than any other
        const size = battle.id === focus ? LARGEST + 6 : markSize(engaged, most);
        const marker = L.marker(at, {
          title: battle.name,
          alt: battle.name,
          riseOnHover: true,
          zIndexOffset: battle.id === focus ? 2000 : (soon ? 500 : 1000) + (LARGEST - size) * 5,
          icon: L.divIcon({
            className: `map-battle${soon ? " map-battle-soon" : ""}${!focus ? "" : battle.id === focus ? " map-battle-focus" : " map-faded"}`,
            iconSize: [size, size],
            iconAnchor: [size / 2, size / 2],
            tooltipAnchor: [0, 0],
            popupAnchor: [0, -size / 2],
            html: swords(soon),
          }),
        });
        // Its name, and beneath it when it was fought
        const gap = size / 2 + 3;
        const side: [number, number] = [Math.sign(OFFSET[label][0]) * gap, Math.sign(OFFSET[label][1]) * gap];
        marker.bindTooltip(
          `${escape(battle.name)}<span class="map-label-date">${escape(shortDate(battle.date))}</span>`,
          {
            permanent: true,
            direction: label,
            offset: [side[0] + nudge[0], side[1] + nudge[1]],
            className: `map-label ${battle.id === focus ? "map-label-focus" : soon ? "map-label-soon" : "map-label-battle"}${focus && battle.id !== focus ? " map-faded" : ""}`,
          }
        );
        const pop = document.createElement("div");
        pop.className = "map-pop";
        pop.innerHTML = `<strong>${escape(battle.name)}</strong><div class="map-pop-date">${escape(battle.date)}</div><div class="map-pop-engaged">About ${engaged.toLocaleString("en-GB")} men engaged</div><p>${escape(battle.summary)}</p>`;
        if (battle.id === focus) {
          // Already on its page
        } else if (soon) {
          pop.insertAdjacentHTML("beforeend", `<span class="map-pop-soon">Coming soon</span>`);
        } else {
          const link = document.createElement("a");
          const href = battleHref(battle);
          link.href = href;
          link.className = "map-pop-link";
          const n = battle.forces.length;
          link.textContent = `Open the ${n} ${n === 1 ? "force" : "forces"} →`;
          link.addEventListener("click", (e) => {
            if (e.metaKey || e.ctrlKey || e.shiftKey || e.button !== 0) return;
            e.preventDefault();
            router.push(href);
          });
          pop.appendChild(link);
        }
        marker.bindPopup(pop, { maxWidth: 280 });
        marker.addTo(map);
      }

      requestAnimationFrame(declutter);
      setReady(true);
    });

    return () => {
      cancelled = true;
      resize?.disconnect();
      map?.remove();
      mapRef.current = null;
      layers.clear();
    };
  }, [campaignId, focus, data, router]);

  // Show or hide a side's routes from the key
  useEffect(() => {
    const map = mapRef.current;
    if (!map) return;
    routeLayers.current.forEach((group, id) => {
      if (hidden.has(id)) group.remove();
      else {
        // Its lines in the order they were drawn, the parchment edge under the colour
        group.addTo(map);
        group.eachLayer((l) => (l as Leaflet.Path).bringToFront?.());
      }
    });
  }, [hidden, ready]);

  if (!data) return null;
  // On a battle's map, only the sides that have a march on it
  const shown = focus ? new Set(routesAt(campaignId, focus).map((r) => r.side)) : undefined;
  const keySides = shown ? data.sides.filter((side) => shown.has(side.id)) : data.sides;
  const toggle = (id: string) =>
    setHidden((h) => {
      const next = new Set(h);
      if (next.has(id)) next.delete(id);
      else next.add(id);
      return next;
    });

  return (
    <div className="campaign-map">
      <div ref={holder} className="campaign-map-canvas" aria-label={`Map of ${data.theatre}`} role="region">
        {!ready && (
          <Text p="md" c="dimmed">
            Loading map…
          </Text>
        )}
      </div>
      <div className="map-legend" aria-label="Map key">
        {keySides.map((side) => (
          <UnstyledButton
            key={side.id}
            className="map-key"
            aria-pressed={!hidden.has(side.id)}
            title={`${hidden.has(side.id) ? "Show" : "Hide"} ${side.label.toLowerCase()}'s routes`}
            onClick={() => toggle(side.id)}
          >
            <svg width="26" height="8" aria-hidden="true">
              <line
                x1="2"
                y1="4"
                x2="24"
                y2="4"
                stroke={side.colour}
                strokeWidth="3"
                strokeDasharray={side.dash}
                strokeLinecap="round"
              />
            </svg>
            <span>{side.label}</span>
          </UnstyledButton>
        ))}
        <span className="map-key map-key-static">
          <span className="map-key-icon" dangerouslySetInnerHTML={{ __html: swords(false, 16) }} />
          <span>Battle with forces</span>
        </span>
        <span className="map-key map-key-static">
          <span className="map-key-icon" dangerouslySetInnerHTML={{ __html: swords(true, 13) }} />
          <span>Coming soon</span>
        </span>
        <span className="map-key map-key-static" title="Each battle's mark is sized by the men engaged">
          <span className="map-key-scale" aria-hidden="true">
            <span dangerouslySetInnerHTML={{ __html: swords(false, 10) }} />
            <span dangerouslySetInnerHTML={{ __html: swords(false, 18) }} />
          </span>
          <span>Size: men engaged</span>
        </span>
      </div>
    </div>
  );
}
