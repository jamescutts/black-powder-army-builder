import { nations, supplements } from "@/data";
import { OG_SIZE, pageCard } from "@/lib/og";

// The Black Powder picker's sharing image; supplements and armies have their own
export const alt = "Black Powder army lists on Army Builder";
export const size = OG_SIZE;
export const contentType = "image/png";

export default function Image() {
  return pageCard({
    kicker: `${supplements.length} supplements · ${nations.length} army lists`,
    title: "Black Powder",
    flags: ["/flags/britain.svg", "/flags/france.svg"],
  });
}
