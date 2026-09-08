import type { DistrictStats } from "@/lib/types";

function money(value: number | null, currency = "S/"): string {
  if (value == null) return "—";
  return `${currency} ${value.toLocaleString("es-PE")}`;
}

export function DistrictTable({ districts }: { districts: DistrictStats[] }) {
  return (
    <section>
      <h2 className="mb-3 text-xs font-semibold uppercase tracking-wider text-ink-muted">
        Por distrito
      </h2>
      <div className="overflow-x-auto rounded-xl border border-ink-border bg-ink-card">
        <table className="min-w-full text-sm">
          <thead className="bg-[#121a24] text-left text-ink-muted">
            <tr>
              <th className="px-4 py-3 font-medium">Distrito</th>
              <th className="px-4 py-3 font-medium">Proyectos</th>
              <th className="px-4 py-3 font-medium">Developers</th>
              <th className="px-4 py-3 font-medium">Precio min</th>
              <th className="px-4 py-3 font-medium">Precio max</th>
            </tr>
          </thead>
          <tbody>
            {districts.map((d) => (
              <tr key={d.district} className="border-t border-ink-border hover:bg-[#1f2a3a]">
                <td className="px-4 py-2.5">{d.district}</td>
                <td className="px-4 py-2.5 tabular-nums">{d.project_count}</td>
                <td className="px-4 py-2.5 tabular-nums">{d.company_count}</td>
                <td className="px-4 py-2.5 tabular-nums">{money(d.min_price)}</td>
                <td className="px-4 py-2.5 tabular-nums">{money(d.max_price)}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </section>
  );
}
