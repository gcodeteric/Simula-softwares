"use client";

import { useQuery } from "@tanstack/react-query";
import { api } from "@/lib/api";

export function useCompareVersions(setupId: string, v1?: string, v2?: string) {
  return useQuery({
    queryKey: ["compare", setupId, v1, v2],
    queryFn: () => api.get(`/api/v1/setups/${setupId}/compare`, { v1, v2 }),
    enabled: !!setupId && !!v1 && !!v2,
  });
}

export function useCrossCompare(versionA?: string, versionB?: string) {
  return useQuery({
    queryKey: ["compare-cross", versionA, versionB],
    queryFn: () => api.post("/api/v1/compare", { versionA, versionB }),
    enabled: !!versionA && !!versionB,
  });
}
