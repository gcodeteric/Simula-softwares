import {
  pgTable, uuid, varchar, boolean, timestamp, pgEnum, index, uniqueIndex,
} from "drizzle-orm/pg-core";
import { users } from "./users";
import { setups } from "./setups";

export const librarySourceEnum = pgEnum("library_source", [
  "created", "purchased", "shared", "imported",
]);

export const userLibrary = pgTable("user_library", {
  id: uuid("id").primaryKey().defaultRandom(),
  userId: uuid("user_id").notNull().references(() => users.id, { onDelete: "cascade" }),
  setupId: uuid("setup_id").notNull().references(() => setups.id, { onDelete: "cascade" }),
  source: librarySourceEnum("source").notNull().default("created"),
  purchaseId: uuid("purchase_id"),
  isFavorite: boolean("is_favorite").notNull().default(false),
  folder: varchar("folder", { length: 255 }),
  addedAt: timestamp("added_at", { withTimezone: true }).notNull().defaultNow(),
  lastUsedAt: timestamp("last_used_at", { withTimezone: true }),
}, (table) => [
  uniqueIndex("user_library_user_setup_idx").on(table.userId, table.setupId),
  index("user_library_user_id_idx").on(table.userId),
  index("user_library_folder_idx").on(table.userId, table.folder),
]);
