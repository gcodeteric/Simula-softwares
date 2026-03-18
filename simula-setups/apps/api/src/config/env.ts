import { z } from "zod";

const envSchema = z.object({
  NODE_ENV: z.enum(["development", "production", "test"]).default("development"),
  API_PORT: z.coerce.number().default(3001),
  DATABASE_URL: z.string().url(),
  REDIS_URL: z.string().default("redis://localhost:6379"),
  STORAGE_PROVIDER: z.enum(["local", "r2"]).default("local"),
  STORAGE_LOCAL_PATH: z.string().default("./storage"),
  AUTH_PROVIDER: z.enum(["mock", "hub"]).default("mock"),
  NEXTAUTH_SECRET: z.string().default("dev-secret-change-in-production"),
});

function loadEnv() {
  const parsed = envSchema.safeParse(process.env);
  if (!parsed.success) {
    console.error("❌ Invalid environment variables:");
    console.error(parsed.error.flatten().fieldErrors);
    process.exit(1);
  }
  return parsed.data;
}

export const env = loadEnv();
export type Env = z.infer<typeof envSchema>;
