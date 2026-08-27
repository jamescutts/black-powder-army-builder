"use client";

import { useRef, useState } from "react";
import { Alert, Badge, Button, Divider, Group, List, Modal, Stack, Table, Text, Title } from "@mantine/core";
import { IconAlertTriangle, IconDownload, IconEye, IconPrinter } from "@tabler/icons-react";
import { useDisclosure } from "@mantine/hooks";
import type { Nation, UnitEntry } from "@/data/types";
import type { RosterState, RosterUnitLine } from "@/types/army";
import { unitCost, unitStatLine } from "@/lib/units";
import { getSupplement } from "@/data";
import { validateRoster } from "@/lib/validate";

interface Props {
  nation: Nation;
  roster: RosterState;
}

function getStaffRating(unit: UnitEntry, variantLabel?: string): number | undefined {
  if (unit.staffRating !== undefined) return unit.staffRating;
  if (variantLabel && unit.variants) {
    const variant = unit.variants.find((v) => v.label === variantLabel);
    if (variant?.staffRating !== undefined) return variant.staffRating;
  }
  return undefined;
}

function lineTotal(nation: Nation, line: RosterUnitLine): number {
  const unit = nation.units.find((u) => u.id === line.unitId);
  if (!unit) return 0;
  return unitCost(unit, line.variantLabel) * line.qty;
}

function UnitRow({ nation, line }: { nation: Nation; line: RosterUnitLine }) {
  const unit = nation.units.find((u) => u.id === line.unitId);
  if (!unit) return null;
  const sr = unit.category === "Command" ? getStaffRating(unit, line.variantLabel) : undefined;
  const stats = unitStatLine(unit);
  const cost = lineTotal(nation, line);

  return (
    <Table.Tr>
      <Table.Td>
        <Group gap={6} wrap="nowrap" align="center">
          <span>
            {line.qty > 1 ? `${line.qty}× ` : ""}
            {unit.name}
          </span>
          {sr !== undefined && (
            <Badge size="sm" variant="light" color="brown">Staff Rating {sr}</Badge>
          )}
        </Group>
      </Table.Td>
      <Table.Td>{unit.type}</Table.Td>
      <Table.Td>{stats || "\u2014"}</Table.Td>
      <Table.Td>{unit.special?.join(", ") || "\u2014"}</Table.Td>
      <Table.Td style={{ textAlign: "right" }}>{cost}</Table.Td>
    </Table.Tr>
  );
}

