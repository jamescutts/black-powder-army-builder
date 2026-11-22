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
    let cancelled = false;
    const layers = routeLayers.current;

    import("leaflet").then(({ default: L }) => {
      if (cancelled || !holder.current) return;
      map = L.map(holder.current, { scrollWheelZoom: false, zoomSnap: 0.25 });
      mapRef.current = map;
      const battles = scheduleIn(campaignId);
      const placed = battles.filter((b) => battlePlaces[b.id]);
      // The view first: Leaflet can't draw a line on a map with none
      const points: LatLng[] = [...placed.map((b) => battlePlaces[b.id].at), ...data.places.map((p) => p.at)];
      map.fitBounds(L.latLngBounds(points), { paddingTopLeft: [24, 24], paddingBottomRight: [24, 56] });
      // On a narrow map the whole theatre is too small for every name: until it's zoomed in, only the
      // battles with forces keep theirs
      const fitZoom = map.getZoom();
      const sparse = () => {
        const narrow = map!.getSize().x < 640 && map!.getZoom() < fitZoom + 0.75;
        holder.current?.toggleAttribute("data-sparse", narrow);
      };
      sparse();
      map.on("zoomend resize", sparse);
      L.tileLayer(TILES, {
        maxNativeZoom: 8,
        maxZoom: 9,
        attribution: "Tiles &copy; Esri, US National Park Service",
      }).addTo(map);

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

      // Towns, for bearings
      for (const place of data.places) {
        L.circleMarker(place.at, {
          radius: 2.5,
          color: "#4d3e2b",
          weight: 1,
          fillColor: "#4d3e2b",
          fillOpacity: 1,
          interactive: false,
        })
          .bindTooltip(escape(place.name), {
            permanent: true,
            direction: place.label ?? "right",
            offset: OFFSET[place.label ?? "right"],
            className: "map-label map-label-town",
          })
          .addTo(map);
      }

      // Battles on top, those with forces above those still to come
      const ordered = [...placed.filter(isPlanned), ...placed.filter((b) => !isPlanned(b))];
      for (const battle of ordered) {
        const { at, label = "right", nudge = [0, 0] } = battlePlaces[battle.id];
        const soon = isPlanned(battle);
        const marker = L.circleMarker(at, {
          radius: soon ? 5 : 7,
          color: soon ? "#7d6a4c" : "#fbf6e9",
          weight: 2,
          fillColor: soon ? "#efe8d8" : "#701626",
          fillOpacity: 1,
          className: soon ? "map-battle map-battle-soon" : "map-battle",
        });
        marker.bindTooltip(escape(battle.name), {
          permanent: true,
          direction: label,
          offset: [OFFSET[label][0] + nudge[0], OFFSET[label][1] + nudge[1]],
          className: soon ? "map-label map-label-soon" : "map-label map-label-battle",
        });
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

      setReady(true);
    });

    return () => {
      cancelled = true;
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
          <span className="map-key-dot" aria-hidden="true" />
          <span>Battle with forces</span>
        </span>
        <span className="map-key map-key-static">
          <span className="map-key-dot map-key-dot-soon" aria-hidden="true" />
          <span>Coming soon</span>
        </span>
      </div>
    </div>
  );
}
