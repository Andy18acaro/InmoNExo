"use client";

import { useMemo, useState } from "react";

import type { MarketEvent } from "@/lib/types";

const EVENT_LABELS: Record<string, string> = {
  NEW_PROJECT: "Nuevo proyecto",
  PRICE_CHANGE: "Cambio de precio",
  PROJECT_STATUS_CHANGE: "Cambio de estado",
  PROJECT_REMOVED: "Proyecto retirado",
  NEW_UNIT_TYPE: "Nueva tipología",
  PRICE_REMOVED: "Precio retirado",
};

function label(eventType: string): string {
  return EVENT_LABELS[eventType] ?? eventType;
}

export function EventsFeed({ events }: { events: MarketEvent[] }) {
  const [eventType, setEventType] = useState("");
  const [district, setDistrict] = useState("");

  const eventTypes = useMemo(
    () => [...new Set(events.map((e) => e.event_type))].sort(),
    [events],
  );

  const districts = useMemo(
    () => [...new Set(events.map((e) => e.district).filter(Boolean))].sort() as string[],
    [events],
  );

  const filtered = useMemo(
    () =>
      events.filter((e) => {
        if (eventType && e.event_type !== eventType) return false;
        if (district && e.district !== district) return false;
        return true;
      }),
    [events, eventType, district],
  );

  return (
    <section>
      <h2 className="mb-3 text-xs font-semibold uppercase tracking-wider text-ink-muted">
        Eventos de mercado
      </h2>
      {events.length === 0 ? (
        <p className="rounded-xl border border-ink-border bg-ink-card px-4 py-6 text-center text-sm text-ink-muted">
          Sin eventos detectados todavía. La actividad aparece cuando el scraper detecta
          proyectos nuevos, cambios de precio o de estado.
        </p>
      ) : (
        <>
          <div className="mb-3 flex flex-wrap gap-2">
            <select
              value={eventType}
              onChange={(e) => setEventType(e.target.value)}
              className="rounded-lg border border-ink-border bg-ink-card px-3 py-2 text-sm"
            >
              <option value="">Todos los eventos</option>
              {eventTypes.map((t) => (
                <option key={t} value={t}>
                  {label(t)}
                </option>
              ))}
            </select>
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
          </div>
          <p className="mb-2 text-xs text-ink-muted">{filtered.length} eventos</p>
          <div className="overflow-x-auto rounded-xl border border-ink-border bg-ink-card">
            <table className="min-w-full text-sm">
              <thead className="bg-[#121a24] text-left text-ink-muted">
                <tr>
                  <th className="px-4 py-3 font-medium">Evento</th>
                  <th className="px-4 py-3 font-medium">Proyecto</th>
                  <th className="px-4 py-3 font-medium">Developer</th>
                  <th className="px-4 py-3 font-medium">Distrito</th>
                  <th className="px-4 py-3 font-medium">Detectado</th>
                </tr>
              </thead>
              <tbody>
                {filtered.length === 0 ? (
                  <tr>
                    <td colSpan={5} className="px-4 py-6 text-center text-ink-muted">
                      Sin eventos que coincidan con los filtros
                    </td>
                  </tr>
                ) : (
                  filtered.map((e) => (
                    <tr key={e.id} className="border-t border-ink-border hover:bg-[#1f2a3a]">
                      <td className="px-4 py-2.5">
                        <span className="rounded-full bg-[#243044] px-2 py-0.5 text-xs text-mint">
                          {label(e.event_type)}
                        </span>
                      </td>
                      <td className="px-4 py-2.5">
                        {e.source_url ? (
                          <a
                            href={e.source_url}
                            target="_blank"
                            rel="noopener noreferrer"
                            className="text-mint hover:underline"
                          >
                            {e.project_name ?? e.entity_id}
                          </a>
                        ) : (
                          e.project_name ?? "—"
                        )}
                      </td>
                      <td className="px-4 py-2.5">{e.company_name ?? "—"}</td>
                      <td className="px-4 py-2.5">{e.district ?? "—"}</td>
                      <td className="px-4 py-2.5 tabular-nums text-ink-muted">
                        {new Date(e.detected_at).toLocaleDateString("es-PE", {
                          day: "2-digit",
                          month: "short",
                          year: "numeric",
                        })}
                      </td>
                    </tr>
                  ))
                )}
              </tbody>
            </table>
          </div>
        </>
      )}
    </section>
  );
}
