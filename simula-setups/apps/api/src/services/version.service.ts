import { db, setups, setupVersions } from "@simula-setups/db";
import { eq, and, desc, sql } from "drizzle-orm";
import { AppError } from "../middleware/error-handler.js";
import type { CreateVersionInput } from "../validators/setup.validator.js";

export class VersionService {
  /**
   * List all versions for a setup.
   */
  async listVersions(setupId: string, userId: string) {
    // Verify setup exists and user has access
    const [setup] = await db.select().from(setups).where(eq(setups.id, setupId)).limit(1);
    if (!setup) throw new AppError(404, "NOT_FOUND", "Setup not found");
    if (setup.userId !== userId && setup.visibility === "private") {
      throw new AppError(403, "FORBIDDEN", "No access to this setup");
    }

    const versions = await db
      .select()
      .from(setupVersions)
      .where(eq(setupVersions.setupId, setupId))
      .orderBy(desc(setupVersions.versionNumber));

    return { versions, currentVersionId: setup.currentVersionId };
  }

  /**
   * Get a specific version.
   */
  async getVersion(setupId: string, versionId: string, userId: string) {
    const [setup] = await db.select().from(setups).where(eq(setups.id, setupId)).limit(1);
    if (!setup) throw new AppError(404, "NOT_FOUND", "Setup not found");
    if (setup.userId !== userId && setup.visibility === "private") {
      throw new AppError(403, "FORBIDDEN", "No access to this setup");
    }

    const [version] = await db
      .select()
      .from(setupVersions)
      .where(and(
        eq(setupVersions.id, versionId),
        eq(setupVersions.setupId, setupId),
      ))
      .limit(1);

    if (!version) throw new AppError(404, "NOT_FOUND", "Version not found");

    return { ...version, isCurrent: setup.currentVersionId === version.id };
  }

  /**
   * Create a new version (snapshot-based).
   */
  async createVersion(setupId: string, userId: string, input: CreateVersionInput) {
    const [setup] = await db.select().from(setups).where(eq(setups.id, setupId)).limit(1);
    if (!setup) throw new AppError(404, "NOT_FOUND", "Setup not found");
    if (setup.userId !== userId) throw new AppError(403, "FORBIDDEN", "Not your setup");

    // Get next version number
    const [{ maxVersion }] = await db
      .select({ maxVersion: sql<number>`COALESCE(MAX(${setupVersions.versionNumber}), 0)` })
      .from(setupVersions)
      .where(eq(setupVersions.setupId, setupId));

    const nextVersion = maxVersion + 1;

    // Create new version and update current pointer
    const result = await db.transaction(async (tx) => {
      const [version] = await tx.insert(setupVersions).values({
        setupId,
        versionNumber: nextVersion,
        parameters: input.parameters,
        changelog: input.changelog || null,
        source: input.source || "manual",
        createdBy: userId,
      }).returning();

      await tx.update(setups)
        .set({ currentVersionId: version.id, updatedAt: new Date() })
        .where(eq(setups.id, setupId));

      return version;
    });

    return result;
  }

  /**
   * Revert to a previous version (non-destructive: creates new version).
   */
  async revertToVersion(setupId: string, targetVersionId: string, userId: string) {
    const [setup] = await db.select().from(setups).where(eq(setups.id, setupId)).limit(1);
    if (!setup) throw new AppError(404, "NOT_FOUND", "Setup not found");
    if (setup.userId !== userId) throw new AppError(403, "FORBIDDEN", "Not your setup");

    const [targetVersion] = await db
      .select()
      .from(setupVersions)
      .where(and(
        eq(setupVersions.id, targetVersionId),
        eq(setupVersions.setupId, setupId),
      ))
      .limit(1);

    if (!targetVersion) throw new AppError(404, "NOT_FOUND", "Target version not found");

    // Create new version as a copy of the target
    const newVersion = await this.createVersion(setupId, userId, {
      parameters: targetVersion.parameters as Record<string, unknown>,
      changelog: `Reverted to version ${targetVersion.versionNumber}`,
      source: "manual",
    });

    return newVersion;
  }
}

export const versionService = new VersionService();
