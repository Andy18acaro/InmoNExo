"use client";

import { useMemo, useState } from "react";

import type { Project } from "@/lib/types";

type SortKey = "project_name" | "company_name" | "district" | "project_status" | "price_min" | "last_seen_at";
type SortDir = "asc" | "desc";

const STATUS_LABELS: Record<string, string> = {
  PRE_SALE: "Pre venta",
  UNDER_CONSTRUCTION: "En construcción",
  READY_TO_MOVE: "Entrega inmediata",
  DELIVERED: "Entregado",
  UNKNOWN: "Desconocido",
};

function money(project: Project): string {
  if (project.price_min == null) return "—";
  const sym = project.currency === "PEN" || project.currency == null ? "S/" : project.currency;
  return `${sym} ${project.price_min.toLocaleString("es-PE")}`;
}

function compare(a: Project, b: Project, key: SortKey, dir: SortDir): number {
  const mul = dir === "asc" ? 1 : -1;
  const av = a[key];
  const bv = b[key];
  if (av == null && bv == null) return 0;
  if (av == null) return 1;
  if (bv == null) return -1;
  if (typeof av === "number" && typeof bv === "number") return (av - bv) * mul;
  return String(av).localeCompare(String(bv), "es") * mul;
}

export function ProjectExplorer({ projects }: { projects: Project[] }) {
  const [query, setQuery] = useState("");
  const [district, setDistrict] = useState("");
  const [status, setStatus] = useState("");
  const [sortKey, setSortKey] = useState<SortKey>("project_name");
  const [sortDir, setSortDir] = useState<SortDir>("asc");

  const districts = useMemo(
    () => [...new Set(projects.map((p) => p.district).filter(Boolean))].sort() as string[],
    [projects],
  );

  const statuses = useMemo(
    () => [...new Set(projects.map((p) => p.project_status))].sort(),
    [projects],
  );

  const filtered = useMemo(() => {
    const q = query.trim().toLowerCase();
    return projects
      .filter((p) => {
        if (district && p.district !== district) return false;
        if (status && p.project_status !== status) return false;
        if (!q) return true;
        const hay = `${p.project_name} ${p.company_name} ${p.district ?? ""}`.toLowerCase();
        return hay.includes(q);
      })
      .sort((a, b) => compare(a, b, sortKey, sortDir));
  }, [projects, query, district, status, sortKey, sortDir]);

  function toggleSort(key: SortKey) {
    if (sortKey === key) {
      setSortDir((d) => (d === "asc" ? "desc" : "asc"));
    } else {
      setSortKey(key);
      setSortDir("asc");
    }
  }

  function sortIndicator(key: SortKey) {
    if (sortKey !== key) return "";
    return sortDir === "asc" ? " ↑" : " ↓";
  }

  return (
    <section>
      <h2 className="mb-3 text-xs font-semibold uppercase tracking-wider text-ink-muted">
        Explorador de proyectos
      </h2>
      <div className="mb-3 flex flex-wrap gap-2">
        <input
          type="search"
          placeholder="Buscar proyecto o developer…"
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          className="min-w-[220px] flex-1 rounded-lg border border-ink-border bg-ink-card px-3 py-2 text-sm outline-none focus:border-mint"
        />
        <select
          value={district}
          onChange={(e) => setDistrict(e.target.value)}
          className="rounded-lg border border-ink-border bg-ink-card px-3 py-2 text-sm"
        >
          <option value="">Todos los distritos</option>
          {districts.map((d) => (
            <option key={d} value={d}>
              {d}
            </option>
          ))}
        </select>
        <select
          value={status}
          onChange={(e) => setStatus(e.target.value)}
          className="rounded-lg border border-ink-border bg-ink-card px-3 py-2 text-sm"
        >
          <option value="">Todos los estados</option>
          {statuses.map((s) => (
            <option key={s} value={s}>
              {STATUS_LABELS[s] ?? s}
            </option>
          ))}
        </select>
      </div>
      <p className="mb-2 text-xs text-ink-muted">{filtered.length} proyectos</p>
      <div className="overflow-x-auto rounded-xl border border-ink-border bg-ink-card">
        <table className="min-w-full text-sm">
          <thead className="bg-[#121a24] text-left text-ink-muted">
            <tr>
              {(
                [
                  ["project_name", "Proyecto"],
                  ["company_name", "Developer"],
                  ["district", "Distrito"],
                  ["project_status", "Estado"],
                  ["price_min", "Desde"],
                  ["last_seen_at", "Actualizado"],
                ] as const
              ).map(([key, label]) => (
                <th key={key} className="px-4 py-3 font-medium">
                  <button
                    type="button"
                    onClick={() => toggleSort(key)}
                    className="hover:text-mint"
                  >
                    {label}
                    {sortIndicator(key)}
                  </button>
                </th>
              ))}
            </tr>
          </thead>
          <tbody>
            {filtered.length === 0 ? (
              <tr>
                <td colSpan={6} className="px-4 py-6 text-center text-ink-muted">
                  Sin resultados
                </td>
              </tr>
            ) : (
              filtered.map((p) => (
                <tr key={p.id} className="border-t border-ink-border hover:bg-[#1f2a3a]">
                  <td className="px-4 py-2.5">
                    <a
                      href={p.project_url ?? p.source_url}
                      target="_blank"
                      rel="noopener noreferrer"
                      className="text-mint hover:underline"
                    >
                      {p.project_name}
                    </a>
                  </td>
                  <td className="px-4 py-2.5">{p.company_name}</td>
                  <td className="px-4 py-2.5">{p.district ?? "—"}</td>
                  <td className="px-4 py-2.5">
                    <span className="rounded-full bg-[#243044] px-2 py-0.5 text-xs text-mint">
                      {STATUS_LABELS[p.project_status] ?? p.project_status}
                    </span>
                  </td>
                  <td className="px-4 py-2.5 tabular-nums">{money(p)}</td>
                  <td className="px-4 py-2.5 tabular-nums text-ink-muted">
                    {new Date(p.last_seen_at).toLocaleDateString("es-PE")}
                  </td>
                </tr>
              ))
            )}
          </tbody>
        </table>
      </div>
    </section>
  );
}
