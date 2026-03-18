import { Router } from "express";
import { pool } from "@simula-setups/db";
import { checkRedisHealth } from "../lib/redis.js";

const router = Router();

router.get("/health", async (_req, res) => {
  const checks: Record<string, string> = {};

  // Check PostgreSQL
  try {
    await pool.query("SELECT 1");
    checks.database = "connected";
  } catch {
    checks.database = "disconnected";
  }

  // Check Redis
  const redisOk = await checkRedisHealth();
  checks.redis = redisOk ? "connected" : "disconnected";

  const allHealthy = Object.values(checks).every((v) => v === "connected");

  res.status(allHealthy ? 200 : 503).json({
    success: true,
    data: {
      status: allHealthy ? "healthy" : "degraded",
      timestamp: new Date().toISOString(),
      checks,
    },
  });
});

export { router as healthRouter };
