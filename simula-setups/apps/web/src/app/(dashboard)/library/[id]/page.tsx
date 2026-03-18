"use client";

import { useState } from "react";
import { useParams, useRouter } from "next/navigation";
import Link from "next/link";
import { useSetup } from "@/hooks/use-library";
import { useVersions, useCreateVersion, useRevertVersion } from "@/hooks/use-versions";
import { useNotes, useCreateNote, useDeleteNote } from "@/hooks/use-notes";
import { useCompareVersions } from "@/hooks/use-compare";
import { SETUP_CATEGORIES } from "@simula-setups/types";

export default function SetupDetailPage() {
  const params = useParams();
  const setupId = params.id as string;
  const { data: setupData, isLoading } = useSetup(setupId);
  const { data: versionsData } = useVersions(setupId);

  const setup = setupData?.data;
  const versions = versionsData?.data?.versions || [];
  const currentVersionId = versionsData?.data?.currentVersionId;

  const [activeTab, setActiveTab] = useState<"parameters" | "versions" | "notes" | "compare">("parameters");

  if (isLoading) {
    return <div className="text-center py-12 text-muted-foreground">Loading setup...</div>;
  }

  if (!setup) {
    return <div className="text-center py-12 text-muted-foreground">Setup not found</div>;
  }

  const currentVersion = setup.currentVersion;
  const paramSchema = (setup.car?.parameterSchema || {}) as Record<string, any>;
  const currentParams = (currentVersion?.parameters || {}) as Record<string, any>;

  // Group params by category
  const paramsByCategory = Object.entries(paramSchema).reduce<Record<string, [string, any][]>>((acc, entry) => {
    const cat = entry[1].category || "other";
    if (!acc[cat]) acc[cat] = [];
    acc[cat].push(entry);
    return acc;
  }, {});

  return (
    <div className="space-y-6">
      {/* Breadcrumb + Header */}
      <div className="flex items-start justify-between">
        <div className="space-y-1">
          <div className="flex items-center gap-2 text-sm text-muted-foreground">
            <Link href="/library" className="hover:text-foreground transition-colors">Library</Link>
            <span>/</span>
            <span>{setup.name}</span>
          </div>
          <h1 className="text-2xl font-bold">{setup.name}</h1>
          <div className="flex items-center gap-3 text-sm text-muted-foreground">
            <span className="font-medium text-simula-600">{setup.car?.name}</span>
            {setup.track && <span>{setup.track.name}{setup.track.config ? ` (${setup.track.config})` : ""}</span>}
            {setup.season && <span>Season: {setup.season}</span>}
            {currentVersion && <span>v{currentVersion.versionNumber}</span>}
          </div>
          {setup.tags?.length > 0 && (
            <div className="flex gap-1 mt-1">
              {setup.tags.map((tag: string) => (
                <span key={tag} className="rounded-full bg-muted px-2 py-0.5 text-xs">{tag}</span>
              ))}
            </div>
          )}
        </div>
      </div>

      {/* Tabs */}
      <div className="flex gap-1 border-b">
        {(["parameters", "versions", "notes", "compare"] as const).map((tab) => (
          <button
            key={tab}
            onClick={() => setActiveTab(tab)}
            className={`px-4 py-2 text-sm font-medium border-b-2 transition-colors ${
              activeTab === tab
                ? "border-simula-600 text-simula-600"
                : "border-transparent text-muted-foreground hover:text-foreground"
            }`}
          >
            {tab === "parameters" ? "Parameters" : tab === "versions" ? `Versions (${versions.length})` : tab === "notes" ? "Notes" : "Compare"}
          </button>
        ))}
      </div>

      {/* Tab Content */}
      {activeTab === "parameters" && (
        <ParametersView paramSchema={paramSchema} params={currentParams} paramsByCategory={paramsByCategory} />
      )}
      {activeTab === "versions" && (
        <VersionsView setupId={setupId} versions={versions} currentVersionId={currentVersionId} paramSchema={paramSchema} currentParams={currentParams} />
      )}
      {activeTab === "notes" && currentVersion && (
        <NotesView setupId={setupId} versionId={currentVersion.id} />
      )}
      {activeTab === "compare" && (
        <CompareView setupId={setupId} versions={versions} />
      )}
    </div>
  );
}

function ParametersView({ paramSchema, params, paramsByCategory }: any) {
  return (
    <div className="space-y-6">
      {SETUP_CATEGORIES.map((cat) => {
        const catParams = paramsByCategory[cat];
        if (!catParams || catParams.length === 0) return null;
        const hasValues = catParams.some(([key]: [string]) => params[key] !== undefined && params[key] !== null && params[key] !== "");
        return (
          <div key={cat} className="rounded-lg border bg-card p-4">
            <h3 className="text-sm font-semibold uppercase text-muted-foreground tracking-wider mb-3">{cat}</h3>
            <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-4 gap-3">
              {catParams.map(([key, schema]: [string, any]) => {
                const val = params[key];
                return (
                  <div key={key} className="space-y-0.5">
                    <p className="text-xs text-muted-foreground">{schema.label}</p>
                    <p className="text-sm font-medium">
                      {val !== undefined && val !== null && val !== "" ? (
                        <>{val}{schema.unit ? <span className="text-muted-foreground ml-1">{schema.unit}</span> : null}</>
                      ) : (
                        <span className="text-muted-foreground">-</span>
                      )}
                    </p>
                  </div>
                );
              })}
            </div>
          </div>
        );
      })}
    </div>
  );
}

