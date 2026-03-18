import type { Request, Response, NextFunction } from "express";
import { db, users } from "@simula-setups/db";
import { eq } from "drizzle-orm";
import { AppError } from "./error-handler.js";
import { env } from "../config/env.js";

/**
 * Extends Express Request with authenticated user
 */
declare global {
  namespace Express {
    interface Request {
      user?: {
        id: string;
        email: string;
        name: string;
      };
    }
  }
}

/**
 * Auth middleware.
 *
 * In mock mode (development), accepts:
 * - X-Mock-User-Id header → looks up user by ID
 * - X-Mock-User-Email header → looks up user by email
 *
 * In production (Hub SSO), will validate JWT from HttpOnly cookie.
 */
export async function requireAuth(req: Request, _res: Response, next: NextFunction) {
  try {
    if (env.AUTH_PROVIDER === "mock") {
      const userId = req.headers["x-mock-user-id"] as string | undefined;
      const userEmail = req.headers["x-mock-user-email"] as string | undefined;

      if (!userId && !userEmail) {
        throw new AppError(401, "UNAUTHORIZED", "Authentication required. Provide X-Mock-User-Id or X-Mock-User-Email header.");
      }

      let user;
      if (userId) {
        [user] = await db.select().from(users).where(eq(users.id, userId)).limit(1);
      } else if (userEmail) {
        [user] = await db.select().from(users).where(eq(users.email, userEmail)).limit(1);
      }

      if (!user) {
        throw new AppError(401, "UNAUTHORIZED", "User not found");
      }

      req.user = {
        id: user.id,
        email: user.email,
        name: user.name,
      };

      return next();
    }

    // TODO: Hub SSO JWT validation
    throw new AppError(501, "NOT_IMPLEMENTED", "Hub SSO auth not yet implemented");
  } catch (err) {
    next(err);
  }
}

/**
 * Optional auth — attaches user if present but doesn't block.
 */
export async function optionalAuth(req: Request, _res: Response, next: NextFunction) {
  try {
    const userId = req.headers["x-mock-user-id"] as string | undefined;
    const userEmail = req.headers["x-mock-user-email"] as string | undefined;

    if (userId || userEmail) {
      let user;
      if (userId) {
        [user] = await db.select().from(users).where(eq(users.id, userId)).limit(1);
      } else if (userEmail) {
        [user] = await db.select().from(users).where(eq(users.email, userEmail)).limit(1);
      }

      if (user) {
        req.user = {
          id: user.id,
          email: user.email,
          name: user.name,
        };
      }
    }

    next();
  } catch {
    next();
  }
}
