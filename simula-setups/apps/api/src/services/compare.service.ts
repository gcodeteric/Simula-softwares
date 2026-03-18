import { db, setupVersions, setups, cars } from "@simula-setups/db";
import { eq } from "drizzle-orm";
import { AppError } from "../middleware/error-handler.js";
import type { ComparisonResult, ComparisonCategory, ComparisonParameter } from "@simula-setups/types";

export class CompareService {
  /**
   * Compare two versions of the same or different setups.
   */
  async compare(versionIdA: string, versionIdB: string): Promise<ComparisonResult> {
    // Fetch both versions
    const [versionA] = await db.select().from(setupVersions).where(eq(setupVersions.id, versionIdA)).limit(1);
    const [versionB] = await db.select().from(setupVersions).where(eq(setupVersions.id, versionIdB)).limit(1);

    if (!versionA) throw new AppError(404, "NOT_FOUND", "Version A not found");
    if (!versionB) throw new AppError(404, "NOT_FOUND", "Version B not found");

    // Get the car's parameter schema for labels/units
    const [setupA] = await db.select().from(setups).where(eq(setups.id, versionA.setupId)).limit(1);
    const [car] = setupA ? await db.select().from(cars).where(eq(cars.id, setupA.carId)).limit(1) : [null];

    const paramSchema = (car?.parameterSchema || {}) as Record<string, any>;
    const paramsA = (versionA.parameters || {}) as Record<string, unknown>;
    const paramsB = (versionB.parameters || {}) as Record<string, unknown>;

    // Collect all parameter keys from both versions
    const allKeys = new Set([...Object.keys(paramsA), ...Object.keys(paramsB)]);

    // Build comparison parameters grouped by category
    const categoryMap = new Map<string, ComparisonParameter[]>();
    let changedCount = 0;

    for (const key of allKeys) {
      const schema = paramSchema[key];
      const valA = paramsA[key] ?? null;
      const valB = paramsB[key] ?? null;
      const changed = JSON.stringify(valA) !== JSON.stringify(valB);

      if (changed) changedCount++;

      const category = schema?.category || "other";
      const label = schema?.label || key;
      const unit = schema?.unit || null;

      // Calculate numeric delta
      let delta: number | null = null;
      let deltaPercent: number | null = null;
      if (changed && typeof valA === "number" && typeof valB === "number") {
        delta = Number((valB - valA).toFixed(4));
        deltaPercent = valA !== 0 ? Number(((delta / valA) * 100).toFixed(1)) : null;
      }

      const param: ComparisonParameter = {
        key,
        label,
        unit,
        category,
        valueA: valA,
        valueB: valB,
        changed,
        delta,
        deltaPercent,
      };

      if (!categoryMap.has(category)) categoryMap.set(category, []);
      categoryMap.get(category)!.push(param);
    }

    // Build categories array
    const categories: ComparisonCategory[] = [];
    const categoryOrder = ["tires", "suspension", "chassis", "brakes", "aero", "electronics", "differential", "fuel", "gearing", "other"];

    for (const catName of categoryOrder) {
      const params = categoryMap.get(catName);
      if (params && params.length > 0) {
        categories.push({
          name: catName,
          parameters: params,
          hasChanges: params.some((p) => p.changed),
        });
      }
    }

    // Any remaining categories not in the ordered list
    for (const [catName, params] of categoryMap) {
      if (!categoryOrder.includes(catName) && params.length > 0) {
        categories.push({
          name: catName,
          parameters: params,
          hasChanges: params.some((p) => p.changed),
        });
      }
    }

    const categoriesAffected = categories.filter((c) => c.hasChanges).map((c) => c.name);

    return {
      categories,
      summary: {
        totalParams: allKeys.size,
        changedParams: changedCount,
        categoriesAffected,
      },
    };
  }
}

export const compareService = new CompareService();
