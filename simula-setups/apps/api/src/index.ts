import express from "express";
import cors from "cors";
import helmet from "helmet";
import morgan from "morgan";
import { env } from "./config/env.js";
import { redis } from "./lib/redis.js";
import { notFound, errorHandler } from "./middleware/error-handler.js";
import { healthRouter } from "./routes/health.js";
import { authRouter } from "./routes/auth.js";
import { carsRouter } from "./routes/cars.js";
import { libraryRouter } from "./routes/library.js";
import { versionsRouter } from "./routes/versions.js";
import { compareRouter } from "./routes/compare.js";
import { notesRouter } from "./routes/notes.js";

const app = express();

// ---- Global Middleware ----
app.use(helmet());
app.use(cors({
  origin: env.NODE_ENV === "development"
    ? ["http://localhost:3000", "http://localhost:3001"]
    : ["https://setups.simulaproject.com"],
  credentials: true,
}));
app.use(morgan(env.NODE_ENV === "development" ? "dev" : "combined"));
app.use(express.json({ limit: "10mb" }));
app.use(express.urlencoded({ extended: true }));

// ---- API Routes ----
app.use("/api/v1", healthRouter);
app.use("/api/v1", authRouter);
app.use("/api/v1", carsRouter);
app.use("/api/v1", libraryRouter);
app.use("/api/v1", versionsRouter);
app.use("/api/v1", compareRouter);
app.use("/api/v1", notesRouter);

// ---- Error Handling ----
app.use(notFound);
app.use(errorHandler);

// ---- Start Server ----
async function start() {
  try {
    // Connect Redis
    await redis.connect();

    app.listen(env.API_PORT, () => {
      console.log(`
╔═══════════════════════════════════════════════╗
║  Simula Setups API                            ║
║  Running on: http://localhost:${env.API_PORT}          ║
║  Environment: ${env.NODE_ENV.padEnd(31)}║
║  Storage: ${env.STORAGE_PROVIDER.padEnd(35)}║
║  Auth: ${env.AUTH_PROVIDER.padEnd(38)}║
╚═══════════════════════════════════════════════╝
      `);
    });
  } catch (err) {
    console.error("❌ Failed to start server:", err);
    process.exit(1);
  }
}

// Graceful shutdown
function shutdown(signal: string) {
  console.log(`\n${signal} received. Shutting down gracefully...`);
  redis.disconnect();
  process.exit(0);
}

process.on("SIGINT", () => shutdown("SIGINT"));
process.on("SIGTERM", () => shutdown("SIGTERM"));

start();
