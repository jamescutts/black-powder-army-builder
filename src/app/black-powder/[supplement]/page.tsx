import { notFound } from "next/navigation";
import { getSupplement } from "@/data";
import { SupplementNationPicker } from "@/components/SupplementNationPicker";

export default async function SupplementPage({
  params,
}: {
  params: Promise<{ supplement: string }>;
}) {
  const { supplement } = await params;
  if (!getSupplement(supplement)) notFound();
  return <SupplementNationPicker initialSupplementId={supplement} />;
}
