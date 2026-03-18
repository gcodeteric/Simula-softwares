"use client";

import { useState } from "react";
import Link from "next/link";
import { usePathname } from "next/navigation";
import { useAuthStore } from "@/stores/auth";
import { useLibraryStats, useFolders } from "@/hooks/use-library";
import { cn } from "@/lib/utils";

const mainNav = [
  {
    href: "/library",
    label: "Library",
    icon: "M3 7v10a2 2 0 002 2h14a2 2 0 002-2V9a2 2 0 00-2-2h-6l-2-2H5a2 2 0 00-2 2z",
    matchExact: false,
    excludePaths: ["/library/new"],
  },
  {
    href: "/library/new",
    label: "New Setup",
    icon: "M12 4v16m8-8H4",
    matchExact: true,
  },
  {
    href: "/compare",
    label: "Compare",
    icon: "M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2",
    matchExact: true,
  },
];

function isActive(pathname: string, item: (typeof mainNav)[number]) {
  if (item.matchExact) return pathname === item.href;
  if (item.excludePaths?.some((p) => pathname.startsWith(p))) return false;
  return pathname.startsWith(item.href);
}

export function Sidebar() {
  const pathname = usePathname();
  const user = useAuthStore((s) => s.user);
  const logout = useAuthStore((s) => s.logout);
  const { data: statsData } = useLibraryStats();
  const { data: foldersData } = useFolders();

  const [foldersOpen, setFoldersOpen] = useState(true);

  const stats = statsData?.data || { total: 0, favorites: 0 };
  const folders: { name: string; count: number }[] = foldersData?.data || [];

  return (
    <>
      {/* Desktop sidebar */}
      <aside className="hidden lg:flex flex-col w-64 border-r bg-card h-screen sticky top-0 shrink-0">
        <SidebarContent
          pathname={pathname}
          user={user}
          logout={logout}
          stats={stats}
          folders={folders}
          foldersOpen={foldersOpen}
          setFoldersOpen={setFoldersOpen}
        />
      </aside>
    </>
  );
}

export function MobileHeader() {
  const pathname = usePathname();
  const user = useAuthStore((s) => s.user);
  const logout = useAuthStore((s) => s.logout);
  const { data: statsData } = useLibraryStats();
  const { data: foldersData } = useFolders();
  const [open, setOpen] = useState(false);
  const [foldersOpen, setFoldersOpen] = useState(true);

  const stats = statsData?.data || { total: 0, favorites: 0 };
  const folders: { name: string; count: number }[] = foldersData?.data || [];

  return (
    <div className="lg:hidden">
      {/* Top bar */}
      <div className="sticky top-0 z-40 flex items-center justify-between border-b bg-card px-4 py-3">
        <Link href="/library" className="flex items-center gap-2">
          <div className="w-7 h-7 rounded-lg bg-simula-600 flex items-center justify-center text-white font-bold text-xs">
            S
          </div>
          <span className="text-base font-semibold text-simula-700 dark:text-simula-400">
            Setups
          </span>
        </Link>
        <button
          onClick={() => setOpen(!open)}
          className="p-2 rounded-md text-muted-foreground hover:bg-muted hover:text-foreground transition-colors"
          aria-label="Toggle menu"
        >
          {open ? (
            <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24" strokeWidth={2}>
              <path strokeLinecap="round" strokeLinejoin="round" d="M6 18L18 6M6 6l12 12" />
            </svg>
          ) : (
            <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24" strokeWidth={2}>
              <path strokeLinecap="round" strokeLinejoin="round" d="M3.75 6.75h16.5M3.75 12h16.5m-16.5 5.25h16.5" />
            </svg>
          )}
        </button>
      </div>

      {/* Overlay */}
      {open && (
        <>
          <div className="fixed inset-0 z-40 bg-black/40" onClick={() => setOpen(false)} />
          <aside className="fixed inset-y-0 left-0 z-50 w-72 bg-card border-r flex flex-col animate-in slide-in-from-left duration-200">
            <SidebarContent
              pathname={pathname}
              user={user}
              logout={logout}
              stats={stats}
              folders={folders}
              foldersOpen={foldersOpen}
              setFoldersOpen={setFoldersOpen}
              onNavigate={() => setOpen(false)}
            />
          </aside>
        </>
      )}
    </div>
  );
}

