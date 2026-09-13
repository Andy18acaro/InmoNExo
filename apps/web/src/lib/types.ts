export type Overview = {
  company_count: number;
  project_count: number;
  projects_with_price: number;
  district_count: number;
  event_count: number;
  recent_event_count: number;
  last_scrape_at: string | null;
  last_scrape_status: string | null;
};

export type DistrictStats = {
  district: string;
  project_count: number;
  company_count: number;
  priced_project_count: number;
  min_price: number | null;
  max_price: number | null;
  avg_price: number | null;
};

export type Project = {
  id: string;
  company_id: string;
  company_name: string;
  project_name: string;
  project_url: string | null;
  district: string | null;
  city: string;
  address: string | null;
  project_status: string;
  source_url: string;
  price_min: number | null;
  price_max: number | null;
  currency: string | null;
  first_seen_at: string;
  last_seen_at: string;
};

export type MarketEvent = {
  id: string;
  event_type: string;
  entity_type: string;
  entity_id: string;
  previous_value: Record<string, unknown> | null;
  new_value: Record<string, unknown> | null;
  detected_at: string;
  project_name: string | null;
  company_name: string | null;
  district: string | null;
  source_url: string | null;
};

export type PriceSnapshot = {
  id: string;
  project_id: string | null;
  unit_id: string | null;
  price: number;
  currency: string;
  recorded_at: string;
  source_url: string | null;
};

export type DashboardData = {
  overview: Overview;
  districts: DistrictStats[];
  projects: Project[];
  events: MarketEvent[];
};
