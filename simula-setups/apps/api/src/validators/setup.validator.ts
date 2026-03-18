import { z } from "zod";

export const createSetupSchema = z.object({
  carId: z.string().uuid(),
  trackId: z.string().uuid().optional(),
  sim: z.enum(["iracing", "acc", "rfactor2", "lmu"]),
  name: z.string().min(1).max(255),
  description: z.string().optional(),
  tags: z.array(z.string()).optional().default([]),
  season: z.string().max(20).optional(),
  visibility: z.enum(["private", "public", "marketplace"]).optional().default("private"),
  isBaseline: z.boolean().optional().default(false),
  parameters: z.record(z.unknown()).default({}),
  changelog: z.string().optional(),
});

export const updateSetupSchema = z.object({
  name: z.string().min(1).max(255).optional(),
  description: z.string().nullable().optional(),
  tags: z.array(z.string()).optional(),
  season: z.string().max(20).nullable().optional(),
  visibility: z.enum(["private", "public", "marketplace"]).optional(),
  isBaseline: z.boolean().optional(),
});

export const createVersionSchema = z.object({
  parameters: z.record(z.unknown()),
  changelog: z.string().optional(),
  source: z.enum(["manual", "import", "marketplace_purchase", "ai_generated"]).optional().default("manual"),
});

export const libraryQuerySchema = z.object({
  page: z.coerce.number().min(1).optional().default(1),
  pageSize: z.coerce.number().min(1).max(100).optional().default(20),
  carId: z.string().uuid().optional(),
  trackId: z.string().uuid().optional(),
  sim: z.enum(["iracing", "acc", "rfactor2", "lmu"]).optional(),
  search: z.string().optional(),
  tags: z.string().optional(), // comma-separated
  folder: z.string().optional(),
  isFavorite: z.coerce.boolean().optional(),
  sortBy: z.enum(["name", "createdAt", "updatedAt"]).optional().default("updatedAt"),
  sortOrder: z.enum(["asc", "desc"]).optional().default("desc"),
});

export type CreateSetupInput = z.infer<typeof createSetupSchema>;
export type UpdateSetupInput = z.infer<typeof updateSetupSchema>;
export type CreateVersionInput = z.infer<typeof createVersionSchema>;
export type LibraryQueryParams = z.infer<typeof libraryQuerySchema>;
