import { createHash } from "node:crypto";
import { extname } from "node:path";

/** Compute SHA-256 hash of a buffer */
export function computeFileHash(buffer: Buffer): string {
  return createHash("sha256").update(buffer).digest("hex");
}

/** Get file extension (lowercase, with dot) */
export function getExtension(filename: string): string {
  return extname(filename).toLowerCase();
}
