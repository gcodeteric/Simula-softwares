import { Router } from "express";
import { z } from "zod";
import { requireAuth } from "../middleware/auth.js";
import { compareService } from "../services/compare.service.js";

const router = Router();

const compareQuerySchema = z.object({
  v1: z.string().uuid(),
  v2: z.string().uuid(),
});

const compareBodySchema = z.object({
  versionA: z.string().uuid(),
  versionB: z.string().uuid(),
});

/** GET /api/v1/setups/:id/compare?v1=...&v2=... — Compare two versions of same setup */
router.get("/setups/:id/compare", requireAuth, async (req, res, next) => {
  try {
    const { v1, v2 } = compareQuerySchema.parse(req.query);
    const result = await compareService.compare(v1, v2);
    res.json({ success: true, data: result });
  } catch (err) {
    next(err);
  }
});

/** POST /api/v1/compare — Compare any two versions (cross-setup) */
router.post("/compare", requireAuth, async (req, res, next) => {
  try {
    const { versionA, versionB } = compareBodySchema.parse(req.body);
    const result = await compareService.compare(versionA, versionB);
    res.json({ success: true, data: result });
  } catch (err) {
    next(err);
  }
});

export { router as compareRouter };
