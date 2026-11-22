"use client";

import "leaflet/dist/leaflet.css";
import { useEffect, useRef, useState } from "react";
import { useRouter } from "next/navigation";
import type * as Leaflet from "leaflet";
import { Text, UnstyledButton } from "@mantine/core";
import { isPlanned, scheduleIn } from "@/data/battles";
import { battlePlaces, campaignMaps, type LabelSide, type LatLng, type MapRoute } from "@/data/battles/geo";
import { battleHref } from "@/lib/forces";

// A campaign's theatre on a map, as on Fleet Ledger's war pages: each battle a marked, labelled point
// (those with forces open their page; those still to come are paler), and the armies' main movements as
// arrowed lines, coloured and dashed by side. Leaflet over Esri's physical basemap, which needs no key.

// Relief and land cover only: no roads, borders or modern names, so with a sepia wash it reads as an old atlas
const TILES = "https://server.arcgisonline.com/ArcGIS/rest/services/World_Physical_Map/MapServer/tile/{z}/{y}/{x}";

const OFFSET: Record<LabelSide, [number, number]> = {
  top: [0, -8],
  bottom: [0, 8],
  left: [-8, 0],
  right: [8, 0],
};

/** The bearing of a segment on a Web Mercator map, in degrees clockwise from north */
function bearing(from: LatLng, to: LatLng): number {
  const y = (lat: number) => Math.log(Math.tan(Math.PI / 4 + (lat * Math.PI) / 360));
  return (Math.atan2(((to[1] - from[1]) * Math.PI) / 180, y(to[0]) - y(from[0])) * 180) / Math.PI;
}

function escape(s: string): string {
  return s.replace(/[&<>"]/g, (c) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" })[c]!);
}

const BATTLE_SIZE = 30;
const SOON_SIZE = 23;

/** A battle's mark, as on an old atlas: two crossed sabres in ink, haloed in parchment so they stand off
 * the lines under them; burgundy for a battle with forces, a fainter sepia for one still to come */
