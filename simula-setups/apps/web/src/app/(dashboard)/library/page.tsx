"use client";

import { useState, useEffect } from "react";
import Link from "next/link";
import { useSearchParams, useRouter } from "next/navigation";
import { useLibrary, useDeleteSetup, useToggleFavorite, useMoveToFolder, useFolders } from "@/hooks/use-library";
import { useCars, useTracks } from "@/hooks/use-data";

export default function LibraryPage() {
  const router = useRouter();
  const searchParams = useSearchParams();

  const [search, setSearch] = useState("");
  const [carFilter, setCarFilter] = useState("");
  const [trackFilter, setTrackFilter] = useState("");

  // Read filters from URL (for sidebar links like ?isFavorite=true or ?folder=...)
  const urlFavorite = searchParams.get("isFavorite");
  const urlFolder = searchParams.get("folder");

  const { data, isLoading, error } = useLibrary({
    search: search || undefined,
    carId: carFilter || undefined,
    trackId: trackFilter || undefined,
    isFavorite: urlFavorite === "true" ? "true" : undefined,
    folder: urlFolder || undefined,
    sortBy: "updatedAt",
    sortOrder: "desc",
  });

  const { data: carsData } = useCars("iracing");
  const { data: tracksData } = useTracks("iracing");
  const { data: foldersData } = useFolders();
  const deleteMutation = useDeleteSetup();
  const toggleFav = useToggleFavorite();
  const moveToFolder = useMoveToFolder();

  const items = data?.data || [];
  const cars = carsData?.data || [];
  const tracksList = tracksData?.data || [];
  const folders: { name: string; count: number }[] = foldersData?.data || [];

  // Active filter badge info
  const activeFilters: string[] = [];
  if (urlFavorite === "true") activeFilters.push("Favorites");
  if (urlFolder) activeFilters.push(`Folder: ${urlFolder}`);
  if (carFilter) {
    const car = cars.find((c: any) => c.id === carFilter);
    activeFilters.push(car?.name || "Car filter");
  }
  if (trackFilter) {
    const track = tracksList.find((t: any) => t.id === trackFilter);
    activeFilters.push(track?.name || "Track filter");
  }

  function clearFilters() {
    setSearch("");
    setCarFilter("");
    setTrackFilter("");
    router.push("/library");
  }

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
        <div>
          <h1 className="text-2xl font-bold">
            {urlFavorite === "true" ? "Favorites" : urlFolder ? `Folder: ${urlFolder}` : "Setup Library"}
          </h1>
          <p className="text-muted-foreground">
            {data?.pagination?.total || 0} setups
          </p>
        </div>
        <Link
          href="/library/new"
          className="inline-flex items-center justify-center gap-2 rounded-md bg-simula-600 px-4 py-2 text-sm font-medium text-white hover:bg-simula-700 transition-colors shrink-0"
        >
          <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24" strokeWidth={2}>
            <path strokeLinecap="round" strokeLinejoin="round" d="M12 4v16m8-8H4" />
          </svg>
          New Setup
        </Link>
      </div>

      {/* Active filter badges */}
      {activeFilters.length > 0 && (
        <div className="flex items-center gap-2 flex-wrap">
          {activeFilters.map((label) => (
            <span key={label} className="inline-flex items-center rounded-full bg-simula-100 dark:bg-simula-900/30 text-simula-700 dark:text-simula-300 px-3 py-1 text-xs font-medium">
              {label}
            </span>
          ))}
          <button
            onClick={clearFilters}
            className="text-xs text-muted-foreground hover:text-foreground transition-colors underline"
          >
            Clear all
          </button>
        </div>
      )}

      {/* Filters */}
      <div className="flex gap-3 flex-wrap">
        <input
          type="text"
          placeholder="Search setups..."
          value={search}
          onChange={(e) => setSearch(e.target.value)}
          className="rounded-md border border-input bg-background px-3 py-2 text-sm w-full sm:w-64 focus:outline-none focus:ring-2 focus:ring-ring"
        />
        <select
          value={carFilter}
          onChange={(e) => setCarFilter(e.target.value)}
          className="rounded-md border border-input bg-background px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-ring"
        >
          <option value="">All Cars</option>
          {cars.map((car: any) => (
            <option key={car.id} value={car.id}>{car.name}</option>
          ))}
        </select>
        <select
          value={trackFilter}
          onChange={(e) => setTrackFilter(e.target.value)}
          className="rounded-md border border-input bg-background px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-ring"
        >
          <option value="">All Tracks</option>
          {tracksList.map((track: any) => (
            <option key={track.id} value={track.id}>
              {track.name}{track.config ? ` (${track.config})` : ""}
            </option>
          ))}
        </select>
      </div>

      {/* Loading */}
      {isLoading && (
        <div className="text-center py-12 text-muted-foreground">Loading setups...</div>
      )}

      {/* Error */}
      {error && (
        <div className="rounded-lg bg-red-50 dark:bg-red-950/30 border border-red-200 p-4 text-red-600">
          Failed to load library: {(error as any).message}
        </div>
      )}

      {/* Empty State */}
      {!isLoading && items.length === 0 && (
        <div className="text-center py-16 space-y-4">
          <div className="text-6xl">
            {urlFavorite === "true" ? "\u2b50" : urlFolder ? "\ud83d\udcc2" : "\ud83c\udfce\ufe0f"}
          </div>
          <h2 className="text-xl font-semibold">
            {urlFavorite === "true" ? "No favorites yet" : urlFolder ? "This folder is empty" : "No setups yet"}
          </h2>
          <p className="text-muted-foreground">
            {urlFavorite === "true"
              ? "Star your favorite setups and they'll appear here"
              : urlFolder
                ? "Move setups into this folder to organize them"
                : "Upload your first iRacing setup to get started"}
          </p>
          {!urlFavorite && !urlFolder && (
            <Link
              href="/library/new"
              className="inline-flex items-center gap-2 rounded-md bg-simula-600 px-6 py-3 text-sm font-medium text-white hover:bg-simula-700 transition-colors"
            >
              Create First Setup
            </Link>
          )}
        </div>
      )}

      {/* Setup Grid */}
      {items.length > 0 && (
        <div className="grid grid-cols-1 sm:grid-cols-2 xl:grid-cols-3 gap-4">
          {items.map((item: any) => (
            <SetupCard
              key={item.setupId}
              item={item}
              folders={folders}
              onDelete={() => {
                if (confirm("Delete this setup?")) {
                  deleteMutation.mutate(item.setupId);
                }
              }}
              onToggleFavorite={() => toggleFav.mutate(item.setupId)}
              onMoveToFolder={(folder: string | null) => moveToFolder.mutate({ setupId: item.setupId, folder })}
            />
          ))}
        </div>
      )}

      {/* Pagination hint */}
      {data?.pagination && data.pagination.totalPages > 1 && (
        <div className="text-center text-sm text-muted-foreground pt-4">
          Page {data.pagination.page} of {data.pagination.totalPages}
        </div>
      )}
    </div>
  );
}

