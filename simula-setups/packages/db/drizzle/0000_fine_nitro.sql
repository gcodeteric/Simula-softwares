CREATE TYPE "public"."car_class" AS ENUM('gt3', 'gt4', 'lmp2', 'lmh', 'formula', 'touring', 'stock', 'other');--> statement-breakpoint
CREATE TYPE "public"."library_source" AS ENUM('created', 'purchased', 'shared', 'imported');--> statement-breakpoint
CREATE TYPE "public"."note_type" AS ENUM('manual', 'ai_suggestion', 'telemetry_linked');--> statement-breakpoint
CREATE TYPE "public"."sim" AS ENUM('iracing', 'acc', 'rfactor2', 'lmu');--> statement-breakpoint
CREATE TYPE "public"."track_type" AS ENUM('high_downforce', 'low_downforce', 'technical', 'mixed', 'oval', 'street');--> statement-breakpoint
CREATE TYPE "public"."version_source" AS ENUM('manual', 'import', 'marketplace_purchase', 'ai_generated');--> statement-breakpoint
CREATE TYPE "public"."visibility" AS ENUM('private', 'public', 'marketplace');--> statement-breakpoint
CREATE TABLE "cars" (
	"id" uuid PRIMARY KEY DEFAULT gen_random_uuid() NOT NULL,
	"sim" "sim" NOT NULL,
	"name" varchar(255) NOT NULL,
	"manufacturer" varchar(255) NOT NULL,
	"car_class" "car_class" NOT NULL,
	"parameter_schema" jsonb DEFAULT '{}'::jsonb NOT NULL,
	"metadata" jsonb DEFAULT '{}'::jsonb NOT NULL,
	"created_at" timestamp with time zone DEFAULT now() NOT NULL,
	"updated_at" timestamp with time zone DEFAULT now() NOT NULL
);
--> statement-breakpoint
CREATE TABLE "setup_notes" (
	"id" uuid PRIMARY KEY DEFAULT gen_random_uuid() NOT NULL,
	"setup_version_id" uuid NOT NULL,
	"session_id" uuid,
	"user_id" uuid NOT NULL,
	"type" "note_type" DEFAULT 'manual' NOT NULL,
	"content" text NOT NULL,
	"ai_suggestions" jsonb,
	"telemetry_summary" jsonb,
	"created_at" timestamp with time zone DEFAULT now() NOT NULL,
	"updated_at" timestamp with time zone DEFAULT now() NOT NULL
);
--> statement-breakpoint
CREATE TABLE "setup_versions" (
	"id" uuid PRIMARY KEY DEFAULT gen_random_uuid() NOT NULL,
	"setup_id" uuid NOT NULL,
	"version_number" integer NOT NULL,
	"parameters" jsonb DEFAULT '{}'::jsonb NOT NULL,
	"raw_file_key" varchar(512),
	"raw_file_hash" varchar(64),
	"changelog" text,
	"source" "version_source" DEFAULT 'manual' NOT NULL,
	"created_at" timestamp with time zone DEFAULT now() NOT NULL,
	"created_by" uuid NOT NULL
);
--> statement-breakpoint
CREATE TABLE "setups" (
	"id" uuid PRIMARY KEY DEFAULT gen_random_uuid() NOT NULL,
	"user_id" uuid NOT NULL,
	"car_id" uuid NOT NULL,
	"track_id" uuid,
	"sim" "sim" NOT NULL,
	"name" varchar(255) NOT NULL,
	"description" text,
	"tags" text[] DEFAULT '{}' NOT NULL,
	"season" varchar(20),
	"visibility" "visibility" DEFAULT 'private' NOT NULL,
	"is_baseline" boolean DEFAULT false NOT NULL,
	"current_version_id" uuid,
	"created_at" timestamp with time zone DEFAULT now() NOT NULL,
	"updated_at" timestamp with time zone DEFAULT now() NOT NULL,
	"deleted_at" timestamp with time zone
);
--> statement-breakpoint
CREATE TABLE "tracks" (
	"id" uuid PRIMARY KEY DEFAULT gen_random_uuid() NOT NULL,
	"sim" "sim" NOT NULL,
	"name" varchar(255) NOT NULL,
	"config" varchar(255),
	"country" varchar(100) DEFAULT '' NOT NULL,
	"track_type" "track_type" DEFAULT 'mixed' NOT NULL,
	"metadata" jsonb DEFAULT '{}'::jsonb NOT NULL,
	"created_at" timestamp with time zone DEFAULT now() NOT NULL,
	"updated_at" timestamp with time zone DEFAULT now() NOT NULL
);
--> statement-breakpoint
CREATE TABLE "user_library" (
	"id" uuid PRIMARY KEY DEFAULT gen_random_uuid() NOT NULL,
	"user_id" uuid NOT NULL,
	"setup_id" uuid NOT NULL,
	"source" "library_source" DEFAULT 'created' NOT NULL,
	"purchase_id" uuid,
	"is_favorite" boolean DEFAULT false NOT NULL,
	"folder" varchar(255),
	"added_at" timestamp with time zone DEFAULT now() NOT NULL,
	"last_used_at" timestamp with time zone
);
--> statement-breakpoint
CREATE TABLE "users" (
	"id" uuid PRIMARY KEY DEFAULT gen_random_uuid() NOT NULL,
	"email" varchar(255) NOT NULL,
	"name" varchar(255) NOT NULL,
	"avatar_url" text,
	"auth_provider" varchar(50) DEFAULT 'mock' NOT NULL,
	"external_id" varchar(255),
	"created_at" timestamp with time zone DEFAULT now() NOT NULL,
	"updated_at" timestamp with time zone DEFAULT now() NOT NULL,
	CONSTRAINT "users_email_unique" UNIQUE("email")
);
--> statement-breakpoint
ALTER TABLE "setup_notes" ADD CONSTRAINT "setup_notes_setup_version_id_setup_versions_id_fk" FOREIGN KEY ("setup_version_id") REFERENCES "public"."setup_versions"("id") ON DELETE cascade ON UPDATE no action;--> statement-breakpoint
ALTER TABLE "setup_notes" ADD CONSTRAINT "setup_notes_user_id_users_id_fk" FOREIGN KEY ("user_id") REFERENCES "public"."users"("id") ON DELETE cascade ON UPDATE no action;--> statement-breakpoint
ALTER TABLE "setup_versions" ADD CONSTRAINT "setup_versions_setup_id_setups_id_fk" FOREIGN KEY ("setup_id") REFERENCES "public"."setups"("id") ON DELETE cascade ON UPDATE no action;--> statement-breakpoint
ALTER TABLE "setup_versions" ADD CONSTRAINT "setup_versions_created_by_users_id_fk" FOREIGN KEY ("created_by") REFERENCES "public"."users"("id") ON DELETE no action ON UPDATE no action;--> statement-breakpoint
ALTER TABLE "setups" ADD CONSTRAINT "setups_user_id_users_id_fk" FOREIGN KEY ("user_id") REFERENCES "public"."users"("id") ON DELETE cascade ON UPDATE no action;--> statement-breakpoint
ALTER TABLE "setups" ADD CONSTRAINT "setups_car_id_cars_id_fk" FOREIGN KEY ("car_id") REFERENCES "public"."cars"("id") ON DELETE no action ON UPDATE no action;--> statement-breakpoint
ALTER TABLE "setups" ADD CONSTRAINT "setups_track_id_tracks_id_fk" FOREIGN KEY ("track_id") REFERENCES "public"."tracks"("id") ON DELETE no action ON UPDATE no action;--> statement-breakpoint
ALTER TABLE "user_library" ADD CONSTRAINT "user_library_user_id_users_id_fk" FOREIGN KEY ("user_id") REFERENCES "public"."users"("id") ON DELETE cascade ON UPDATE no action;--> statement-breakpoint
ALTER TABLE "user_library" ADD CONSTRAINT "user_library_setup_id_setups_id_fk" FOREIGN KEY ("setup_id") REFERENCES "public"."setups"("id") ON DELETE cascade ON UPDATE no action;--> statement-breakpoint
CREATE INDEX "cars_sim_idx" ON "cars" USING btree ("sim");--> statement-breakpoint
CREATE INDEX "cars_class_idx" ON "cars" USING btree ("car_class");--> statement-breakpoint
CREATE INDEX "setup_notes_version_id_idx" ON "setup_notes" USING btree ("setup_version_id");--> statement-breakpoint
CREATE INDEX "setup_notes_user_id_idx" ON "setup_notes" USING btree ("user_id");--> statement-breakpoint
CREATE INDEX "setup_versions_setup_id_idx" ON "setup_versions" USING btree ("setup_id");--> statement-breakpoint
CREATE INDEX "setup_versions_setup_version_idx" ON "setup_versions" USING btree ("setup_id","version_number");--> statement-breakpoint
CREATE INDEX "setups_user_id_idx" ON "setups" USING btree ("user_id");--> statement-breakpoint
CREATE INDEX "setups_car_id_idx" ON "setups" USING btree ("car_id");--> statement-breakpoint
CREATE INDEX "setups_track_id_idx" ON "setups" USING btree ("track_id");--> statement-breakpoint
CREATE INDEX "setups_sim_idx" ON "setups" USING btree ("sim");--> statement-breakpoint
CREATE INDEX "setups_tags_idx" ON "setups" USING btree ("tags");--> statement-breakpoint
CREATE INDEX "tracks_sim_idx" ON "tracks" USING btree ("sim");--> statement-breakpoint
CREATE UNIQUE INDEX "user_library_user_setup_idx" ON "user_library" USING btree ("user_id","setup_id");--> statement-breakpoint
CREATE INDEX "user_library_user_id_idx" ON "user_library" USING btree ("user_id");--> statement-breakpoint
CREATE INDEX "user_library_folder_idx" ON "user_library" USING btree ("user_id","folder");