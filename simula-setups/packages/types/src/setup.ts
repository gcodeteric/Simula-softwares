import type { Sim, Visibility, VersionSource, NoteType, LibrarySource } from "./enums";

// ---- Car ----
export interface Car {
  id: string;
  sim: Sim;
  name: string;
  manufacturer: string;
  carClass: string;
  parameterSchema: Record<string, ParameterSchemaEntry>;
  metadata: Record<string, unknown>;
  createdAt: string;
  updatedAt: string;
}

export interface ParameterSchemaEntry {
  type: "integer" | "float" | "discrete" | "boolean";
  label: string;
  category: SetupCategory;
  unit?: string;
  min?: number;
  max?: number;
  step?: number;
  values?: string[];
}

// ---- Track ----
export interface Track {
  id: string;
  sim: Sim;
  name: string;
  config: string | null;
  country: string;
  trackType: string;
  metadata: Record<string, unknown>;
  createdAt: string;
  updatedAt: string;
}

// ---- Setup Categories ----
export const SETUP_CATEGORIES = [
  "tires",
  "suspension",
  "chassis",
  "brakes",
  "aero",
  "fuel",
  "differential",
  "gearing",
  "electronics",
] as const;
export type SetupCategory = (typeof SETUP_CATEGORIES)[number];

// ---- Setup ----
export interface Setup {
  id: string;
  userId: string;
  carId: string;
  trackId: string | null;
  sim: Sim;
  name: string;
  description: string | null;
  tags: string[];
  season: string | null;
  visibility: Visibility;
  isBaseline: boolean;
  currentVersionId: string | null;
  createdAt: string;
  updatedAt: string;
}

export interface SetupWithRelations extends Setup {
  car: Car;
  track: Track | null;
  currentVersion: SetupVersion | null;
}

export interface CreateSetupInput {
  carId: string;
  trackId?: string;
  sim: Sim;
  name: string;
  description?: string;
  tags?: string[];
  season?: string;
  visibility?: Visibility;
  isBaseline?: boolean;
  parameters: Record<string, unknown>;
  changelog?: string;
}

export interface UpdateSetupInput {
  name?: string;
  description?: string;
  tags?: string[];
  season?: string;
  visibility?: Visibility;
  isBaseline?: boolean;
}

// ---- Setup Version ----
export interface SetupVersion {
  id: string;
  setupId: string;
  versionNumber: number;
  parameters: Record<string, unknown>;
  rawFileKey: string | null;
  rawFileHash: string | null;
  changelog: string | null;
  source: VersionSource;
  createdAt: string;
}

export interface CreateVersionInput {
  parameters: Record<string, unknown>;
  changelog?: string;
  source?: VersionSource;
}

// ---- Setup Note ----
export interface SetupNote {
  id: string;
  setupVersionId: string;
  userId: string;
  type: NoteType;
  content: string;
  createdAt: string;
  updatedAt: string;
}

export interface CreateNoteInput {
  content: string;
}

export interface UpdateNoteInput {
  content: string;
}

// ---- User Library ----
export interface UserLibraryEntry {
  id: string;
  userId: string;
  setupId: string;
  source: LibrarySource;
  isFavorite: boolean;
  folder: string | null;
  addedAt: string;
  lastUsedAt: string | null;
  setup?: SetupWithRelations;
}
