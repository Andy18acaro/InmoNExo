import type {
  DashboardData,
  DistrictStats,
  MarketEvent,
  Overview,
  PriceSnapshot,
  Project,
} from "./types";

const DEFAULT_API = "http://127.0.0.1:8100";

/** Server-side fetch target (Vercel binding or explicit URL). */
export function apiBaseUrl(): string {
  return (
    process.env.INMONEXO_API_URL ??
    process.env.NEXT_PUBLIC_API_URL ??
    DEFAULT_API
  );
}

/** Browser-visible API base (OpenAPI link, etc.). */
export function publicApiBaseUrl(): string {
  return process.env.NEXT_PUBLIC_API_URL ?? apiBaseUrl();
}

async function fetchJson<T>(path: string): Promise<T> {
  const res = await fetch(`${apiBaseUrl()}${path}`, { cache: "no-store" });
  if (!res.ok) {
    throw new Error(`API ${path} failed: ${res.status}`);
  }
  return res.json() as Promise<T>;
}

export async function fetchOverview(): Promise<Overview> {
  return fetchJson<Overview>("/analytics/overview");
}

export async function fetchDistricts(): Promise<DistrictStats[]> {
  return fetchJson<DistrictStats[]>("/analytics/districts");
}

export async function fetchProjects(): Promise<Project[]> {
  return fetchJson<Project[]>("/projects");
}

export async function fetchEvents(limit = 200): Promise<MarketEvent[]> {
  return fetchJson<MarketEvent[]>(`/events?limit=${limit}`);
}

export async function fetchProjectPriceHistory(projectId: string): Promise<PriceSnapshot[]> {
  return fetchJson<PriceSnapshot[]>(`/projects/${projectId}/price-history`);
}

export async function fetchDashboardData(): Promise<DashboardData> {
  const [overview, districts, projects, events] = await Promise.all([
    fetchOverview(),
    fetchDistricts(),
    fetchProjects(),
    fetchEvents(),
  ]);
  return { overview, districts, projects, events };
}
