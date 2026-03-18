import {
  db, setups, setupVersions, userLibrary, cars, tracks,
} from "@simula-setups/db";
import { eq, and, desc, asc, isNull, ilike, sql, inArray } from "drizzle-orm";
import { AppError } from "../middleware/error-handler.js";
import type { CreateSetupInput, UpdateSetupInput, LibraryQueryParams } from "../validators/setup.validator.js";

export class SetupService {
  /**
   * Create a new setup with its initial version.
   */
  async create(userId: string, input: CreateSetupInput) {
    // Verify car exists
    const [car] = await db.select().from(cars).where(eq(cars.id, input.carId)).limit(1);
    if (!car) throw new AppError(404, "NOT_FOUND", "Car not found");

    // Verify track exists (if provided)
    if (input.trackId) {
      const [track] = await db.select().from(tracks).where(eq(tracks.id, input.trackId)).limit(1);
      if (!track) throw new AppError(404, "NOT_FOUND", "Track not found");
    }

    // Create setup + first version + library entry in transaction
    const result = await db.transaction(async (tx) => {
      // 1. Create the setup
      const [setup] = await tx.insert(setups).values({
        userId,
        carId: input.carId,
        trackId: input.trackId || null,
        sim: input.sim,
        name: input.name,
        description: input.description || null,
        tags: input.tags || [],
        season: input.season || null,
        visibility: input.visibility || "private",
        isBaseline: input.isBaseline || false,
      }).returning();

      // 2. Create the first version
      const [version] = await tx.insert(setupVersions).values({
        setupId: setup.id,
        versionNumber: 1,
        parameters: input.parameters,
        changelog: input.changelog || "Initial version",
        source: "manual",
        createdBy: userId,
      }).returning();

      // 3. Update setup with current version pointer
      await tx.update(setups)
        .set({ currentVersionId: version.id })
        .where(eq(setups.id, setup.id));

      // 4. Add to user library
      await tx.insert(userLibrary).values({
        userId,
        setupId: setup.id,
        source: "created",
      });

      return { ...setup, currentVersionId: version.id, currentVersion: version };
    });

    return result;
  }

  /**
   * Get a single setup with car, track, and current version.
   */
  async getById(setupId: string, userId: string) {
    const [setup] = await db
      .select()
      .from(setups)
      .where(and(
        eq(setups.id, setupId),
        isNull(setups.deletedAt),
      ))
      .limit(1);

    if (!setup) throw new AppError(404, "NOT_FOUND", "Setup not found");

    // Check access — only owner or public setups
    if (setup.userId !== userId && setup.visibility === "private") {
      throw new AppError(403, "FORBIDDEN", "You don't have access to this setup");
    }

    // Fetch relations
    const [car] = await db.select().from(cars).where(eq(cars.id, setup.carId)).limit(1);
    const track = setup.trackId
      ? (await db.select().from(tracks).where(eq(tracks.id, setup.trackId)).limit(1))[0]
      : null;

    let currentVersion = null;
    if (setup.currentVersionId) {
      [currentVersion] = await db
        .select()
        .from(setupVersions)
        .where(eq(setupVersions.id, setup.currentVersionId))
        .limit(1);
    }

    return { ...setup, car, track, currentVersion };
  }

  /**
   * List setups in user's library with filters and pagination.
   */
  async listLibrary(userId: string, params: LibraryQueryParams) {
    const { page, pageSize, carId, trackId, sim, search, tags, folder, isFavorite, sortBy, sortOrder } = params;
    const offset = (page - 1) * pageSize;

    // Build conditions
    const conditions = [
      eq(userLibrary.userId, userId),
      isNull(setups.deletedAt),
    ];

    if (carId) conditions.push(eq(setups.carId, carId));
    if (trackId) conditions.push(eq(setups.trackId, trackId));
    if (sim) conditions.push(eq(setups.sim, sim as any));
    if (folder) conditions.push(eq(userLibrary.folder, folder));
    if (isFavorite !== undefined) conditions.push(eq(userLibrary.isFavorite, isFavorite));
    if (search) {
      conditions.push(ilike(setups.name, `%${search}%`));
    }

    // Count total
    const [{ count: total }] = await db
      .select({ count: sql<number>`count(*)::int` })
      .from(userLibrary)
      .innerJoin(setups, eq(userLibrary.setupId, setups.id))
      .where(and(...conditions));

    // Sort
    const sortColumn = sortBy === "name" ? setups.name : sortBy === "createdAt" ? setups.createdAt : setups.updatedAt;
    const orderFn = sortOrder === "asc" ? asc : desc;

    // Fetch setups with joins
    const rows = await db
      .select({
        library: userLibrary,
        setup: setups,
      })
      .from(userLibrary)
      .innerJoin(setups, eq(userLibrary.setupId, setups.id))
      .where(and(...conditions))
      .orderBy(orderFn(sortColumn))
      .limit(pageSize)
      .offset(offset);

    // Fetch related cars and tracks for all results
    const setupIds = rows.map((r) => r.setup.id);

    if (setupIds.length === 0) {
      return {
        data: [],
        pagination: { page, pageSize, total, totalPages: Math.ceil(total / pageSize) },
      };
    }

    const carIds = [...new Set(rows.map((r) => r.setup.carId))];
    const trackIds = [...new Set(rows.map((r) => r.setup.trackId).filter(Boolean))] as string[];

    const allCars = carIds.length > 0
      ? await db.select().from(cars).where(inArray(cars.id, carIds))
      : [];
    const allTracks = trackIds.length > 0
      ? await db.select().from(tracks).where(inArray(tracks.id, trackIds))
      : [];

    // Fetch current versions
    const versionIds = rows.map((r) => r.setup.currentVersionId).filter(Boolean) as string[];
    const allVersions = versionIds.length > 0
      ? await db.select().from(setupVersions).where(inArray(setupVersions.id, versionIds))
      : [];

    const carMap = Object.fromEntries(allCars.map((c) => [c.id, c]));
    const trackMap = Object.fromEntries(allTracks.map((t) => [t.id, t]));
    const versionMap = Object.fromEntries(allVersions.map((v) => [v.id, v]));

    const data = rows.map((row) => ({
      ...row.library,
      setup: {
        ...row.setup,
        car: carMap[row.setup.carId] || null,
        track: row.setup.trackId ? trackMap[row.setup.trackId] || null : null,
        currentVersion: row.setup.currentVersionId ? versionMap[row.setup.currentVersionId] || null : null,
      },
    }));

    return {
      data,
      pagination: {
        page,
        pageSize,
        total,
        totalPages: Math.ceil(total / pageSize),
      },
    };
  }

