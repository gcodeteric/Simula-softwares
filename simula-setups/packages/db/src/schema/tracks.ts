import { pgTable, uuid, varchar, jsonb, timestamp, pgEnum, index } from "drizzle-orm/pg-core";
import { simEnum } from "./cars.js";

export const trackTypeEnum = pgEnum("track_type", [
  "high_downforce", "low_downforce", "technical", "mixed", "oval", "street",
]);

export const tracks = pgTable("tracks", {
  id: uuid("id").primaryKey().defaultRandom(),
  sim: simEnum("sim").notNull(),
  name: varchar("name", { length: 255 }).notNull(),
  config: varchar("config", { length: 255 }),
  country: varchar("country", { length: 100 }).notNull().default(""),
  trackType: trackTypeEnum("track_type").notNull().default("mixed"),
  // Extra metadata (length, corners, etc.)
  metadata: jsonb("metadata").notNull().default({}),
  createdAt: timestamp("created_at", { withTimezone: true }).notNull().defaultNow(),
  updatedAt: timestamp("updated_at", { withTimezone: true }).notNull().defaultNow(),
}, (table) => [
  index("tracks_sim_idx").on(table.sim),
]);
