import { Router } from "express";
import { requireAuth } from "../middleware/auth.js";
import { setupService } from "../services/setup.service.js";
import { createSetupSchema, updateSetupSchema, libraryQuerySchema } from "../validators/setup.validator.js";
import { storage } from "../lib/storage.js";
import { parserRegistry } from "@simula-setups/parsers";
import multer from "multer";

const router = Router();
const upload = multer({ storage: multer.memoryStorage(), limits: { fileSize: 5 * 1024 * 1024 } }); // 5MB max

/**
 * GET /api/v1/library — List user's setups with filters and pagination
 */
router.get("/library", requireAuth, async (req, res, next) => {
  try {
    const params = libraryQuerySchema.parse(req.query);
    const result = await setupService.listLibrary(req.user!.id, params);

    res.json({
      success: true,
      data: result.data,
      pagination: result.pagination,
    });
  } catch (err) {
    next(err);
  }
});

/**
 * POST /api/v1/library — Create a new setup
 * Accepts multipart (with file) or JSON body
 */
router.post("/library", requireAuth, upload.single("file"), async (req, res, next) => {
  try {
    // Parse body — may come as form data or JSON
    const body = req.file ? JSON.parse(req.body.data || "{}") : req.body;
    const input = createSetupSchema.parse(body);

    // If file was uploaded, process it
    if (req.file) {
      const parser = parserRegistry.findParser(req.file.originalname);
      if (parser) {
        const parseResult = await parser.parse(req.file.buffer, req.file.originalname);

        // Store raw file
        const fileKey = `setups/${req.user!.id}/${Date.now()}_${req.file.originalname}`;
        await storage.upload(fileKey, req.file.buffer, req.file.mimetype);

        // Merge parsed parameters with user-provided (user input takes precedence)
        input.parameters = { ...parseResult.parameters, ...input.parameters };

        // Store file reference (will be added to version later via service)
        (input as any)._rawFileKey = fileKey;
        (input as any)._rawFileHash = parseResult.fileHash;
      }
    }

    const setup = await setupService.create(req.user!.id, input);

    res.status(201).json({
      success: true,
      data: setup,
    });
  } catch (err) {
    next(err);
  }
});

/**
 * GET /api/v1/library/setups/:id — Get setup detail
 */
router.get("/library/setups/:id", requireAuth, async (req, res, next) => {
  try {
    const setup = await setupService.getById(req.params.id as string, req.user!.id);
    res.json({ success: true, data: setup });
  } catch (err) {
    next(err);
  }
});

/**
 * PUT /api/v1/library/setups/:id — Update setup metadata
 */
router.put("/library/setups/:id", requireAuth, async (req, res, next) => {
  try {
    const input = updateSetupSchema.parse(req.body);
    const setup = await setupService.update(req.params.id as string, req.user!.id, input);
    res.json({ success: true, data: setup });
  } catch (err) {
    next(err);
  }
});

/**
 * DELETE /api/v1/library/setups/:id — Soft delete
 */
router.delete("/library/setups/:id", requireAuth, async (req, res, next) => {
  try {
    await setupService.delete(req.params.id as string, req.user!.id);
    res.json({ success: true, data: { deleted: true } });
  } catch (err) {
    next(err);
  }
});

// ============ FAVORITES ============

/** PATCH /api/v1/library/setups/:id/favorite — Toggle favorite */
router.patch("/library/setups/:id/favorite", requireAuth, async (req, res, next) => {
  try {
    const result = await setupService.toggleFavorite(req.params.id as string, req.user!.id);
    res.json({ success: true, data: result });
  } catch (err) {
    next(err);
  }
});

// ============ FOLDERS ============

/** PATCH /api/v1/library/setups/:id/folder — Move setup to folder */
router.patch("/library/setups/:id/folder", requireAuth, async (req, res, next) => {
  try {
    const { folder } = req.body as { folder: string | null };
    const result = await setupService.moveToFolder(req.params.id as string, req.user!.id, folder ?? null);
    res.json({ success: true, data: result });
  } catch (err) {
    next(err);
  }
});

/** GET /api/v1/library/folders — List user's folders */
router.get("/library/folders", requireAuth, async (req, res, next) => {
  try {
    const folders = await setupService.listFolders(req.user!.id);
    res.json({ success: true, data: folders });
  } catch (err) {
    next(err);
  }
});

/** GET /api/v1/library/stats — Library summary counts */
router.get("/library/stats", requireAuth, async (req, res, next) => {
  try {
    const stats = await setupService.getLibraryStats(req.user!.id);
    res.json({ success: true, data: stats });
  } catch (err) {
    next(err);
  }
});

export { router as libraryRouter };