  /**
   * Update setup metadata.
   */
  async update(setupId: string, userId: string, input: UpdateSetupInput) {
    const [setup] = await db.select().from(setups).where(eq(setups.id, setupId)).limit(1);
    if (!setup) throw new AppError(404, "NOT_FOUND", "Setup not found");
    if (setup.userId !== userId) throw new AppError(403, "FORBIDDEN", "Not your setup");

    const [updated] = await db
      .update(setups)
      .set({ ...input, updatedAt: new Date() })
      .where(eq(setups.id, setupId))
      .returning();

    return updated;
  }

  /**
   * Soft-delete a setup.
   */
  async delete(setupId: string, userId: string) {
    const [setup] = await db.select().from(setups).where(eq(setups.id, setupId)).limit(1);
    if (!setup) throw new AppError(404, "NOT_FOUND", "Setup not found");
    if (setup.userId !== userId) throw new AppError(403, "FORBIDDEN", "Not your setup");

    await db
      .update(setups)
      .set({ deletedAt: new Date() })
      .where(eq(setups.id, setupId));

    return { deleted: true };
  }

  // ============ FAVORITES ============

  /**
   * Toggle favorite status for a setup in user's library.
   */
  async toggleFavorite(setupId: string, userId: string) {
    const [entry] = await db
      .select()
      .from(userLibrary)
      .where(and(eq(userLibrary.userId, userId), eq(userLibrary.setupId, setupId)))
      .limit(1);

    if (!entry) throw new AppError(404, "NOT_FOUND", "Setup not in your library");

    const [updated] = await db
      .update(userLibrary)
      .set({ isFavorite: !entry.isFavorite })
      .where(eq(userLibrary.id, entry.id))
      .returning();

    return { isFavorite: updated.isFavorite };
  }

  // ============ FOLDERS ============

  /**
   * Move a setup to a folder (or null to remove from folder).
   */
  async moveToFolder(setupId: string, userId: string, folder: string | null) {
    const [entry] = await db
      .select()
      .from(userLibrary)
      .where(and(eq(userLibrary.userId, userId), eq(userLibrary.setupId, setupId)))
      .limit(1);

    if (!entry) throw new AppError(404, "NOT_FOUND", "Setup not in your library");

    const [updated] = await db
      .update(userLibrary)
      .set({ folder })
      .where(eq(userLibrary.id, entry.id))
      .returning();

    return updated;
  }

  /**
   * List all folders for a user.
   */
  async listFolders(userId: string) {
    const rows = await db
      .select({
        folder: userLibrary.folder,
        count: sql<number>`count(*)::int`,
      })
      .from(userLibrary)
      .innerJoin(setups, eq(userLibrary.setupId, setups.id))
      .where(and(
        eq(userLibrary.userId, userId),
        isNull(setups.deletedAt),
        sql`${userLibrary.folder} IS NOT NULL`,
      ))
      .groupBy(userLibrary.folder);

    return rows.map((r) => ({ name: r.folder!, count: r.count }));
  }

  // ============ LIBRARY STATS ============

  /**
   * Get library summary counts for the sidebar.
   */
  async getLibraryStats(userId: string) {
    const [stats] = await db
      .select({
        total: sql<number>`count(*)::int`,
        favorites: sql<number>`count(*) FILTER (WHERE ${userLibrary.isFavorite} = true)::int`,
      })
      .from(userLibrary)
      .innerJoin(setups, eq(userLibrary.setupId, setups.id))
      .where(and(
        eq(userLibrary.userId, userId),
        isNull(setups.deletedAt),
      ));

    return {
      total: stats?.total || 0,
      favorites: stats?.favorites || 0,
    };
  }
}

export const setupService = new SetupService();
