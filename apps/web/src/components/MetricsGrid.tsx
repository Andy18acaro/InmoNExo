import type { Overview } from "@/lib/types";

type Metric = { label: string; value: number | string };

export function MetricsGrid({ overview }: { overview: Overview }) {
  const metrics: Metric[] = [
    { label: "Developers", value: overview.company_count },
    { label: "Proyectos", value: overview.project_count },
    { label: "Con precio", value: overview.projects_with_price },
    { label: "Distritos", value: overview.district_count },
    { label: "Eventos", value: overview.event_count },
  ];

  const freshness = overview.last_scrape_at
    ? `Último scrape: ${new Date(overview.last_scrape_at).toLocaleString("es-PE")} (${overview.last_scrape_status ?? "—"})`
    : "Sin scrapes registrados";

  return (
    <section>
      <div className="mb-3 flex flex-wrap items-end justify-between gap-2">
        <h2 className="text-xs font-semibold uppercase tracking-wider text-ink-muted">Overview</h2>
        <p className="text-sm text-ink-muted">{freshness}</p>
      </div>
      <div className="grid grid-cols-2 gap-3 sm:grid-cols-3 lg:grid-cols-5">
        {metrics.map((m) => (
          <div key={m.label} className="rounded-xl border border-ink-border bg-ink-card p-4">
            <p className="text-[0.65rem] uppercase tracking-wide text-ink-muted">{m.label}</p>
            <p className="mt-1 text-2xl font-semibold tabular-nums">{m.value}</p>
          </div>
        ))}
      </div>
    </section>
  );
}
