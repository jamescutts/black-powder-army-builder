"use client";

import { SegmentedControl, Text } from "@mantine/core";
import type { Nation } from "@/data/types";

const ANY = "any";

/**
 * The list's campaign period, for books that divide their lists into them (Albion Triumphant's Peninsular
 * Early, Middle and Late), at the top of the Army command card: it decides what the rest of the list can
 * take. "Any" keeps every period's choices on offer.
 */
export function PeriodPicker({
  nation,
  period,
  onChange,
}: {
  nation: Nation;
  period: string | undefined;
  onChange: (period: string | undefined) => void;
}) {
  if (!nation.periods?.length) return null;
  return (
    <div className="period-picker">
      <Text size="sm" fw={600} id="period-picker-label">
        Campaign period
      </Text>
      <SegmentedControl
        fullWidth
        color="brown"
        aria-labelledby="period-picker-label"
        value={period ?? ANY}
        onChange={(value) => onChange(value === ANY ? undefined : value)}
        data={[
          {
            value: ANY,
            label: (
              <span className="period-option">
                <span>Any</span>
                <span className="period-years">every period</span>
              </span>
            ),
          },
          ...nation.periods.map((p) => ({
            value: p.id,
            label: (
              <span className="period-option">
                <span>{p.label}</span>
                <span className="period-years">{p.years}</span>
              </span>
            ),
          })),
        ]}
      />
    </div>
  );
}
