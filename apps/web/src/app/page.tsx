import "@/app/globals.css";

import type { Metadata } from "next";

import { DistrictTable } from "@/components/DistrictTable";
import { EventsFeed } from "@/components/EventsFeed";
import { MetricsGrid } from "@/components/MetricsGrid";
import { ProjectExplorer } from "@/components/ProjectExplorer";
import { StatusBreakdown } from "@/components/StatusBreakdown";
import { apiBaseUrl, fetchDashboardData, publicApiBaseUrl } from "@/lib/api";

export const metadata: Metadata = {
  title: "InmoNExo — Market Intelligence Lima",
  description: "Dashboard de inteligencia inmobiliaria para developers en Lima",
};

export default async function HomePage() {
  let data;
  let error: string | null = null;

  try {
    data = await fetchDashboardData();
  } catch (e) {
    error = e instanceof Error ? e.message : "Error cargando datos";
  }

  return (
    <div className="min-h-screen">
      <header className="border-b border-ink-border px-6 py-5 sm:px-8">
        <div className="mx-auto flex max-w-6xl flex-wrap items-end justify-between gap-3">
          <div>
            <h1 className="text-xl font-semibold">
              Inmo<span className="text-mint">NExo</span>
            </h1>
            <p className="text-sm text-ink-muted">Inteligencia de mercado — 5 developers Lima</p>
          </div>
          <a
            href={`${publicApiBaseUrl()}/docs`}
            target="_blank"
            rel="noopener noreferrer"
            className="text-sm text-mint hover:underline"
          >
            OpenAPI
          </a>
        </div>
      </header>

      <main className="mx-auto max-w-6xl space-y-8 px-6 py-8 sm:px-8">
        {error ? (
          <div className="rounded-xl border border-red-900/50 bg-red-950/30 p-4 text-sm">
            <p className="font-medium text-red-300">No se pudo conectar con la API</p>
            <p className="mt-1 text-ink-muted">{error}</p>
            <p className="mt-3 text-ink-muted">
              Asegúrate de tener la API en {apiBaseUrl()} y datos con{" "}
              <code className="text-mint">python infrastructure/scripts/seed_demo.py</code>
            </p>
          </div>
        ) : (
          data && (
            <>
              <MetricsGrid overview={data.overview} />
              <div className="grid gap-8 lg:grid-cols-2">
                <DistrictTable districts={data.districts} />
                <StatusBreakdown projects={data.projects} />
              </div>
              <ProjectExplorer projects={data.projects} />
              <EventsFeed events={data.events} />
            </>
          )
        )}
      </main>

      <footer className="px-6 py-8 text-center text-xs text-ink-muted">
        Datos públicos · No marketplace
      </footer>
    </div>
  );
}
