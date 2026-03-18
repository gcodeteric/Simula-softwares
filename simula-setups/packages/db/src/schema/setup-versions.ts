import {
  pgTable, uuid, integer, varchar, text, jsonb, timestamp, pgEnum, index,
} from "drizzle-orm/pg-core";
import { setups } from "./setups.js";
import { users } from "./users.js";

export const versionSourceEnum = pgEnum("version_source", [
  "manual", "import", "marketplace_purchase", "ai_generated",
]);

export const setupVersions = pgTable("setup_versions", {
  id: uuid("id").primaryKey().defaultRandom(),
  setupId: uuid("setup_id").notNull().references(() => setups.id, { onDelete: "cascade" }),
  versionNumber: integer("version_number").notNull(),
  // The full setup parameters as normalized JSONB (snapshot-based)
  parameters: jsonb("parameters").notNull().default({}),
  // S3/R2 key for the original raw file (.sto, .json, etc.)
  rawFileKey: varchar("raw_file_key", { length: 512 }),
  // SHA-256 of the raw file for dedup and integrity
  rawFileHash: varchar("raw_file_hash", { length: 64 }),
  // Human-written changelog for this version
  changelog: text("changelog"),
  source: versionSourceEnum("source").notNull().default("manual"),
  createdAt: timestamp("created_at", { withTimezone: true }).notNull().defaultNow(),
  createdBy: uuid("created_by").notNull().references(() => users.id),
}, (table) => [
  index("setup_versions_setup_id_idx").on(table.setupId),
  index("setup_versions_setup_version_idx").on(table.setupId, table.versionNumber),
]);