function RosterContent({ nation, roster }: Props) {
  const commandTotal = roster.commandItems.reduce((s, l) => s + lineTotal(nation, l), 0);

  const brigadeTotals = roster.brigadeInstances.map((instance) => {
    const bt = nation.brigades.find((b) => b.id === instance.brigadeTypeId);
    const commanderCost = instance.commanderLine ? lineTotal(nation, instance.commanderLine) : 0;
    const total =
      commanderCost + instance.slotLines.flat().reduce((s, l) => s + lineTotal(nation, l), 0);
    return { instance, bt, total };
  });

  const grandTotal = commandTotal + brigadeTotals.reduce((s, b) => s + b.total, 0);
  const supplement = getSupplement(nation.supplementId);

  return (
    <Stack gap="md">
      <Group justify="space-between" align="center">
        <Group gap="sm" align="center">
          {nation.flagFile && (
            <div style={{
              position: "relative",
              width: 54,
              height: 36,
              borderRadius: 3,
              border: "1px solid var(--mantine-color-gray-3)",
              overflow: "hidden",
              flexShrink: 0,
            }}>
              <img
                src={nation.flagFile}
                alt={`${nation.name} flag`}
                style={{ width: "100%", height: "100%", objectFit: "cover", display: "block" }}
              />
              <div style={{
                position: "absolute",
                inset: 0,
                background: [
                  "radial-gradient(ellipse at center, transparent 40%, rgba(60,30,5,0.35) 100%)",
                  "linear-gradient(135deg, rgba(180,130,60,0.18) 0%, rgba(120,70,20,0.22) 100%)",
                ].join(", "),
                mixBlendMode: "multiply",
                pointerEvents: "none",
              }} data-flag-overlay />
            </div>
          )}
          <Stack gap={0}>
            <Title order={3}>{nation.name}</Title>
            <Text size="sm" c="dimmed">
              {supplement?.name ? `${supplement.name} \u2014 ` : ""}
              {roster.brigadeInstances.length} brigade
              {roster.brigadeInstances.length === 1 ? "" : "s"}
            </Text>
          </Stack>
        </Group>
        <Badge size="xl" variant="filled" color="brown">
          {grandTotal} pts
        </Badge>
      </Group>

      {(() => {
        const issues = validateRoster(nation, roster);
        if (issues.length === 0) return null;
        return (
          <Alert color="red" variant="light" icon={<IconAlertTriangle />} title="Roster issues">
            <List size="sm" spacing={4}>
              {issues.map((issue, idx) => (
                <List.Item key={idx}>{issue.message}</List.Item>
              ))}
            </List>
          </Alert>
        );
      })()}

      {roster.commandItems.length > 0 && (
        <>
          <Title order={4} c="brown.7" mt="sm" style={{ fontFamily: "var(--font-heading), serif" }}>
            Army Command
          </Title>
          <Stack gap="xs">
            {roster.commandItems.map((line) => {
              const unit = nation.units.find((u) => u.id === line.unitId);
              if (!unit) return null;
              const sr = getStaffRating(unit, line.variantLabel);
              const cost = lineTotal(nation, line);
              return (
                <Group gap="sm" align="center" wrap="nowrap" key={line.key}
                  style={{ padding: "8px 12px", border: "1px solid var(--mantine-color-gray-3)", borderRadius: 6 }}
                >
                  {sr !== undefined && (
                    <Group gap={8} align="center" wrap="nowrap" data-staff-rating style={{
                      flexShrink: 0,
                      padding: "6px 10px",
                      borderRadius: 6,
                      backgroundColor: "var(--mantine-color-brown-light)",
                    }}>
                      <Stack gap={0}>
                        <Text size="10px" c="dark" fw={600} tt="uppercase" lh={1}>Staff</Text>
                        <Text size="10px" c="dark" fw={600} tt="uppercase" lh={1}>Rating</Text>
                      </Stack>
                      <Text size="xl" fw={700} c="dark" lh={1}>{sr}</Text>
                    </Group>
                  )}
                  <Stack gap={2} style={{ flex: 1, minWidth: 0 }}>
                    <Text fw={600} size="sm">{unit.name}</Text>
                    {unit.special && unit.special.length > 0 && (
                      <Text size="xs" c="dimmed">{unit.special.join(", ")}</Text>
                    )}
                  </Stack>
                  <Text fw={700} size="sm" style={{ whiteSpace: "nowrap", flexShrink: 0 }}>{cost} pts</Text>
                </Group>
              );
            })}
          </Stack>
        </>
      )}

      {brigadeTotals.map(({ instance, bt, total }) => {
        if (!bt) return null;
        const unitLines = instance.slotLines.flat();
        const commanderLine = instance.commanderLine;
        const commanderUnit = commanderLine
          ? nation.units.find((u) => u.id === commanderLine.unitId)
          : undefined;
        const commanderSr = commanderUnit && commanderLine
          ? getStaffRating(commanderUnit, commanderLine.variantLabel)
          : undefined;
        const commanderCost = commanderLine ? lineTotal(nation, commanderLine) : 0;

        return (
          <div key={instance.key}>
            <Group justify="space-between" align="baseline" mt="sm">
              <Title order={4} c="brown.7" style={{ fontFamily: "var(--font-heading), serif" }}>
                {bt.name}
              </Title>
              <Text size="sm" c="dimmed">{total} pts</Text>
            </Group>

            {commanderUnit && commanderLine && (
              <Group gap="sm" align="center" wrap="nowrap" style={{ padding: "6px 0" }}>
                {commanderSr !== undefined && (
                  <Group gap={6} align="center" wrap="nowrap" data-staff-rating style={{
                    flexShrink: 0,
                    padding: "4px 8px",
                    borderRadius: 6,
                    backgroundColor: "var(--mantine-color-brown-light)",
                  }}>
                    <Stack gap={0}>
                      <Text size="9px" c="dark" fw={600} tt="uppercase" lh={1}>Staff</Text>
                      <Text size="9px" c="dark" fw={600} tt="uppercase" lh={1}>Rating</Text>
                    </Stack>
                    <Text size="lg" fw={700} c="dark" lh={1}>{commanderSr}</Text>
                  </Group>
                )}
                <Text fw={600} size="sm" style={{ flex: 1, minWidth: 0 }}>
                  {commanderUnit.name}
                </Text>
                <Text fw={600} size="sm" c="dimmed" style={{ whiteSpace: "nowrap", flexShrink: 0 }}>
                  {commanderCost} pts
                </Text>
              </Group>
            )}

            {unitLines.length > 0 && (
            <Table verticalSpacing={4} fz="xs" layout="fixed">
              <colgroup>
                <col style={{ width: "22%" }} />
                <col style={{ width: "14%" }} />
                <col style={{ width: "16%" }} />
                <col style={{ width: "40%" }} />
                <col style={{ width: "8%" }} />
              </colgroup>
              <Table.Thead>
                <Table.Tr>
                  <Table.Th>Unit</Table.Th>
                  <Table.Th>Type</Table.Th>
                  <Table.Th>Stats</Table.Th>
                  <Table.Th>Special</Table.Th>
                  <Table.Th style={{ textAlign: "right" }}>Pts</Table.Th>
                </Table.Tr>
              </Table.Thead>
              <Table.Tbody>
                {unitLines.map((line) => (
                  <UnitRow key={line.key} nation={nation} line={line} />
                ))}
              </Table.Tbody>
            </Table>
            )}
          </div>
        );
      })}

      <Divider />
      <Group justify="flex-end">
        <Text fw={700} size="lg">
          Total: {grandTotal} pts
        </Text>
      </Group>

      {nation.notes.length > 0 && (
        <>
          <Title order={4} c="brown.7" mt="sm" style={{ fontFamily: "var(--font-heading), serif" }}>
            Army Notes
          </Title>
          <List size="xs" spacing={4}>
            {nation.notes.map((note, i) => (
              <List.Item key={i}>{note}</List.Item>
            ))}
          </List>
        </>
      )}
    </Stack>
  );
}