function SetupCard({
  item,
  folders,
  onDelete,
  onToggleFavorite,
  onMoveToFolder,
}: {
  item: any;
  folders: { name: string; count: number }[];
  onDelete: () => void;
  onToggleFavorite: () => void;
  onMoveToFolder: (folder: string | null) => void;
}) {
  const setup = item.setup;
  const car = setup?.car;
  const track = setup?.track;
  const [showFolderMenu, setShowFolderMenu] = useState(false);

  return (
    <div className="relative rounded-lg border bg-card hover:shadow-md transition-shadow group">
      <Link
        href={`/library/${setup?.id || item.setupId}`}
        className="block p-5"
      >
        <div className="flex items-start justify-between">
          <div className="space-y-1 min-w-0 flex-1 pr-8">
            <h3 className="font-semibold truncate group-hover:text-simula-600 transition-colors">
              {setup?.name || "Untitled"}
            </h3>
            <p className="text-sm text-muted-foreground truncate">
              {car?.name || "Unknown car"}
            </p>
            {track && (
              <p className="text-xs text-muted-foreground truncate">
                {track.name}{track.config ? ` (${track.config})` : ""}
              </p>
            )}
          </div>
        </div>

        {/* Tags */}
        {setup?.tags && setup.tags.length > 0 && (
          <div className="flex gap-1 mt-3 flex-wrap">
            {setup.tags.slice(0, 3).map((tag: string) => (
              <span key={tag} className="inline-flex items-center rounded-full bg-muted px-2 py-0.5 text-xs">
                {tag}
              </span>
            ))}
            {setup.tags.length > 3 && (
              <span className="text-xs text-muted-foreground">+{setup.tags.length - 3}</span>
            )}
          </div>
        )}

        {/* Folder badge */}
        {item.folder && (
          <div className="mt-2">
            <span className="inline-flex items-center gap-1 rounded bg-muted px-2 py-0.5 text-xs text-muted-foreground">
              <svg className="w-3 h-3" fill="none" stroke="currentColor" viewBox="0 0 24 24" strokeWidth={1.5}>
                <path strokeLinecap="round" strokeLinejoin="round" d="M2.25 12.75V12A2.25 2.25 0 014.5 9.75h15A2.25 2.25 0 0121.75 12v.75m-8.69-6.44l-2.12-2.12a1.5 1.5 0 00-1.061-.44H4.5A2.25 2.25 0 002.25 6v12a2.25 2.25 0 002.25 2.25h15A2.25 2.25 0 0021.75 18V9a2.25 2.25 0 00-2.25-2.25h-5.379a1.5 1.5 0 01-1.06-.44z" />
              </svg>
              {item.folder}
            </span>
          </div>
        )}

        {/* Footer */}
        <div className="flex items-center gap-2 mt-4 text-xs text-muted-foreground">
          <span className="uppercase font-medium text-simula-600 dark:text-simula-400">
            {setup?.sim || "iracing"}
          </span>
          {setup?.season && <span>S: {setup.season}</span>}
          <span className="ml-auto">
            {setup?.updatedAt ? new Date(setup.updatedAt).toLocaleDateString() : ""}
          </span>
        </div>
      </Link>

      {/* Action buttons (overlay top-right) */}
      <div className="absolute top-3 right-3 flex items-center gap-1">
        {/* Favorite */}
        <button
          onClick={(e) => { e.preventDefault(); e.stopPropagation(); onToggleFavorite(); }}
          className={`p-1.5 rounded-md transition-all ${
            item.isFavorite
              ? "text-amber-500 hover:text-amber-600"
              : "text-muted-foreground/40 hover:text-amber-500 opacity-0 group-hover:opacity-100"
          }`}
          title={item.isFavorite ? "Remove from favorites" : "Add to favorites"}
        >
          <svg
            className="w-4 h-4"
            fill={item.isFavorite ? "currentColor" : "none"}
            stroke="currentColor"
            viewBox="0 0 24 24"
            strokeWidth={1.5}
          >
            <path strokeLinecap="round" strokeLinejoin="round" d="M11.48 3.499a.562.562 0 011.04 0l2.125 5.111a.563.563 0 00.475.345l5.518.442c.499.04.701.663.321.988l-4.204 3.602a.563.563 0 00-.182.557l1.285 5.385a.562.562 0 01-.84.61l-4.725-2.885a.562.562 0 00-.586 0L6.982 20.54a.562.562 0 01-.84-.61l1.285-5.386a.562.562 0 00-.182-.557l-4.204-3.602a.562.562 0 01.321-.988l5.518-.442a.563.563 0 00.475-.345L11.48 3.5z" />
          </svg>
        </button>

        {/* Folder menu */}
        <div className="relative">
          <button
            onClick={(e) => { e.preventDefault(); e.stopPropagation(); setShowFolderMenu(!showFolderMenu); }}
            className="p-1.5 rounded-md text-muted-foreground/40 hover:text-foreground opacity-0 group-hover:opacity-100 transition-all"
            title="Move to folder"
          >
            <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24" strokeWidth={1.5}>
              <path strokeLinecap="round" strokeLinejoin="round" d="M2.25 12.75V12A2.25 2.25 0 014.5 9.75h15A2.25 2.25 0 0121.75 12v.75m-8.69-6.44l-2.12-2.12a1.5 1.5 0 00-1.061-.44H4.5A2.25 2.25 0 002.25 6v12a2.25 2.25 0 002.25 2.25h15A2.25 2.25 0 0021.75 18V9a2.25 2.25 0 00-2.25-2.25h-5.379a1.5 1.5 0 01-1.06-.44z" />
            </svg>
          </button>
          {showFolderMenu && (
            <>
              <div className="fixed inset-0 z-10" onClick={(e) => { e.stopPropagation(); setShowFolderMenu(false); }} />
              <div className="absolute right-0 top-full mt-1 z-20 w-48 rounded-md border bg-popover shadow-md py-1">
                <button
                  onClick={(e) => { e.preventDefault(); e.stopPropagation(); onMoveToFolder(null); setShowFolderMenu(false); }}
                  className="w-full text-left px-3 py-1.5 text-sm hover:bg-muted transition-colors text-muted-foreground"
                >
                  No folder
                </button>
                {folders.map((f) => (
                  <button
                    key={f.name}
                    onClick={(e) => { e.preventDefault(); e.stopPropagation(); onMoveToFolder(f.name); setShowFolderMenu(false); }}
                    className={`w-full text-left px-3 py-1.5 text-sm hover:bg-muted transition-colors ${
                      item.folder === f.name ? "text-simula-600 font-medium" : ""
                    }`}
                  >
                    {f.name}
                  </button>
                ))}
                <FolderInput
                  onSubmit={(name) => { onMoveToFolder(name); setShowFolderMenu(false); }}
                />
              </div>
            </>
          )}
        </div>

        {/* Delete */}
        <button
          onClick={(e) => { e.preventDefault(); e.stopPropagation(); onDelete(); }}
          className="p-1.5 rounded-md text-muted-foreground/40 hover:text-red-500 opacity-0 group-hover:opacity-100 transition-all"
          title="Delete"
        >
          <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24" strokeWidth={1.5}>
            <path strokeLinecap="round" strokeLinejoin="round" d="M14.74 9l-.346 9m-4.788 0L9.26 9m9.968-3.21c.342.052.682.107 1.022.166m-1.022-.165L18.16 19.673a2.25 2.25 0 01-2.244 2.077H8.084a2.25 2.25 0 01-2.244-2.077L4.772 5.79m14.456 0a48.108 48.108 0 00-3.478-.397m-12 .562c.34-.059.68-.114 1.022-.165m0 0a48.11 48.11 0 013.478-.397m7.5 0v-.916c0-1.18-.91-2.164-2.09-2.201a51.964 51.964 0 00-3.32 0c-1.18.037-2.09 1.022-2.09 2.201v.916m7.5 0a48.667 48.667 0 00-7.5 0" />
          </svg>
        </button>
      </div>
    </div>
  );
}

function FolderInput({ onSubmit }: { onSubmit: (name: string) => void }) {
  const [creating, setCreating] = useState(false);
  const [name, setName] = useState("");

  if (!creating) {
    return (
      <button
        onClick={(e) => { e.preventDefault(); e.stopPropagation(); setCreating(true); }}
        className="w-full text-left px-3 py-1.5 text-sm text-simula-600 hover:bg-muted transition-colors border-t mt-1 pt-1.5"
      >
        + New folder
      </button>
    );
  }

  return (
    <div className="px-3 py-1.5 border-t mt-1 pt-1.5">
      <input
        type="text"
        value={name}
        onChange={(e) => setName(e.target.value)}
        onKeyDown={(e) => {
          e.stopPropagation();
          if (e.key === "Enter" && name.trim()) {
            onSubmit(name.trim());
            setName("");
            setCreating(false);
          }
          if (e.key === "Escape") {
            setCreating(false);
            setName("");
          }
        }}
        placeholder="Folder name..."
        autoFocus
        className="w-full rounded border border-input bg-background px-2 py-1 text-xs focus:outline-none focus:ring-1 focus:ring-ring"
        onClick={(e) => e.stopPropagation()}
      />
    </div>
  );
}
