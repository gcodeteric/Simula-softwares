import { Router } from "express";
import { requireAuth } from "../middleware/auth.js";
import { versionService } from "../services/version.service.js";
import { createVersionSchema } from "../validators/setup.validator.js";

const router = Router();

/** GET /api/v1/setups/:id/versions — List all versions */
router.get("/setups/:id/versions", requireAuth, async (req, res, next) => {
  try {
    const result = await versionService.listVersions(req.params.id as string, req.user!.id);
    res.json({ success: true, data: result });
  } catch (err) {
    next(err);
  }
});

/** POST /api/v1/setups/:id/versions — Create new version */
router.post("/setups/:id/versions", requireAuth, async (req, res, next) => {
  try {
    const input = createVersionSchema.parse(req.body);
    const version = await versionService.createVersion(req.params.id as string, req.user!.id, input);
    res.status(201).json({ success: true, data: version });
  } catch (err) {
    next(err);
  }
});

/** GET /api/v1/setups/:id/versions/:versionId — Get version detail */
router.get("/setups/:id/versions/:versionId", requireAuth, async (req, res, next) => {
  try {
    const version = await versionService.getVersion(req.params.id as string, req.params.versionId as string, req.user!.id);
    res.json({ success: true, data: version });
  } catch (err) {
    next(err);
  }
});

/** POST /api/v1/setups/:id/revert/:versionId — Revert (non-destructive) */
router.post("/setups/:id/revert/:versionId", requireAuth, async (req, res, next) => {
  try {
    const version = await versionService.revertToVersion(req.params.id as string, req.params.versionId as string, req.user!.id);
    res.status(201).json({ success: true, data: version });
  } catch (err) {
    next(err);
  }
});

export { router as versionsRouter };
