import { Router } from "express";
import { z } from "zod";
import { requireAuth } from "../middleware/auth.js";
import { noteService } from "../services/note.service.js";

const router = Router();

const noteBodySchema = z.object({
  content: z.string().min(1),
});

/** GET /api/v1/setups/:id/versions/:versionId/notes */
router.get("/setups/:id/versions/:versionId/notes", requireAuth, async (req, res, next) => {
  try {
    const notes = await noteService.listForVersion(req.params.id as string, req.params.versionId as string, req.user!.id);
    res.json({ success: true, data: notes });
  } catch (err) {
    next(err);
  }
});

/** POST /api/v1/setups/:id/versions/:versionId/notes */
router.post("/setups/:id/versions/:versionId/notes", requireAuth, async (req, res, next) => {
  try {
    const { content } = noteBodySchema.parse(req.body);
    const note = await noteService.create(req.params.id as string, req.params.versionId as string, req.user!.id, content);
    res.status(201).json({ success: true, data: note });
  } catch (err) {
    next(err);
  }
});

/** PUT /api/v1/notes/:noteId */
router.put("/notes/:noteId", requireAuth, async (req, res, next) => {
  try {
    const { content } = noteBodySchema.parse(req.body);
    const note = await noteService.update(req.params.noteId as string, req.user!.id, content);
    res.json({ success: true, data: note });
  } catch (err) {
    next(err);
  }
});

/** DELETE /api/v1/notes/:noteId */
router.delete("/notes/:noteId", requireAuth, async (req, res, next) => {
  try {
    await noteService.delete(req.params.noteId as string, req.user!.id);
    res.json({ success: true, data: { deleted: true } });
  } catch (err) {
    next(err);
  }
});

export { router as notesRouter };
