import {
  pgTable, uuid, text, jsonb, timestamp, pgEnum, index,
} from "drizzle-orm/pg-core";
import { setupVersions } from "./setup-versions";
import { users } from "./users";

export const noteTypeEnum = pgEnum("note_type", [
  "manual", "ai_suggestion", "telemetry_linked",
]);

export const setupNotes = pgTable("setup_notes", {
  id: uuid("id").primaryKey().defaultRandom(),
  setupVersionId: uuid("setup_version_id").notNull().references(() => setupVersions.id, { onDelete: "cascade" }),
  // Logical FK to Telemetry.SessionData (consumed via API, not direct FK)
  sessionId: uuid("session_id"),
  userId: uuid("user_id").notNull().references(() => users.id, { onDelete: "cascade" }),
  type: noteTypeEnum("type").notNull().default("manual"),
  content: text("content").notNull(),
  // AI suggestions payload (populated when type='ai_suggestion')
  aiSuggestions: jsonb("ai_suggestions"),
  // Snapshot of telemetry data at the time of note creation
  telemetrySummary: jsonb("telemetry_summary"),
  createdAt: timestamp("created_at", { withTimezone: true }).notNull().defaultNow(),
  updatedAt: timestamp("updated_at", { withTimezone: true }).notNull().defaultNow(),
}, (table) => [
  index("setup_notes_version_id_idx").on(table.setupVersionId),
  index("setup_notes_user_id_idx").on(table.userId),
]);
