import { config } from "dotenv";
import { resolve } from "path";
import { existsSync } from "fs";

// Load .env from monorepo root
const envPaths = [
  resolve(process.cwd(), ".env"),
  resolve(process.cwd(), "../../.env"),
  resolve(__dirname, "../../../../.env"),
];
const envPath = envPaths.find((p) => existsSync(p));
if (envPath) config({ path: envPath });

import { drizzle } from "drizzle-orm/node-postgres";
import pg from "pg";
import { cars, tracks, users } from "../schema/index";
import { iRacingCars } from "./cars-data";
import { iRacingTracks } from "./tracks-data";

const { Pool } = pg;

async function seed() {
  const pool = new Pool({ connectionString: process.env.DATABASE_URL });
  const db = drizzle(pool);

  console.log("🌱 Seeding database...\n");

  // ---- Seed demo user ----
  console.log("👤 Creating demo user...");
  const [demoUser] = await db
    .insert(users)
    .values({
      email: "demo@simulaproject.com",
      name: "Demo User",
      authProvider: "mock",
    })
    .onConflictDoNothing({ target: users.email })
    .returning();

  if (demoUser) {
    console.log(`   Created: ${demoUser.email} (${demoUser.id})`);
  } else {
    console.log("   Demo user already exists, skipping.");
  }

  // ---- Seed iRacing cars ----
  console.log(`\n🏎️  Seeding ${iRacingCars.length} iRacing cars...`);
  for (const car of iRacingCars) {
    const [inserted] = await db
      .insert(cars)
      .values(car)
      .onConflictDoNothing()
      .returning();
    if (inserted) {
      console.log(`   ✅ ${inserted.name}`);
    }
  }

  // ---- Seed iRacing tracks ----
  console.log(`\n🏁 Seeding ${iRacingTracks.length} iRacing tracks...`);
  for (const track of iRacingTracks) {
    const [inserted] = await db
      .insert(tracks)
      .values(track)
      .onConflictDoNothing()
      .returning();
    if (inserted) {
      console.log(`   ✅ ${inserted.name}${inserted.config ? ` (${inserted.config})` : ""}`);
    }
  }

  console.log("\n✨ Seed completed!\n");
  await pool.end();
}

seed().catch((err) => {
  console.error("❌ Seed failed:", err);
  process.exit(1);
});
