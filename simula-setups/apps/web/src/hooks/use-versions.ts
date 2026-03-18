"use client";

import { useQuery, useMutation, useQueryClient } from "@tanstack/react-query";
import { api } from "@/lib/api";

export function useVersions(setupId: string) {
  return useQuery({
    queryKey: ["versions", setupId],
    queryFn: () => api.get(`/api/v1/setups/${setupId}/versions`),
    enabled: !!setupId,
  });
}

export function useVersion(setupId: string, versionId: string) {
  return useQuery({
    queryKey: ["version", setupId, versionId],
    queryFn: () => api.get(`/api/v1/setups/${setupId}/versions/${versionId}`),
    enabled: !!setupId && !!versionId,
  });
}

export function useCreateVersion(setupId: string) {
  const qc = useQueryClient();
  return useMutation({
    mutationFn: (data: { parameters: Record<string, unknown>; changelog?: string }) =>
      api.post(`/api/v1/setups/${setupId}/versions`, data),
    onSuccess: () => {
      qc.invalidateQueries({ queryKey: ["versions", setupId] });
      qc.invalidateQueries({ queryKey: ["setup", setupId] });
    },
  });
}

export function useRevertVersion(setupId: string) {
  const qc = useQueryClient();
  return useMutation({
    mutationFn: (versionId: string) =>
      api.post(`/api/v1/setups/${setupId}/revert/${versionId}`),
    onSuccess: () => {
      qc.invalidateQueries({ queryKey: ["versions", setupId] });
      qc.invalidateQueries({ queryKey: ["setup", setupId] });
    },
  });
}
