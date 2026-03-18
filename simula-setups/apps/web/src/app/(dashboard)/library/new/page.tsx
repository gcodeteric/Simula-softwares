"use client";

import { useState } from "react";
import { useRouter } from "next/navigation";
import { useCars, useTracks } from "@/hooks/use-data";
import { useCreateSetup, useUploadSetup } from "@/hooks/use-library";
import { SETUP_CATEGORIES } from "@simula-setups/types";

export default function NewSetupPage() {
  const router = useRouter();
  const { data: carsData } = useCars("iracing");
  const { data: tracksData } = useTracks("iracing");
  const createMutation = useCreateSetup();
  const uploadMutation = useUploadSetup();

  const cars = carsData?.data || [];
  const tracks = tracksData?.data || [];

  const [step, setStep] = useState(1);
  const [file, setFile] = useState<File | null>(null);
  const [meta, setMeta] = useState({
    name: "",
    carId: "",
    trackId: "",
    sim: "iracing" as const,
    description: "",
    tags: "",
    season: "",
  });
  const [parameters, setParameters] = useState<Record<string, any>>({});
  const [error, setError] = useState("");

  const selectedCar = cars.find((c: any) => c.id === meta.carId);
  const paramSchema = (selectedCar?.parameterSchema || {}) as Record<string, any>;

  // Group parameters by category
  const paramsByCategory = Object.entries(paramSchema).reduce<Record<string, [string, any][]>>((acc, entry) => {
    const cat = entry[1].category || "other";
    if (!acc[cat]) acc[cat] = [];
    acc[cat].push(entry);
    return acc;
  }, {});

  async function handleSubmit() {
    setError("");
    try {
      const payload = {
        ...meta,
        trackId: meta.trackId || undefined,
        tags: meta.tags ? meta.tags.split(",").map((t: string) => t.trim()).filter(Boolean) : [],
        season: meta.season || undefined,
        parameters,
      };

      if (file) {
        await uploadMutation.mutateAsync({ file, data: payload });
      } else {
        await createMutation.mutateAsync(payload);
      }
      router.push("/library");
    } catch (err: any) {
      setError(err.message || "Failed to create setup");
    }
  }

  const isSubmitting = createMutation.isPending || uploadMutation.isPending;

  return (
    <div className="max-w-3xl space-y-6">
      <div>
        <h1 className="text-2xl font-bold">New Setup</h1>
        <p className="text-muted-foreground">Upload a .sto file or enter parameters manually</p>
      </div>

      {/* Steps indicator */}
      <div className="flex gap-2">
        {[1, 2, 3].map((s) => (
          <button
            key={s}
            onClick={() => s <= step && setStep(s)}
            className={`flex items-center gap-2 px-4 py-2 rounded-md text-sm font-medium transition-colors ${
              s === step ? "bg-simula-600 text-white" : s < step ? "bg-simula-100 text-simula-700" : "bg-muted text-muted-foreground"
            }`}
          >
            {s}. {s === 1 ? "Metadata" : s === 2 ? "Parameters" : "Review"}
          </button>
        ))}
      </div>

      {error && (
        <div className="rounded-lg bg-red-50 border border-red-200 p-3 text-sm text-red-600">{error}</div>
      )}

      {/* Step 1: Metadata */}
      {step === 1 && (
        <div className="rounded-lg border bg-card p-6 space-y-4">
          <h2 className="text-lg font-semibold">Setup Details</h2>

          {/* File upload */}
          <div className="space-y-2">
            <label className="text-sm font-medium">Setup File (.sto)</label>
            <div className="border-2 border-dashed rounded-lg p-6 text-center">
              {file ? (
                <div className="space-y-2">
                  <p className="text-sm font-medium">{file.name}</p>
                  <p className="text-xs text-muted-foreground">{(file.size / 1024).toFixed(1)} KB</p>
                  <button onClick={() => setFile(null)} className="text-xs text-red-500 hover:text-red-700">Remove</button>
                </div>
              ) : (
                <label className="cursor-pointer space-y-2 block">
                  <p className="text-sm text-muted-foreground">Drop a .sto file here or click to browse</p>
                  <p className="text-xs text-muted-foreground">(Optional - you can enter parameters manually)</p>
                  <input
                    type="file"
                    accept=".sto"
                    className="hidden"
                    onChange={(e) => setFile(e.target.files?.[0] || null)}
                  />
                </label>
              )}
            </div>
          </div>

          <div className="space-y-2">
            <label className="text-sm font-medium">Name *</label>
            <input
              type="text"
              value={meta.name}
              onChange={(e) => setMeta({ ...meta, name: e.target.value })}
              placeholder="e.g., Spa Wet Baseline"
              required
              className="w-full rounded-md border border-input bg-background px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-ring"
            />
          </div>

          <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
            <div className="space-y-2">
              <label className="text-sm font-medium">Car *</label>
              <select
                value={meta.carId}
                onChange={(e) => setMeta({ ...meta, carId: e.target.value })}
                required
                className="w-full rounded-md border border-input bg-background px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-ring"
              >
                <option value="">Select car...</option>
                {cars.map((car: any) => (
                  <option key={car.id} value={car.id}>{car.name}</option>
                ))}
              </select>
            </div>
            <div className="space-y-2">
              <label className="text-sm font-medium">Track</label>
              <select
                value={meta.trackId}
                onChange={(e) => setMeta({ ...meta, trackId: e.target.value })}
                className="w-full rounded-md border border-input bg-background px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-ring"
              >
                <option value="">Generic (no track)</option>
                {tracks.map((t: any) => (
                  <option key={t.id} value={t.id}>{t.name}{t.config ? ` (${t.config})` : ""}</option>
                ))}
              </select>
            </div>
          </div>

          <div className="space-y-2">
            <label className="text-sm font-medium">Description</label>
            <textarea
              value={meta.description}
              onChange={(e) => setMeta({ ...meta, description: e.target.value })}
              rows={2}
              placeholder="Notes about this setup..."
              className="w-full rounded-md border border-input bg-background px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-ring"
            />
          </div>

          <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
            <div className="space-y-2">
              <label className="text-sm font-medium">Tags</label>
              <input
                type="text"
                value={meta.tags}
                onChange={(e) => setMeta({ ...meta, tags: e.target.value })}
                placeholder="wet, qualifying, endurance"
                className="w-full rounded-md border border-input bg-background px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-ring"
              />
            </div>
            <div className="space-y-2">
              <label className="text-sm font-medium">Season</label>
              <input
                type="text"
                value={meta.season}
                onChange={(e) => setMeta({ ...meta, season: e.target.value })}
                placeholder="2026S1"
                className="w-full rounded-md border border-input bg-background px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-ring"
              />
            </div>
          </div>

          <div className="flex justify-end pt-2">
            <button
              onClick={() => setStep(2)}
              disabled={!meta.name || !meta.carId}
              className="rounded-md bg-simula-600 px-6 py-2 text-sm font-medium text-white hover:bg-simula-700 disabled:opacity-50 transition-colors"
            >
              Next: Parameters
            </button>
          </div>
        </div>
      )}

      {/* Step 2: Parameters */}
      {step === 2 && (
        <div className="rounded-lg border bg-card p-6 space-y-6">
          <h2 className="text-lg font-semibold">Setup Parameters</h2>
          {!selectedCar && (
            <p className="text-sm text-muted-foreground">Select a car first to see available parameters.</p>
          )}

          {SETUP_CATEGORIES.map((cat) => {
            const catParams = paramsByCategory[cat];
            if (!catParams || catParams.length === 0) return null;
            return (
              <div key={cat} className="space-y-3">
                <h3 className="text-sm font-semibold uppercase text-muted-foreground tracking-wider border-b pb-1">
                  {cat}
                </h3>
                <div className="grid grid-cols-2 md:grid-cols-3 gap-3">
                  {catParams.map(([key, schema]) => (
                    <div key={key} className="space-y-1">
                      <label className="text-xs font-medium text-muted-foreground">
                        {schema.label} {schema.unit ? `(${schema.unit})` : ""}
                      </label>
                      {schema.type === "discrete" ? (
                        <select
                          value={parameters[key] ?? ""}
                          onChange={(e) => setParameters({ ...parameters, [key]: e.target.value })}
                          className="w-full rounded-md border border-input bg-background px-2 py-1.5 text-sm focus:outline-none focus:ring-1 focus:ring-ring"
                        >
                          <option value="">-</option>
                          {schema.values?.map((v: string) => (
                            <option key={v} value={v}>{v}</option>
                          ))}
                        </select>
                      ) : (
                        <input
                          type="number"
                          value={parameters[key] ?? ""}
                          onChange={(e) => setParameters({ ...parameters, [key]: e.target.value ? Number(e.target.value) : undefined })}
                          min={schema.min}
                          max={schema.max}
                          step={schema.step || 1}
                          placeholder={schema.min !== undefined ? `${schema.min}-${schema.max}` : ""}
                          className="w-full rounded-md border border-input bg-background px-2 py-1.5 text-sm focus:outline-none focus:ring-1 focus:ring-ring"
                        />
                      )}
                    </div>
                  ))}
                </div>
              </div>
            );
          })}

          <div className="flex justify-between pt-2">
            <button onClick={() => setStep(1)} className="rounded-md border px-6 py-2 text-sm font-medium hover:bg-muted transition-colors">
              Back
            </button>
            <button
              onClick={() => setStep(3)}
              className="rounded-md bg-simula-600 px-6 py-2 text-sm font-medium text-white hover:bg-simula-700 transition-colors"
            >
              Next: Review
            </button>
          </div>
        </div>
      )}

      {/* Step 3: Review */}
      {step === 3 && (
        <div className="rounded-lg border bg-card p-6 space-y-4">
          <h2 className="text-lg font-semibold">Review & Create</h2>

          <dl className="grid grid-cols-1 sm:grid-cols-2 gap-x-6 gap-y-3 text-sm">
            <div>
              <dt className="text-muted-foreground">Name</dt>
              <dd className="font-medium">{meta.name}</dd>
            </div>
            <div>
              <dt className="text-muted-foreground">Car</dt>
              <dd className="font-medium">{selectedCar?.name || "-"}</dd>
            </div>
            <div>
              <dt className="text-muted-foreground">Track</dt>
              <dd className="font-medium">{tracks.find((t: any) => t.id === meta.trackId)?.name || "Generic"}</dd>
            </div>
            <div>
              <dt className="text-muted-foreground">File</dt>
              <dd className="font-medium">{file?.name || "None (manual entry)"}</dd>
            </div>
            <div>
              <dt className="text-muted-foreground">Parameters set</dt>
              <dd className="font-medium">{Object.keys(parameters).filter((k) => parameters[k] !== undefined && parameters[k] !== "").length}</dd>
            </div>
            <div>
              <dt className="text-muted-foreground">Tags</dt>
              <dd className="font-medium">{meta.tags || "None"}</dd>
            </div>
          </dl>

          <div className="flex justify-between pt-4">
            <button onClick={() => setStep(2)} className="rounded-md border px-6 py-2 text-sm font-medium hover:bg-muted transition-colors">
              Back
            </button>
            <button
              onClick={handleSubmit}
              disabled={isSubmitting}
              className="rounded-md bg-simula-600 px-8 py-2 text-sm font-medium text-white hover:bg-simula-700 disabled:opacity-50 transition-colors"
            >
              {isSubmitting ? "Creating..." : "Create Setup"}
            </button>
          </div>
        </div>
      )}
    </div>
  );
}
