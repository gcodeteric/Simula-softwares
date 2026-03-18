import { pgTable, uuid, varchar, jsonb, timestamp, pgEnum, index } from "drizzle-orm/pg-core";

export const simEnum = pgEnum("sim", ["iracing", "acc", "rfactor2", "lmu"]);

export const carClassEnum = pgEnum("car_class", [
  "gt3", "gt4", "lmp2", "lmh", "formula", "touring", "stock", "other",
]);

export const cars = pgTable("cars", {
  id: uuid("id").primaryKey().defaultRandom(),
  sim: simEnum("sim").notNull(),
  name: varchar("name", { length: 255 }).notNull(),
  manufacturer: varchar("manufacturer", { length: 255 }).notNull(),
  carClass: carClassEnum("car_class").notNull(),
  // Schema defining available parameters for this car
  // e.g., { "arb_front": { "type": "discrete", "values": ["D1","D2",...] }, ... }
  parameterSchema: jsonb("parameter_schema").notNull().default({}),
  // Extra metadata (power, weight, BoP, etc.)
  metadata: jsonb("metadata").notNull().default({}),
  createdAt: timestamp("created_at", { withTimezone: true }).notNull().defaultNow(),
  updatedAt: timestamp("updated_at", { withTimezone: true }).notNull().defaultNow(),
}, (table) => [
  index("cars_sim_idx").on(table.sim),
  index("cars_class_idx").on(table.carClass),
]);