export function swords(soon: boolean, size?: number): string {
  const ink = soon ? "#5e4d36" : "#5a101e";
  const dims = size ? ` width="${size}" height="${size}"` : "";
  const blades = "M4 3.5 Q8.6 6.6 15.2 15.2 M20 3.5 Q15.4 6.6 8.8 15.2";
  const guards = "M13 17.4 L17.4 13 M6.6 13 L11 17.4";
  const grips = "M15.2 15.2 L18.4 18.4 M8.8 15.2 L5.6 18.4";
  const sabres = (stroke: string, extra: number) =>
    `<g fill="none" stroke="${stroke}" stroke-linecap="round" stroke-linejoin="round">` +
    `<path d="${blades}" stroke-width="${1.9 + extra}"/>` +
    `<path d="${guards}" stroke-width="${1.6 + extra}"/>` +
    `<path d="${grips}" stroke-width="${2.4 + extra}"/></g>` +
    `<g fill="${stroke}"><circle cx="19.2" cy="19.2" r="${1.4 + extra / 2}"/><circle cx="4.8" cy="19.2" r="${1.4 + extra / 2}"/></g>`;
  return `<svg viewBox="0 0 24 24"${dims} aria-hidden="true">${sabres("#fbf6e9", 2.6)}${sabres(ink, 0)}</svg>`;
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

export function CampaignMap({ campaignId }: { campaignId: string }) {
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
      map = L.map(holder.current, { scrollWheelZoom: false, zoomSnap: 0.25 });
      mapRef.current = map;
      const battles = scheduleIn(campaignId);
      const placed = battles.filter((b) => battlePlaces[b.id]);
      // The view first, as Leaflet can't draw a line on a map with none: the battles, and the towns and
      // frontiers around them too where there's room
      const wide = holder.current.clientWidth >= 640;
      const points: LatLng[] = [
        ...placed.map((b) => battlePlaces[b.id].at),
        ...(wide ? data.places.map((p) => p.at) : []),
        ...data.routes.filter((r) => r.start).map((r) => r.path[0]),
      ];
      const bounds = L.latLngBounds(points);
      let fitZoom = 0;
      const fit = () => {
        map!.fitBounds(bounds, { paddingTopLeft: [40, 24], paddingBottomRight: [24, 72], animate: false });
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
      // then the battles with forces, the cities, the battles still to come, and the towns last
      const RANK = ["map-label-start", "map-label-battle", "map-label-city", "map-label-soon", "map-label-town"];
      const declutter = () => {
        const labels = [...(holder.current?.querySelectorAll<HTMLElement>(".leaflet-tooltip.map-label") ?? [])];
        const rank = (el: HTMLElement) => RANK.findIndex((c) => el.classList.contains(c));
        labels.sort((a, b) => rank(a) - rank(b));
        const kept: DOMRect[] = [];
        for (const el of labels) {
          el.style.visibility = "";
          if (getComputedStyle(el).display === "none") continue;
          const r = el.getBoundingClientRect();
          if (kept.some((k) => r.left < k.right && k.left < r.right && r.top < k.bottom && k.top < r.bottom)) {
            el.style.visibility = "hidden";
          } else kept.push(r);
        }
      };
      map.on("zoomend resize", () => requestAnimationFrame(declutter));
      L.tileLayer(TILES, {
        maxNativeZoom: 8,
        maxZoom: 9,
        attribution: "Tiles &copy; Esri, US National Park Service",
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

      for (const route of data.routes) {
        const side = sideOf.get(route.side)!;
        const group = routeGroups.get(route.side)!;
        // A wide clear line under each route, so it's easy to tap
        L.polyline(route.path, { color: side.colour, weight: 14, opacity: 0, interactive: true })
          .bindPopup(routePopup(route))
          .addTo(group);
        L.polyline(route.path, {
          color: side.colour,
          weight: 3,
          opacity: 0.85,
          dashArray: side.dash,
          lineCap: "round",
          lineJoin: "round",
          interactive: false,
        }).addTo(group);
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
          start.bindTooltip(escape(route.start).replace(/\n/g, "<br>"), {
            permanent: true,
            direction: at,
            offset: [OFFSET[at][0], OFFSET[at][1] + below],
            className: "map-label map-label-start",
          });
        }
        start.addTo(group);
        const end = route.path[route.path.length - 1];
        const before = route.path[route.path.length - 2];
        // Its head stops just short of where the route ends, clear of the battle or town there
        L.marker(end, {
          interactive: false,
          keyboard: false,
          icon: L.divIcon({
            className: "map-arrow",
            iconSize: [16, 16],
            iconAnchor: [8, 8],
            html: `<svg width="16" height="16" viewBox="0 0 14 14" style="transform: rotate(${bearing(before, end)}deg) translateY(12px)"><path d="M7 1 L12.5 12 L7 9 L1.5 12 Z" fill="${side.colour}" stroke="#fbf6e9" stroke-width="1"/></svg>`,
          }),
        }).addTo(group);
      }
      layers.clear();
      routeGroups.forEach((g, id) => layers.set(id, g));

      // Towns, for bearings, the great cities larger
      for (const place of data.places) {
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

      // Battles on top, those with forces above those still to come
      const ordered = [...placed.filter(isPlanned), ...placed.filter((b) => !isPlanned(b))];
      for (const battle of ordered) {
        const { at, label = "right", nudge = [0, 0] } = battlePlaces[battle.id];
        const soon = isPlanned(battle);
        // Crossed swords on a disc: bold for a battle with forces, pale and smaller for one still to come
        const size = soon ? SOON_SIZE : BATTLE_SIZE;
        const marker = L.marker(at, {
          title: battle.name,
          alt: battle.name,
          riseOnHover: true,
          zIndexOffset: soon ? 500 : 1000,
          icon: L.divIcon({
            className: soon ? "map-battle map-battle-soon" : "map-battle",
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
            className: soon ? "map-label map-label-soon" : "map-label map-label-battle",
          }
        );
        const pop = document.createElement("div");
        pop.className = "map-pop";
        pop.innerHTML = `<strong>${escape(battle.name)}</strong><div class="map-pop-date">${escape(battle.date)}</div><p>${escape(battle.summary)}</p>`;
        if (soon) {
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
  }, [campaignId, data, router]);

  // Show or hide a side's routes from the key
  useEffect(() => {
    const map = mapRef.current;
    if (!map) return;
    routeLayers.current.forEach((group, id) => {
      if (hidden.has(id)) group.remove();
      else {
        // Back under the battles and towns, where it was drawn
        group.addTo(map);
        group.eachLayer((l) => (l as Leaflet.Path).bringToBack?.());
      }
    });
  }, [hidden, ready]);

  if (!data) return null;
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
        {data.sides.map((side) => (
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
      </div>
    </div>
  );
}
