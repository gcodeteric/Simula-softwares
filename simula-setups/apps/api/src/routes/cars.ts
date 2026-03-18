import { Router } from "express";
import { db, cars, tracks } from "@simula-setups/db";
import { eq } from "drizzle-orm";
import { redis } from "../lib/redis.js";

const router = Router();

const CARS_CACHE_TTL = 86400; // 24h — cars rarely change
const TRACKS_CACHE_TTL = 86400;

/** GET /api/v1/cars — List all cars, optionally filtered by sim (cached) */
router.get("/cars", async (req, res, next) => {
  try {
    const sim = req.query.sim as string | undefined;
    const cacheKey = `cars:${sim || "all"}`;

    // Try cache first
    const cached = await redis.get(cacheKey).catch(() => null);
    if (cached) {
      res.json({ success: true, data: JSON.parse(cached) });
      return;
    }

    let query = db.select().from(cars);
    if (sim) {
      query = query.where(eq(cars.sim, sim as any)) as any;
    }

    const result = await query;

    // Cache result
    await redis.set(cacheKey, JSON.stringify(result), "EX", CARS_CACHE_TTL).catch(() => {});

    res.json({ success: true, data: result });
  } catch (err) {
    next(err);
  }
});

/** GET /api/v1/cars/:id — Get car by ID */
router.get("/cars/:id", async (req, res, next) => {
  try {
    const [car] = await db.select().from(cars).where(eq(cars.id, req.params.id as string)).limit(1);
    if (!car) {
      res.status(404).json({ success: false, error: { code: "NOT_FOUND", message: "Car not found" } });
      return;
    }
    res.json({ success: true, data: car });
  } catch (err) {
    next(err);
  }
});

/** GET /api/v1/tracks — List all tracks, optionally filtered by sim (cached) */
router.get("/tracks", async (req, res, next) => {
  try {
    const sim = req.query.sim as string | undefined;
    const cacheKey = `tracks:${sim || "all"}`;

    const cached = await redis.get(cacheKey).catch(() => null);
    if (cached) {
      res.json({ success: true, data: JSON.parse(cached) });
      return;
    }

    let query = db.select().from(tracks);
    if (sim) {
      query = query.where(eq(tracks.sim, sim as any)) as any;
    }

    const result = await query;

    await redis.set(cacheKey, JSON.stringify(result), "EX", TRACKS_CACHE_TTL).catch(() => {});

    res.json({ success: true, data: result });
  } catch (err) {
    next(err);
  }
});

/** GET /api/v1/tracks/:id — Get track by ID */
router.get("/tracks/:id", async (req, res, next) => {
  try {
    const [track] = await db.select().from(tracks).where(eq(tracks.id, req.params.id as string)).limit(1);
    if (!track) {
      res.status(404).json({ success: false, error: { code: "NOT_FOUND", message: "Track not found" } });
      return;
    }
    res.json({ success: true, data: track });
  } catch (err) {
    next(err);
  }
});

export { router as carsRouter };