interface SidebarContentProps {
  pathname: string;
  user: { id: string; email: string; name: string; avatarUrl: string | null } | null;
  logout: () => void;
  stats: { total: number; favorites: number };
  folders: { name: string; count: number }[];
  foldersOpen: boolean;
  setFoldersOpen: (v: boolean) => void;
  onNavigate?: () => void;
}

function SidebarContent({
  pathname,
  user,
  logout,
  stats,
  folders,
  foldersOpen,
  setFoldersOpen,
  onNavigate,
}: SidebarContentProps) {
  return (
    <>
      {/* Brand */}
      <div className="p-5 border-b">
        <Link href="/library" className="flex items-center gap-2" onClick={onNavigate}>
          <div className="w-8 h-8 rounded-lg bg-simula-600 flex items-center justify-center text-white font-bold text-sm">
            S
          </div>
          <span className="text-lg font-semibold text-simula-700 dark:text-simula-400">
            Setups
          </span>
        </Link>
      </div>

      {/* Main nav */}
      <nav className="flex-1 overflow-y-auto p-3 space-y-4">
        {/* Primary links */}
        <div className="space-y-0.5">
          {mainNav.map((item) => (
            <Link
              key={item.href}
              href={item.href}
              onClick={onNavigate}
              className={cn(
                "flex items-center gap-3 px-3 py-2 rounded-md text-sm font-medium transition-colors",
                isActive(pathname, item)
                  ? "bg-simula-50 text-simula-700 dark:bg-simula-950 dark:text-simula-300"
                  : "text-muted-foreground hover:bg-muted hover:text-foreground",
              )}
            >
              <svg className="w-5 h-5 shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24" strokeWidth={1.5}>
                <path strokeLinecap="round" strokeLinejoin="round" d={item.icon} />
              </svg>
              <span className="flex-1">{item.label}</span>
              {item.label === "Library" && stats.total > 0 && (
                <span className="text-xs font-medium bg-muted text-muted-foreground rounded-full px-2 py-0.5">
                  {stats.total}
                </span>
              )}
            </Link>
          ))}
        </div>

        {/* Quick filters */}
        <div className="space-y-0.5">
          <p className="px-3 text-xs font-semibold uppercase text-muted-foreground tracking-wider mb-1">
            Quick Filters
          </p>
          <Link
            href="/library?isFavorite=true"
            onClick={onNavigate}
            className={cn(
              "flex items-center gap-3 px-3 py-2 rounded-md text-sm font-medium transition-colors",
              pathname === "/library" && typeof window !== "undefined" && window.location.search.includes("isFavorite=true")
                ? "bg-simula-50 text-simula-700 dark:bg-simula-950 dark:text-simula-300"
                : "text-muted-foreground hover:bg-muted hover:text-foreground",
            )}
          >
            <svg className="w-5 h-5 shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24" strokeWidth={1.5}>
              <path strokeLinecap="round" strokeLinejoin="round" d="M11.48 3.499a.562.562 0 011.04 0l2.125 5.111a.563.563 0 00.475.345l5.518.442c.499.04.701.663.321.988l-4.204 3.602a.563.563 0 00-.182.557l1.285 5.385a.562.562 0 01-.84.61l-4.725-2.885a.562.562 0 00-.586 0L6.982 20.54a.562.562 0 01-.84-.61l1.285-5.386a.562.562 0 00-.182-.557l-4.204-3.602a.562.562 0 01.321-.988l5.518-.442a.563.563 0 00.475-.345L11.48 3.5z" />
            </svg>
            <span className="flex-1">Favorites</span>
            {stats.favorites > 0 && (
              <span className="text-xs font-medium bg-amber-100 text-amber-700 dark:bg-amber-900/30 dark:text-amber-400 rounded-full px-2 py-0.5">
                {stats.favorites}
              </span>
            )}
          </Link>
        </div>

        {/* Folders */}
        <div className="space-y-0.5">
          <button
            onClick={() => setFoldersOpen(!foldersOpen)}
            className="flex items-center justify-between w-full px-3 text-xs font-semibold uppercase text-muted-foreground tracking-wider mb-1 hover:text-foreground transition-colors"
          >
            <span>Folders</span>
            <svg
              className={cn("w-3.5 h-3.5 transition-transform", foldersOpen && "rotate-90")}
              fill="none"
              stroke="currentColor"
              viewBox="0 0 24 24"
              strokeWidth={2}
            >
              <path strokeLinecap="round" strokeLinejoin="round" d="M8.25 4.5l7.5 7.5-7.5 7.5" />
            </svg>
          </button>
          {foldersOpen && (
            <div className="space-y-0.5">
              {folders.length === 0 ? (
                <p className="px-3 py-2 text-xs text-muted-foreground italic">
                  No folders yet
                </p>
              ) : (
                folders.map((folder) => (
                  <Link
                    key={folder.name}
                    href={`/library?folder=${encodeURIComponent(folder.name)}`}
                    onClick={onNavigate}
                    className={cn(
                      "flex items-center gap-3 px-3 py-1.5 rounded-md text-sm transition-colors",
                      pathname === "/library" && typeof window !== "undefined" && window.location.search.includes(`folder=${encodeURIComponent(folder.name)}`)
                        ? "bg-simula-50 text-simula-700 dark:bg-simula-950 dark:text-simula-300"
                        : "text-muted-foreground hover:bg-muted hover:text-foreground",
                    )}
                  >
                    <svg className="w-4 h-4 shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24" strokeWidth={1.5}>
                      <path strokeLinecap="round" strokeLinejoin="round" d="M2.25 12.75V12A2.25 2.25 0 014.5 9.75h15A2.25 2.25 0 0121.75 12v.75m-8.69-6.44l-2.12-2.12a1.5 1.5 0 00-1.061-.44H4.5A2.25 2.25 0 002.25 6v12a2.25 2.25 0 002.25 2.25h15A2.25 2.25 0 0021.75 18V9a2.25 2.25 0 00-2.25-2.25h-5.379a1.5 1.5 0 01-1.06-.44z" />
                    </svg>
                    <span className="flex-1 truncate">{folder.name}</span>
                    <span className="text-xs text-muted-foreground">{folder.count}</span>
                  </Link>
                ))
              )}
            </div>
          )}
        </div>
      </nav>

      {/* User footer */}
      {user && (
        <div className="p-3 border-t">
          <div className="flex items-center gap-3 px-2">
            <div className="w-8 h-8 rounded-full bg-simula-100 dark:bg-simula-900 flex items-center justify-center text-simula-600 dark:text-simula-400 text-sm font-medium shrink-0">
              {user.name.charAt(0).toUpperCase()}
            </div>
            <div className="flex-1 min-w-0">
              <p className="text-sm font-medium truncate">{user.name}</p>
              <p className="text-xs text-muted-foreground truncate">{user.email}</p>
            </div>
            <button
              onClick={logout}
              className="text-muted-foreground hover:text-foreground transition-colors shrink-0"
              title="Sign out"
            >
              <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24" strokeWidth={1.5}>
                <path strokeLinecap="round" strokeLinejoin="round" d="M15.75 9V5.25A2.25 2.25 0 0013.5 3h-6a2.25 2.25 0 00-2.25 2.25v13.5A2.25 2.25 0 007.5 21h6a2.25 2.25 0 002.25-2.25V15m3 0l3-3m0 0l-3-3m3 3H9" />
              </svg>
            </button>
          </div>
        </div>
      )}
    </>
  );
}
