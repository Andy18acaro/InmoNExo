import type { DashboardData, DistrictStats, Overview, Project } from "./types";

const DEFAULT_API = "http://127.0.0.1:8100";

export function apiBaseUrl(): string {
  return process.env.NEXT_PUBLIC_API_URL ?? DEFAULT_API;
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

export async function fetchDashboardData(): Promise<DashboardData> {
  const [overview, districts, projects] = await Promise.all([
    fetchOverview(),
    fetchDistricts(),
    fetchProjects(),
  ]);
  return { overview, districts, projects };
}
