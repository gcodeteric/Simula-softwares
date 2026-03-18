"use client";

import { useQuery, useMutation, useQueryClient } from "@tanstack/react-query";
import { api } from "@/lib/api";

export function useLibrary(params?: Record<string, string | undefined>) {
  return useQuery({
    queryKey: ["library", params],
    queryFn: () => api.get("/api/v1/library", params),
  });
}

export function useSetup(id: string) {
  return useQuery({
    queryKey: ["setup", id],
    queryFn: () => api.get(`/api/v1/library/setups/${id}`),
    enabled: !!id,
  });
}

export function useCreateSetup() {
  const qc = useQueryClient();
  return useMutation({
    mutationFn: (data: any) => api.post("/api/v1/library", data),
    onSuccess: () => qc.invalidateQueries({ queryKey: ["library"] }),
  });
}

export function useUploadSetup() {
  const qc = useQueryClient();
  return useMutation({
    mutationFn: ({ file, data }: { file: File; data: any }) =>
      api.upload("/api/v1/library", file, data),
    onSuccess: () => qc.invalidateQueries({ queryKey: ["library"] }),
  });
}

export function useUpdateSetup(id: string) {
  const qc = useQueryClient();
  return useMutation({
    mutationFn: (data: any) => api.put(`/api/v1/library/setups/${id}`, data),
    onSuccess: () => {
      qc.invalidateQueries({ queryKey: ["setup", id] });
      qc.invalidateQueries({ queryKey: ["library"] });
    },
  });
}

export function useDeleteSetup() {
  const qc = useQueryClient();
  return useMutation({
    mutationFn: (id: string) => api.del(`/api/v1/library/setups/${id}`),
    onSuccess: () => qc.invalidateQueries({ queryKey: ["library"] }),
  });
}

// ============ FAVORITES ============

export function useToggleFavorite() {
  const qc = useQueryClient();
  return useMutation({
    mutationFn: (setupId: string) => api.patch(`/api/v1/library/setups/${setupId}/favorite`),
    onSuccess: () => {
      qc.invalidateQueries({ queryKey: ["library"] });
      qc.invalidateQueries({ queryKey: ["library-stats"] });
    },
  });
}

// ============ FOLDERS ============

export function useFolders() {
  return useQuery({
    queryKey: ["library-folders"],
    queryFn: () => api.get("/api/v1/library/folders"),
  });
}

export function useMoveToFolder() {
  const qc = useQueryClient();
  return useMutation({
    mutationFn: ({ setupId, folder }: { setupId: string; folder: string | null }) =>
      api.patch(`/api/v1/library/setups/${setupId}/folder`, { folder }),
    onSuccess: () => {
      qc.invalidateQueries({ queryKey: ["library"] });
      qc.invalidateQueries({ queryKey: ["library-folders"] });
    },
  });
}

// ============ STATS ============

export function useLibraryStats() {
  return useQuery({
    queryKey: ["library-stats"],
    queryFn: () => api.get("/api/v1/library/stats"),
  });
}
