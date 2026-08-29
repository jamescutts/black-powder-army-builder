"use client";

import { Suspense, useEffect } from "react";
import { useSearchParams, useRouter } from "next/navigation";
import { getNation } from "@/data";

// Legacy URL shim: this app originally lived at the site root, with the builder at
// /builder?nation=X. It now lives under /black-powder/{supplement}/{nation}.
export default function LegacyRootBuilderRedirect() {
  return (
    <Suspense>
      <RedirectToNewUrl />
    </Suspense>
  );
}

function RedirectToNewUrl() {
  const searchParams = useSearchParams();
  const router = useRouter();

  useEffect(() => {
    const nationId = searchParams.get("nation");
    const nation = nationId ? getNation(nationId) : undefined;
    router.replace(nation ? `/black-powder/${nation.supplementId}/${nation.id}` : "/black-powder");
  }, [searchParams, router]);

  return null;
}
