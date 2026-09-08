import type { Project } from "@/lib/types";

const STATUS_LABELS: Record<string, string> = {
  PRE_SALE: "Pre venta",
  UNDER_CONSTRUCTION: "En construcción",
  READY_TO_MOVE: "Entrega inmediata",
  DELIVERED: "Entregado",
  UNKNOWN: "Desconocido",
};

export function StatusBreakdown({ projects }: { projects: Project[] }) {
  const counts = projects.reduce<Record<string, number>>((acc, p) => {
    acc[p.project_status] = (acc[p.project_status] ?? 0) + 1;
    return acc;
  }, {});

  const rows = Object.entries(counts).sort((a, b) => b[1] - a[1]);

  return (
    <section>
      <h2 className="mb-3 text-xs font-semibold uppercase tracking-wider text-ink-muted">
        Por estado
      </h2>
      <div className="flex flex-wrap gap-2">
        {rows.map(([status, count]) => (
          <div
            key={status}
            className="rounded-lg border border-ink-border bg-ink-card px-3 py-2 text-sm"
          >
            <span className="text-ink-muted">{STATUS_LABELS[status] ?? status}</span>
            <span className="ml-2 font-semibold tabular-nums text-mint">{count}</span>
          </div>
        ))}
      </div>
    </section>
  );
}
