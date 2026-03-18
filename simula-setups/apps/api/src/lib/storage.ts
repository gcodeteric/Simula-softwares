import { mkdir, writeFile, readFile, unlink, stat } from "node:fs/promises";
import { join, dirname } from "node:path";
import { env } from "../config/env.js";

/**
 * Storage adapter interface.
 * Implementations: LocalStorage (dev), R2Storage (production).
 */
export interface IStorageAdapter {
  upload(key: string, buffer: Buffer, contentType?: string): Promise<string>;
  download(key: string): Promise<Buffer>;
  delete(key: string): Promise<void>;
  exists(key: string): Promise<boolean>;
}

/**
 * Local filesystem storage adapter for development.
 * Files are stored in STORAGE_LOCAL_PATH (default: ./storage).
 */
class LocalStorageAdapter implements IStorageAdapter {
  private basePath: string;

  constructor(basePath: string) {
    this.basePath = basePath;
  }

  private getFullPath(key: string): string {
    return join(this.basePath, key);
  }

  async upload(key: string, buffer: Buffer): Promise<string> {
    const fullPath = this.getFullPath(key);
    await mkdir(dirname(fullPath), { recursive: true });
    await writeFile(fullPath, buffer);
    return key;
  }

  async download(key: string): Promise<Buffer> {
    return readFile(this.getFullPath(key));
  }

  async delete(key: string): Promise<void> {
    try {
      await unlink(this.getFullPath(key));
    } catch (err: unknown) {
      if ((err as NodeJS.ErrnoException).code !== "ENOENT") throw err;
    }
  }

  async exists(key: string): Promise<boolean> {
    try {
      await stat(this.getFullPath(key));
      return true;
    } catch {
      return false;
    }
  }
}

/** Create the appropriate storage adapter based on config */
function createStorageAdapter(): IStorageAdapter {
  if (env.STORAGE_PROVIDER === "r2") {
    // TODO: Implement R2StorageAdapter when needed
    throw new Error("R2 storage not yet implemented. Use STORAGE_PROVIDER=local for development.");
  }
  return new LocalStorageAdapter(env.STORAGE_LOCAL_PATH);
}

export const storage = createStorageAdapter();
