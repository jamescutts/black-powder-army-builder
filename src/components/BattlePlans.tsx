"use client";

import "leaflet/dist/leaflet.css";
import { useEffect, useRef, useState } from "react";
import type * as Leaflet from "leaflet";
import { ActionIcon, Anchor, SegmentedControl, Stack, Text, Title, Tooltip } from "@mantine/core";
import { IconArrowsMaximize, IconArrowsMinimize } from "@tabler/icons-react";
import { battlePlans, type BattlePlan } from "@/data/battles/plans";

// A battle's period maps, each a scan that pans and zooms like a map: Leaflet with no geography (CRS.Simple),
// the scan laid over its own pixels. It opens on the map itself, cropped of its margins, on a light copy, and
// swaps in the full scan once zoomed in past that copy's detail.

/** Leaflet's bounds for a box of the scan's pixels: y runs down the scan, so it's negated as latitude */
function box(L: typeof Leaflet, [left, top, right, bottom]: [number, number, number, number]): Leaflet.LatLngBounds {
  return L.latLngBounds([-bottom, left], [-top, right]);
}

function PlanViewer({ plan }: { plan: BattlePlan }) {
  const frame = useRef<HTMLDivElement>(null);
  const holder = useRef<HTMLDivElement>(null);
  const [ready, setReady] = useState(false);
  const [full, setFull] = useState(false);
  const [detail, setDetail] = useState(false);

  useEffect(() => {
    if (!holder.current) return;
    let map: Leaflet.Map | undefined;
    let resize: ResizeObserver | undefined;
    let cancelled = false;
    setReady(false);
    setDetail(false);

    import("leaflet").then(({ default: L }) => {
      if (cancelled || !holder.current) return;
      const whole = box(L, [0, 0, plan.width, plan.height]);
      const crop = plan.crop ? box(L, plan.crop) : whole;
      // Zoom 0 shows the full scan at its own size; one step beyond doubles it
      map = L.map(holder.current, {
        crs: L.CRS.Simple,
        zoomSnap: 0.25,
        zoomDelta: 0.5,
        wheelPxPerZoomLevel: 120,
        maxZoom: 1,
        scrollWheelZoom: false,
        attributionControl: false,
        maxBounds: crop.pad(0.08),
        maxBoundsViscosity: 0.9,
      });
      // A scan that sits askew on its page is drawn turned, as an image inside an SVG laid over the scan's own
      // pixels, so it pans and zooms like any other; the crop is then of the scan as turned
      const scan = (src: string) => {
        if (!plan.rotate) return L.imageOverlay(src, whole, { alt: plan.title });
        const NS = "http://www.w3.org/2000/svg";
        const svg = document.createElementNS(NS, "svg");
        svg.setAttribute("viewBox", `0 0 ${plan.width} ${plan.height}`);
        svg.setAttribute("preserveAspectRatio", "none");
        const image = document.createElementNS(NS, "image");
        image.setAttribute("href", src);
        image.setAttribute("width", String(plan.width));
        image.setAttribute("height", String(plan.height));
        image.setAttribute("preserveAspectRatio", "none");
        image.setAttribute("transform", `rotate(${-plan.rotate} ${plan.width / 2} ${plan.height / 2})`);
        svg.appendChild(image);
        return L.svgOverlay(svg, whole, { interactive: false });
      };
      scan(plan.preview.src).addTo(map);
      // Everything outside the crop (binding, margins, blank paper) painted over in the frame's colour, above
      // the scans in their own pane
      const mask = map.createPane("mask");
      mask.style.zIndex = "450";
      const far = whole.pad(4);
      const ring = (b: Leaflet.LatLngBounds) => [b.getNorthWest(), b.getNorthEast(), b.getSouthEast(), b.getSouthWest()];
      if (plan.crop)
        L.polygon([ring(far), ring(crop)], { pane: "mask", stroke: false, fillColor: "#e9dfc8", fillOpacity: 1, interactive: false }).addTo(map);
      // Fitted to the crop, and fitted again as the box settles or resizes, until the reader moves it
      let touched = false;
      const fit = () => {
        if (!map) return;
        map.invalidateSize();
        // Leaflet clamps a fit to the minimum zoom, which is 0 (the full scan's own size) until set
        map.setMinZoom(-8);
        const zoom = map.getBoundsZoom(crop);
        map.setMinZoom(zoom - 0.5);
        if (!touched) map.fitBounds(crop, { animate: false });
      };
      fit();
      map.on("dragstart", () => (touched = true));
      holder.current.addEventListener("wheel", () => (touched = true), { passive: true });
      holder.current.addEventListener("pointerdown", () => (touched = true));

      // The full scan, once the light copy is enlarged past its own pixels
      const previewNative = Math.log2(plan.preview.width / plan.width);
      let loaded = false;
      map.on("zoomend", () => {
        if (loaded || !map || map.getZoom() <= previewNative + 0.25) return;
        loaded = true;
        scan(plan.src).addTo(map);
        setDetail(true);
      });

      // The wheel zooms only once the map's been clicked, so the page still scrolls past it
      map.on("click focus", () => map?.scrollWheelZoom.enable());
      map.on("mouseout blur", () => map?.scrollWheelZoom.disable());

      resize = new ResizeObserver(fit);
      resize.observe(holder.current);
      setReady(true);
    });

    return () => {
      cancelled = true;
      resize?.disconnect();
      map?.remove();
    };
  }, [plan]);

  useEffect(() => {
    const change = () => setFull(document.fullscreenElement === frame.current);
    document.addEventListener("fullscreenchange", change);
    return () => document.removeEventListener("fullscreenchange", change);
  }, []);

  const toggleFull = () => {
    if (document.fullscreenElement) document.exitFullscreen();
    else frame.current?.requestFullscreen?.();
  };

  return (
    <div ref={frame} className="battle-plan" data-full={full || undefined}>
      <div ref={holder} className="battle-plan-canvas" role="region" aria-label={`${plan.title}, a map that pans and zooms`}>
        {!ready && (
          <Text p="md" c="dimmed">
            Loading map…
          </Text>
        )}
      </div>
      <Tooltip label={full ? "Leave full screen" : "Full screen"} position="left">
        <ActionIcon className="battle-plan-full" variant="default" size="lg" onClick={toggleFull} aria-label={full ? "Leave full screen" : "Full screen"}>
          {full ? <IconArrowsMinimize size={18} /> : <IconArrowsMaximize size={18} />}
        </ActionIcon>
      </Tooltip>
      {detail && <span className="battle-plan-detail">Full scan</span>}
    </div>
  );
}

