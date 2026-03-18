import { Router } from "express";
import { db, users } from "@simula-setups/db";
import { eq } from "drizzle-orm";
import { z } from "zod";
import { requireAuth } from "../middleware/auth.js";

const router = Router();

const loginSchema = z.object({
  email: z.string().email(),
  name: z.string().min(1).optional(),
  password: z.string().min(1), // Mock: accepted as-is
});

/**
 * POST /api/v1/auth/login
 * Mock auth: creates user if not exists, returns user data.
 * In production this will be replaced by Hub SSO token exchange.
 */
router.post("/auth/login", async (req, res, next) => {
  try {
    const { email, name } = loginSchema.parse(req.body);

    // Find existing user
    let [user] = await db
      .select()
      .from(users)
      .where(eq(users.email, email))
      .limit(1);

    // Auto-create if not exists (mock mode)
    if (!user) {
      const displayName = name || email.split("@")[0];
      [user] = await db
        .insert(users)
        .values({
          email,
          name: displayName,
          authProvider: "mock",
        })
        .returning();
    }

    res.json({
      success: true,
      data: {
        user: {
          id: user.id,
          email: user.email,
          name: user.name,
          avatarUrl: user.avatarUrl,
        },
      },
    });
  } catch (err) {
    next(err);
  }
});

/** GET /api/v1/auth/me — current authenticated user */
router.get("/auth/me", requireAuth, (req, res) => {
  res.json({
    success: true,
    data: req.user,
  });
});

/** GET /api/v1/auth/users — list users (dev/debug only) */
router.get("/auth/users", async (_req, res, next) => {
  try {
    const allUsers = await db.select({
      id: users.id,
      email: users.email,
      name: users.name,
    }).from(users);

    res.json({ success: true, data: allUsers });
  } catch (err) {
    next(err);
  }
});

export { router as authRouter };
