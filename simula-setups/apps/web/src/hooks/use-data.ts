"use client";

import { useQuery } from "@tanstack/react-query";
import { api } from "@/lib/api";

export function useCars(sim?: string) {
  return useQuery({
    queryKey: ["cars", sim],
    queryFn: () => api.get("/api/v1/cars", sim ? { sim } : undefined),
    staleTime: 5 * 60 * 1000, // 5 min cache
  });
}

export function useTracks(sim?: string) {
  return useQuery({
    queryKey: ["tracks", sim],
    queryFn: () => api.get("/api/v1/tracks", sim ? { sim } : undefined),
    staleTime: 5 * 60 * 1000,
  });
}
