import type { Metadata } from "next";
import { DocsContent } from "@/components/DocsContent";

export const metadata: Metadata = {
  title: "Adding Army Lists — Army Builder Docs",
  description: "How to add a new supplement, nation, or community army list to the builder using JSON files.",
};

export default function DocsPage() {
  return <DocsContent />;
}
