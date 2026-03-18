"use client";

import { useState } from "react";
import { useLibrary } from "@/hooks/use-library";
import { useVersions } from "@/hooks/use-versions";
import { useCrossCompare } from "@/hooks/use-compare";

export default function ComparePage() {
  const { data: libraryData } = useLibrary({ pageSize: "100" });
  const items = libraryData?.data || [];

  const [setupIdA, setSetupIdA] = useState("");
  const [setupIdB, setSetupIdB] = useState("");
  const [versionA, setVersionA] = useState("");
  const [versionB, setVersionB] = useState("");

  const { data: versionsA } = useVersions(setupIdA);
  const { data: versionsB } = useVersions(setupIdB);
  const { data: compareData, isLoading } = useCrossCompare(versionA, versionB);

  const versA = versionsA?.data?.versions || [];
  const versB = versionsB?.data?.versions || [];
  const result = compareData?.data;

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-2xl font-bold">Compare Setups</h1>
        <p className="text-muted-foreground">Compare parameters between any two setups or versions</p>
      </div>

      {/* Selectors */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-4 md:gap-6">
        <div className="rounded-lg border bg-card p-4 space-y-3">
          <h3 className="font-semibold text-sm">Setup A</h3>
          <select
            value={setupIdA}
            onChange={(e) => { setSetupIdA(e.target.value); setVersionA(""); }}
            className="w-full rounded-md border border-input bg-background px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-ring"
          >
            <option value="">Select setup...</option>
            {items.map((item: any) => (
              <option key={item.setupId} value={item.setup?.id || item.setupId}>
                {item.setup?.name || "Untitled"} ({item.setup?.car?.name || "?"})
              </option>
            ))}
          </select>
          {versA.length > 0 && (
            <select
              value={versionA}
              onChange={(e) => setVersionA(e.target.value)}
              className="w-full rounded-md border border-input bg-background px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-ring"
            >
              <option value="">Select version...</option>
              {versA.map((v: any) => (
                <option key={v.id} value={v.id}>
                  v{v.versionNumber}{v.changelog ? ` - ${v.changelog.slice(0, 40)}` : ""}
                </option>
              ))}
            </select>
          )}
        </div>

        <div className="rounded-lg border bg-card p-4 space-y-3">
          <h3 className="font-semibold text-sm">Setup B</h3>
          <select
            value={setupIdB}
            onChange={(e) => { setSetupIdB(e.target.value); setVersionB(""); }}
            className="w-full rounded-md border border-input bg-background px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-ring"
          >
            <option value="">Select setup...</option>
            {items.map((item: any) => (
              <option key={item.setupId} value={item.setup?.id || item.setupId}>
                {item.setup?.name || "Untitled"} ({item.setup?.car?.name || "?"})
              </option>
            ))}
          </select>
          {versB.length > 0 && (
            <select
              value={versionB}
              onChange={(e) => setVersionB(e.target.value)}
              className="w-full rounded-md border border-input bg-background px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-ring"
            >
              <option value="">Select version...</option>
              {versB.map((v: any) => (
                <option key={v.id} value={v.id}>
                  v{v.versionNumber}{v.changelog ? ` - ${v.changelog.slice(0, 40)}` : ""}
                </option>
              ))}
            </select>
          )}
        </div>
      </div>

      {isLoading && <p className="text-center py-8 text-muted-foreground">Comparing...</p>}

      {/* Results */}
      {result && (
        <div className="space-y-4">
          <div className="rounded-lg bg-muted/50 p-3 text-sm">
            <span className="font-medium">{result.summary.changedParams}</span> of {result.summary.totalParams} parameters changed
          </div>

          {result.categories.map((cat: any) => (
            <div key={cat.name} className="rounded-lg border bg-card">
              <div className="px-4 py-2 border-b">
                <h4 className="text-sm font-semibold uppercase">{cat.name}</h4>
              </div>
              <div className="overflow-x-auto">
              <table className="w-full text-sm min-w-[500px]">
                <thead>
                  <tr className="text-xs text-muted-foreground border-b">
                    <th className="text-left px-4 py-1.5 font-medium">Parameter</th>
                    <th className="text-left px-4 py-1.5 font-medium">Setup A</th>
                    <th className="text-left px-4 py-1.5 font-medium">Setup B</th>
                    <th className="text-left px-4 py-1.5 font-medium">Delta</th>
                  </tr>
                </thead>
                <tbody className="divide-y">
                  {cat.parameters.map((p: any) => (
                    <tr key={p.key} className={p.changed ? "bg-amber-50/50 dark:bg-amber-950/10" : "opacity-60"}>
                      <td className="px-4 py-1.5 text-muted-foreground">{p.label}</td>
                      <td className="px-4 py-1.5 font-mono">{String(p.valueA ?? "-")}</td>
                      <td className="px-4 py-1.5 font-mono font-medium">{String(p.valueB ?? "-")}</td>
                      <td className={`px-4 py-1.5 font-mono text-xs ${p.delta && p.delta > 0 ? "text-green-600" : p.delta && p.delta < 0 ? "text-red-600" : ""}`}>
                        {p.changed ? (p.delta !== null ? (p.delta > 0 ? "+" : "") + p.delta : "changed") : ""}
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
              </div>
            </div>
          ))}
        </div>
      )}

      {(!versionA || !versionB) && !result && (
        <p className="text-center py-12 text-muted-foreground">
          Select two setups and their versions to compare parameters
        </p>
      )}
    </div>
  );
}