export function RosterViewModal({ nation, roster }: Props) {
  const [opened, { open, close }] = useDisclosure(false);
  const contentRef = useRef<HTMLDivElement>(null);

  function handlePrint() {
    if (!opened) {
      open();
      setTimeout(() => window.print(), 300);
    } else {
      window.print();
    }
  }

  const [pdfLoading, setPdfLoading] = useState(false);

  async function handleDownloadPdf() {
    setPdfLoading(true);

    // Ensure modal is open so contentRef is in the DOM
    if (!opened) {
      open();
      // Wait for modal to render
      await new Promise((r) => setTimeout(r, 400));
    }

    const el = contentRef.current;
    if (!el) {
      setPdfLoading(false);
      return;
    }

    try {
      const html2canvas = (await import("html2canvas-pro")).default;
      const { jsPDF } = await import("jspdf");

      // Convert SVG img elements to inline data URIs so html2canvas can render them
      const images = el.querySelectorAll("img");
      const originals: { img: HTMLImageElement; src: string }[] = [];
      await Promise.all(
        Array.from(images).map(async (img) => {
          if (!img.src.endsWith(".svg")) return;
          try {
            const resp = await fetch(img.src);
            const svgText = await resp.text();
            const dataUri = `data:image/svg+xml;base64,${btoa(unescape(encodeURIComponent(svgText)))}`;
            originals.push({ img, src: img.src });
            img.src = dataUri;
          } catch {
            // If fetch fails, leave original src
          }
        })
      );

      // Hide gradient overlays that html2canvas can't render (mixBlendMode)
      const overlays = el.querySelectorAll<HTMLElement>("[data-flag-overlay]");
      overlays.forEach((o) => { o.style.display = "none"; });

      // Wait a tick for image src changes to take effect
      await new Promise((r) => setTimeout(r, 100));

      const canvas = await html2canvas(el, {
        scale: 2,
        backgroundColor: "#ffffff",
        useCORS: true,
        logging: false,
        windowWidth: 900,
      });

      // Restore original image sources and overlays
      for (const { img, src } of originals) {
        img.src = src;
      }
      overlays.forEach((o) => { o.style.display = ""; });

      const pdf = new jsPDF({
        orientation: "portrait",
        unit: "mm",
        format: "a4",
      });
      const pageWidth = pdf.internal.pageSize.getWidth();
      const pageHeight = pdf.internal.pageSize.getHeight();
      const margin = 10;
      const usableWidth = pageWidth - margin * 2;
      const usableHeight = pageHeight - margin * 2;
      const imgWidth = usableWidth;
      const imgHeight = (canvas.height * imgWidth) / canvas.width;

      // Calculate how many pages we need
      const totalPages = Math.ceil(imgHeight / usableHeight);

      for (let page = 0; page < totalPages; page++) {
        if (page > 0) pdf.addPage();

        // Crop a section of the canvas for this page
        const sourceY = Math.round((page * usableHeight / imgHeight) * canvas.height);
        const sourceHeight = Math.round((usableHeight / imgHeight) * canvas.height);
        const pageCanvas = document.createElement("canvas");
        pageCanvas.width = canvas.width;
        pageCanvas.height = Math.min(sourceHeight, canvas.height - sourceY);
        const ctx = pageCanvas.getContext("2d");
        if (ctx) {
          ctx.drawImage(
            canvas,
            0, sourceY, canvas.width, pageCanvas.height,
            0, 0, canvas.width, pageCanvas.height
          );
        }
        const pageImgData = pageCanvas.toDataURL("image/png");
        const pageImgHeight = (pageCanvas.height * imgWidth) / canvas.width;
        pdf.addImage(pageImgData, "PNG", margin, margin, imgWidth, pageImgHeight);
      }

      pdf.save(`${nation.name.replace(/[^a-zA-Z0-9]/g, "-")}-roster.pdf`);
    } catch (err) {
      console.error("PDF generation failed:", err);
    } finally {
      setPdfLoading(false);
    }
  }

  return (
    <>
      <Stack gap="xs">
        <Button
          color="brown"
          leftSection={<IconEye size={16} />}
          onClick={open}
          fullWidth
        >
          View Roster
        </Button>
        <Group grow>
          <Button
            color="brown"
            variant="light"
            leftSection={<IconPrinter size={16} />}
            onClick={handlePrint}
          >
            Print
          </Button>
          <Button
            color="brown"
            variant="light"
            leftSection={<IconDownload size={16} />}
            onClick={handleDownloadPdf}
            loading={pdfLoading}
          >
            Download PDF
          </Button>
        </Group>
      </Stack>

      <Modal
        opened={opened}
        onClose={close}
        title="Army Roster"
        size="90%"
        centered
      >
        <div ref={contentRef}>
          <RosterContent nation={nation} roster={roster} />
        </div>
        <Group grow mt="lg">
          <Button
            color="brown"
            leftSection={<IconPrinter size={16} />}
            onClick={handlePrint}
          >
            Print
          </Button>
          <Button
            color="brown"
            leftSection={<IconDownload size={16} />}
            onClick={handleDownloadPdf}
            loading={pdfLoading}
          >
            Download PDF
          </Button>
        </Group>
      </Modal>
    </>
  );
}