function VersionsView({ setupId, versions, currentVersionId, paramSchema, currentParams }: any) {
  const createVersion = useCreateVersion(setupId);
  const revertVersion = useRevertVersion(setupId);
  const [showNew, setShowNew] = useState(false);
  const [changelog, setChangelog] = useState("");

  return (
    <div className="space-y-4">
      <div className="flex justify-between items-center">
        <h3 className="font-semibold">Version History</h3>
        <button
          onClick={() => setShowNew(!showNew)}
          className="rounded-md bg-simula-600 px-4 py-1.5 text-sm font-medium text-white hover:bg-simula-700 transition-colors"
        >
          {showNew ? "Cancel" : "New Version"}
        </button>
      </div>

      {showNew && (
        <div className="rounded-lg border bg-card p-4 space-y-3">
          <p className="text-sm text-muted-foreground">Create a new version with the current parameters. You can modify parameters after creation.</p>
          <textarea
            value={changelog}
            onChange={(e) => setChangelog(e.target.value)}
            placeholder="What changed? (e.g., Reduced ARB front to D2 for better mid-corner rotation)"
            rows={2}
            className="w-full rounded-md border border-input bg-background px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-ring"
          />
          <button
            onClick={async () => {
              await createVersion.mutateAsync({ parameters: currentParams, changelog });
              setShowNew(false);
              setChangelog("");
            }}
            disabled={createVersion.isPending}
            className="rounded-md bg-simula-600 px-4 py-1.5 text-sm font-medium text-white hover:bg-simula-700 disabled:opacity-50 transition-colors"
          >
            {createVersion.isPending ? "Creating..." : "Create Version"}
          </button>
        </div>
      )}

      {/* Timeline */}
      <div className="space-y-2">
        {versions.map((v: any) => (
          <div key={v.id} className={`rounded-lg border p-4 ${v.id === currentVersionId ? "border-simula-300 bg-simula-50/50 dark:bg-simula-950/20" : "bg-card"}`}>
            <div className="flex items-center justify-between">
              <div className="space-y-0.5">
                <div className="flex items-center gap-2">
                  <span className="font-semibold text-sm">v{v.versionNumber}</span>
                  {v.id === currentVersionId && (
                    <span className="rounded-full bg-simula-100 text-simula-700 dark:bg-simula-900 dark:text-simula-300 px-2 py-0.5 text-xs font-medium">Current</span>
                  )}
                  <span className="text-xs text-muted-foreground">{v.source}</span>
                </div>
                {v.changelog && <p className="text-sm text-muted-foreground">{v.changelog}</p>}
                <p className="text-xs text-muted-foreground">{new Date(v.createdAt).toLocaleString()}</p>
              </div>
              {v.id !== currentVersionId && (
                <button
                  onClick={() => {
                    if (confirm(`Revert to version ${v.versionNumber}? This creates a new version.`)) {
                      revertVersion.mutate(v.id);
                    }
                  }}
                  className="rounded-md border px-3 py-1 text-xs font-medium hover:bg-muted transition-colors"
                >
                  Revert
                </button>
              )}
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}

function NotesView({ setupId, versionId }: { setupId: string; versionId: string }) {
  const { data, isLoading } = useNotes(setupId, versionId);
  const createNote = useCreateNote(setupId, versionId);
  const deleteNote = useDeleteNote(setupId, versionId);
  const [newNote, setNewNote] = useState("");

  const notes = data?.data || [];

  return (
    <div className="space-y-4">
      {/* New note */}
      <div className="rounded-lg border bg-card p-4 space-y-3">
        <textarea
          value={newNote}
          onChange={(e) => setNewNote(e.target.value)}
          placeholder="Add a note about this setup version... (Markdown supported)"
          rows={3}
          className="w-full rounded-md border border-input bg-background px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-ring"
        />
        <button
          onClick={async () => {
            if (!newNote.trim()) return;
            await createNote.mutateAsync(newNote);
            setNewNote("");
          }}
          disabled={!newNote.trim() || createNote.isPending}
          className="rounded-md bg-simula-600 px-4 py-1.5 text-sm font-medium text-white hover:bg-simula-700 disabled:opacity-50 transition-colors"
        >
          {createNote.isPending ? "Adding..." : "Add Note"}
        </button>
      </div>

      {/* Notes list */}
      {isLoading && <p className="text-sm text-muted-foreground">Loading notes...</p>}
      {notes.length === 0 && !isLoading && (
        <p className="text-center py-8 text-muted-foreground">No notes yet. Add your first note above.</p>
      )}
      {notes.map((note: any) => (
        <div key={note.id} className="rounded-lg border bg-card p-4">
          <div className="flex justify-between items-start">
            <p className="text-sm whitespace-pre-wrap">{note.content}</p>
            <button
              onClick={() => { if (confirm("Delete this note?")) deleteNote.mutate(note.id); }}
              className="text-muted-foreground hover:text-red-500 transition-colors ml-2 shrink-0"
            >
              <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24" strokeWidth={1.5}>
                <path strokeLinecap="round" strokeLinejoin="round" d="M6 18L18 6M6 6l12 12" />
              </svg>
            </button>
          </div>
          <p className="text-xs text-muted-foreground mt-2">{new Date(note.createdAt).toLocaleString()}</p>
        </div>
      ))}
    </div>
  );
}

function CompareView({ setupId, versions }: { setupId: string; versions: any[] }) {
  const [v1, setV1] = useState("");
  const [v2, setV2] = useState("");
  const { data, isLoading } = useCompareVersions(setupId, v1, v2);
  const result = data?.data;

  return (
    <div className="space-y-4">
      <div className="flex gap-3 items-end">
        <div className="space-y-1">
          <label className="text-xs font-medium text-muted-foreground">Version A</label>
          <select value={v1} onChange={(e) => setV1(e.target.value)} className="rounded-md border border-input bg-background px-3 py-1.5 text-sm focus:outline-none focus:ring-1 focus:ring-ring">
            <option value="">Select...</option>
            {versions.map((v: any) => (
              <option key={v.id} value={v.id}>v{v.versionNumber}{v.changelog ? ` - ${v.changelog.slice(0, 30)}` : ""}</option>
            ))}
          </select>
        </div>
        <span className="text-muted-foreground pb-1">vs</span>
        <div className="space-y-1">
          <label className="text-xs font-medium text-muted-foreground">Version B</label>
          <select value={v2} onChange={(e) => setV2(e.target.value)} className="rounded-md border border-input bg-background px-3 py-1.5 text-sm focus:outline-none focus:ring-1 focus:ring-ring">
            <option value="">Select...</option>
            {versions.map((v: any) => (
              <option key={v.id} value={v.id}>v{v.versionNumber}{v.changelog ? ` - ${v.changelog.slice(0, 30)}` : ""}</option>
            ))}
          </select>
        </div>
      </div>

      {isLoading && <p className="text-sm text-muted-foreground">Comparing...</p>}

      {result && (
        <div className="space-y-4">
          {/* Summary */}
          <div className="rounded-lg bg-muted/50 p-3 text-sm">
            <span className="font-medium">{result.summary.changedParams}</span> of {result.summary.totalParams} parameters changed across{" "}
            <span className="font-medium">{result.summary.categoriesAffected.length}</span> categories
          </div>

          {/* Categories */}
          {result.categories.map((cat: any) => (
            <div key={cat.name} className="rounded-lg border bg-card">
              <div className={`px-4 py-2 border-b flex items-center justify-between ${cat.hasChanges ? "" : "opacity-60"}`}>
                <h4 className="text-sm font-semibold uppercase">{cat.name}</h4>
                {cat.hasChanges && (
                  <span className="text-xs text-accent-500 font-medium">
                    {cat.parameters.filter((p: any) => p.changed).length} changed
                  </span>
                )}
              </div>
              <div className="divide-y overflow-x-auto">
                {cat.parameters.filter((p: any) => p.changed).map((p: any) => (
                  <div key={p.key} className="grid grid-cols-2 sm:grid-cols-4 gap-2 sm:gap-4 px-4 py-2 text-sm min-w-[400px]">
                    <span className="text-muted-foreground">{p.label}</span>
                    <span className="font-mono">{String(p.valueA ?? "-")}{p.unit ? ` ${p.unit}` : ""}</span>
                    <span className="font-mono font-medium">{String(p.valueB ?? "-")}{p.unit ? ` ${p.unit}` : ""}</span>
                    <span className={`font-mono text-xs ${p.delta && p.delta > 0 ? "text-green-600" : p.delta && p.delta < 0 ? "text-red-600" : ""}`}>
                      {p.delta !== null ? (p.delta > 0 ? "+" : "") + p.delta + (p.unit ? ` ${p.unit}` : "") : "changed"}
                    </span>
                  </div>
                ))}
                {!cat.hasChanges && (
                  <p className="px-4 py-2 text-xs text-muted-foreground">No changes</p>
                )}
              </div>
            </div>
          ))}
        </div>
      )}

      {!v1 || !v2 ? (
        <p className="text-center py-8 text-muted-foreground">Select two versions to compare</p>
      ) : null}
    </div>
  );
}
