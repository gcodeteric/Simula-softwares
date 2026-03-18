import { db, setupNotes, setupVersions, setups } from "@simula-setups/db";
import { eq, and, desc } from "drizzle-orm";
import { AppError } from "../middleware/error-handler.js";

export class NoteService {
  /**
   * List notes for a specific version.
   */
  async listForVersion(setupId: string, versionId: string, userId: string) {
    // Verify access
    const [setup] = await db.select().from(setups).where(eq(setups.id, setupId)).limit(1);
    if (!setup) throw new AppError(404, "NOT_FOUND", "Setup not found");
    if (setup.userId !== userId && setup.visibility === "private") {
      throw new AppError(403, "FORBIDDEN", "No access to this setup");
    }

    const notes = await db
      .select()
      .from(setupNotes)
      .where(eq(setupNotes.setupVersionId, versionId))
      .orderBy(desc(setupNotes.createdAt));

    return notes;
  }

  /**
   * Create a note on a version.
   */
  async create(setupId: string, versionId: string, userId: string, content: string) {
    const [setup] = await db.select().from(setups).where(eq(setups.id, setupId)).limit(1);
    if (!setup) throw new AppError(404, "NOT_FOUND", "Setup not found");
    if (setup.userId !== userId) throw new AppError(403, "FORBIDDEN", "Not your setup");

    // Verify version exists
    const [version] = await db.select().from(setupVersions)
      .where(and(eq(setupVersions.id, versionId), eq(setupVersions.setupId, setupId)))
      .limit(1);
    if (!version) throw new AppError(404, "NOT_FOUND", "Version not found");

    const [note] = await db.insert(setupNotes).values({
      setupVersionId: versionId,
      userId,
      type: "manual",
      content,
    }).returning();

    return note;
  }

  /**
   * Update a note.
   */
  async update(noteId: string, userId: string, content: string) {
    const [note] = await db.select().from(setupNotes).where(eq(setupNotes.id, noteId)).limit(1);
    if (!note) throw new AppError(404, "NOT_FOUND", "Note not found");
    if (note.userId !== userId) throw new AppError(403, "FORBIDDEN", "Not your note");

    const [updated] = await db
      .update(setupNotes)
      .set({ content, updatedAt: new Date() })
      .where(eq(setupNotes.id, noteId))
      .returning();

    return updated;
  }

  /**
   * Delete a note.
   */
  async delete(noteId: string, userId: string) {
    const [note] = await db.select().from(setupNotes).where(eq(setupNotes.id, noteId)).limit(1);
    if (!note) throw new AppError(404, "NOT_FOUND", "Note not found");
    if (note.userId !== userId) throw new AppError(403, "FORBIDDEN", "Not your note");

    await db.delete(setupNotes).where(eq(setupNotes.id, noteId));
    return { deleted: true };
  }
}

export const noteService = new NoteService();