/** A battle's period maps, with a tab for each where there's more than one, and its maker, source and licence */
export function BattlePlans({ battleId, name }: { battleId: string; name: string }) {
  const plans = battlePlans[battleId];
  const [index, setIndex] = useState(0);
  if (!plans?.length) return null;
  const plan = plans[index];
  return (
    <Stack gap="xs" component="section" id="plans" mt="md">
      <Title order={2} className="builder-heading">
        Maps of the battle
      </Title>
      <Text size="sm" c="brown.9">
        {plans.length > 1 ? `${name} as mapmakers of the time and after drew it.` : `${name} as a mapmaker drew it.`} Drag to pan, and
        zoom with the buttons, a pinch, or the wheel once you&apos;ve clicked the map.
      </Text>
      {plans.length > 1 && (
        <SegmentedControl
          value={String(index)}
          onChange={(v) => setIndex(Number(v))}
          data={plans.map((p, i) => ({ value: String(i), label: p.label }))}
          style={{ alignSelf: "flex-start", maxWidth: "100%" }}
        />
      )}
      <PlanViewer plan={plan} />
      <Text size="sm" c="brown.9">
        <Text span fw={600} fs="italic">
          {plan.title}
        </Text>
        {` · ${plan.maker}, ${plan.date} · ${plan.collection} · `}
        <Anchor href={plan.page} target="_blank" rel="noopener noreferrer" size="sm">
          {plan.licence}, {plan.page.includes("commons.wikimedia.org") ? "on Wikimedia Commons" : "at the collection"}
        </Anchor>
      </Text>
      {plan.note && (
        <Text size="sm" c="dimmed">
          {plan.note}
        </Text>
      )}
    </Stack>
  );
}
