"use client";

import { Fragment, useMemo, useState } from "react";

import { PriceChart } from "@/components/PriceChart";
import { fetchProjectPriceHistory } from "@/lib/api";
import type { PriceSnapshot, Project } from "@/lib/types";

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

function snapshotPrice(s: PriceSnapshot): string {
  const sym = s.currency === "PEN" ? "S/" : s.currency;
  return `${sym} ${s.price.toLocaleString("es-PE")}`;
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
  const [expandedId, setExpandedId] = useState<string | null>(null);
  const [histories, setHistories] = useState<Record<string, PriceSnapshot[]>>({});
  const [historyState, setHistoryState] = useState<Record<string, "loading" | "error" | undefined>>({});

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

  async function toggleExpand(projectId: string) {
    if (expandedId === projectId) {
      setExpandedId(null);
      return;
    }
    setExpandedId(projectId);
    if (histories[projectId] !== undefined || historyState[projectId] === "loading") return;

    setHistoryState((s) => ({ ...s, [projectId]: "loading" }));
    try {
      const series = await fetchProjectPriceHistory(projectId);
      setHistories((h) => ({ ...h, [projectId]: series }));
      setHistoryState((s) => ({ ...s, [projectId]: undefined }));
    } catch {
      setHistoryState((s) => ({ ...s, [projectId]: "error" }));
    }
  }

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
              <th className="w-10 px-2 py-3" aria-label="Expandir histórico" />
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
                <td colSpan={7} className="px-4 py-6 text-center text-ink-muted">
                  Sin resultados
                </td>
              </tr>
            ) : (
              filtered.map((p) => (
                <Fragment key={p.id}>
                  <tr className="border-t border-ink-border hover:bg-[#1f2a3a]">
                    <td className="px-2 py-2.5">
                      <button
                        type="button"
                        onClick={() => toggleExpand(p.id)}
                        aria-expanded={expandedId === p.id}
                        aria-label={`Histórico de precios de ${p.project_name}`}
                        className="rounded px-1.5 py-0.5 text-ink-muted hover:bg-[#243044] hover:text-mint"
                      >
                        {expandedId === p.id ? "▾" : "▸"}
                      </button>
                    </td>
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
                  {expandedId === p.id && (
                    <tr className="border-t border-ink-border bg-[#161f2b]">
                      <td colSpan={7} className="px-4 py-4">
                        <h3 className="mb-2 text-xs font-semibold uppercase tracking-wider text-ink-muted">
                          Histórico de precios · {p.project_name}
                        </h3>
                        {historyState[p.id] === "loading" && (
                          <p className="text-sm text-ink-muted">Cargando histórico…</p>
                        )}
                        {historyState[p.id] === "error" && (
                          <p className="text-sm text-red-300">
                            No se pudo cargar el histórico de precios.
                          </p>
                        )}
                        {histories[p.id] !== undefined && historyState[p.id] === undefined && (
                          histories[p.id].length === 0 ? (
                            <p className="text-sm text-ink-muted">
                              Sin snapshots de precio para este proyecto todavía.
                            </p>
                          ) : (
                            <div className="space-y-3">
                              {histories[p.id].length > 1 && (
                                <PriceChart snapshots={histories[p.id]} />
                              )}
                              <div className="overflow-x-auto rounded-lg border border-ink-border">
                                <table className="min-w-full text-sm">
                                  <thead className="bg-[#121a24] text-left text-ink-muted">
                                    <tr>
                                      <th className="px-4 py-2 font-medium">Fecha</th>
                                      <th className="px-4 py-2 font-medium">Precio</th>
                                      <th className="px-4 py-2 font-medium">Fuente</th>
                                    </tr>
                                  </thead>
                                  <tbody>
                                    {[...histories[p.id]].reverse().map((s) => (
                                      <tr key={s.id} className="border-t border-ink-border">
                                        <td className="px-4 py-2 tabular-nums text-ink-muted">
                                          {new Date(s.recorded_at).toLocaleDateString("es-PE", {
                                            day: "2-digit",
                                            month: "short",
                                            year: "numeric",
                                          })}
                                        </td>
                                        <td className="px-4 py-2 tabular-nums">
                                          {snapshotPrice(s)}
                                        </td>
                                        <td className="px-4 py-2">
                                          {s.source_url ? (
                                            <a
                                              href={s.source_url}
                                              target="_blank"
                                              rel="noopener noreferrer"
                                              className="text-mint hover:underline"
                                            >
                                              Ver fuente
                                            </a>
                                          ) : (
                                            "—"
                                          )}
                                        </td>
                                      </tr>
                                    ))}
                                  </tbody>
                                </table>
                              </div>
                            </div>
                          )
                        )}
                      </td>
                    </tr>
                  )}
                </Fragment>
              ))
            )}
          </tbody>
        </table>
      </div>
    </section>
  );
}
