// ---- Sim Racing Simulators ----
export const SIM_VALUES = ["iracing", "acc", "rfactor2", "lmu"] as const;
export type Sim = (typeof SIM_VALUES)[number];

// ---- Car Classes ----
export const CAR_CLASS_VALUES = [
  "gt3",
  "gt4",
  "lmp2",
  "lmh",
  "formula",
  "touring",
  "stock",
  "other",
] as const;
export type CarClass = (typeof CAR_CLASS_VALUES)[number];

// ---- Track Types ----
export const TRACK_TYPE_VALUES = [
  "high_downforce",
  "low_downforce",
  "technical",
  "mixed",
  "oval",
  "street",
] as const;
export type TrackType = (typeof TRACK_TYPE_VALUES)[number];

// ---- Setup Visibility ----
export const VISIBILITY_VALUES = [
  "private",
  "public",
  "marketplace",
] as const;
export type Visibility = (typeof VISIBILITY_VALUES)[number];

// ---- Setup Version Source ----
export const VERSION_SOURCE_VALUES = [
  "manual",
  "import",
  "marketplace_purchase",
  "ai_generated",
] as const;
export type VersionSource = (typeof VERSION_SOURCE_VALUES)[number];

// ---- Setup Note Type ----
export const NOTE_TYPE_VALUES = [
  "manual",
  "ai_suggestion",
  "telemetry_linked",
] as const;
export type NoteType = (typeof NOTE_TYPE_VALUES)[number];

// ---- Library Source ----
export const LIBRARY_SOURCE_VALUES = [
  "created",
  "purchased",
  "shared",
  "imported",
] as const;
export type LibrarySource = (typeof LIBRARY_SOURCE_VALUES)[number];
