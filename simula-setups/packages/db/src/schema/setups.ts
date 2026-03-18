import {
  pgTable, uuid, varchar, text, boolean, timestamp, pgEnum, index,
} from "drizzle-orm/pg-core";
import { users } from "./users.js";
import { cars, simEnum } from "./cars.js";
import { tracks } from "./tracks.js";

export const visibilityEnum = pgEnum("visibility", ["private", "public", "marketplace"]);

export const setups = pgTable("setups", {
  id: uuid("id").primaryKey().defaultRandom(),
  userId: uuid("user_id").notNull().references(() => users.id, { onDelete: "cascade" }),
  carId: uuid("car_id").notNull().references(() => cars.id),
  trackId: uuid("track_id").references(() => tracks.id),
  sim: simEnum("sim").notNull(),
  name: varchar("name", { length: 255 }).notNull(),
  description: text("description"),
  tags: text("tags").array().notNull().default([]),
  season: varchar("season", { length: 20 }),
  visibility: visibilityEnum("visibility").notNull().default("private"),
  isBaseline: boolean("is_baseline").notNull().default(false),
  // Points to the active version
  currentVersionId: uuid("current_version_id"),
  createdAt: timestamp("created_at", { withTimezone: true }).notNull().defaultNow(),
  updatedAt: timestamp("updated_at", { withTimezone: true }).notNull().defaultNow(),
  deletedAt: timestamp("deleted_at", { withTimezone: true }),
}, (table) => [
  index("setups_user_id_idx").on(table.userId),
  index("setups_car_id_idx").on(table.carId),
  index("setups_track_id_idx").on(table.trackId),
  index("setups_sim_idx").on(table.sim),
  index("setups_tags_idx").on(table.tags),
]);
