import type { Metadata } from "next";
import { DocsContent } from "@/components/DocsContent";
import { pageMeta } from "@/lib/meta";

export const metadata: Metadata = pageMeta({
  title: "Adding army lists",
  description: "How to add a new supplement, nation, or community army list to the builder using JSON files.",
  path: "/docs",
});

export default function DocsPage() {
  return <DocsContent />;
}
