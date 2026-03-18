"use client";

import { useQuery, useMutation, useQueryClient } from "@tanstack/react-query";
import { api } from "@/lib/api";

export function useNotes(setupId: string, versionId: string) {
  return useQuery({
    queryKey: ["notes", setupId, versionId],
    queryFn: () => api.get(`/api/v1/setups/${setupId}/versions/${versionId}/notes`),
    enabled: !!setupId && !!versionId,
  });
}

export function useCreateNote(setupId: string, versionId: string) {
  const qc = useQueryClient();
  return useMutation({
    mutationFn: (content: string) =>
      api.post(`/api/v1/setups/${setupId}/versions/${versionId}/notes`, { content }),
    onSuccess: () => qc.invalidateQueries({ queryKey: ["notes", setupId, versionId] }),
  });
}

export function useUpdateNote(setupId: string, versionId: string) {
  const qc = useQueryClient();
  return useMutation({
    mutationFn: ({ noteId, content }: { noteId: string; content: string }) =>
      api.put(`/api/v1/notes/${noteId}`, { content }),
    onSuccess: () => qc.invalidateQueries({ queryKey: ["notes", setupId, versionId] }),
  });
}

export function useDeleteNote(setupId: string, versionId: string) {
  const qc = useQueryClient();
  return useMutation({
    mutationFn: (noteId: string) => api.del(`/api/v1/notes/${noteId}`),
    onSuccess: () => qc.invalidateQueries({ queryKey: ["notes", setupId, versionId] }),
  });
}
