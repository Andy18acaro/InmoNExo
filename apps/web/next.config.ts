import type { NextConfig } from "next";

const vercelHost = process.env.VERCEL_URL;
const publicApiUrl =
  process.env.NEXT_PUBLIC_API_URL ??
  (vercelHost ? `https://${vercelHost}/svc` : undefined);

const nextConfig: NextConfig = {
  reactStrictMode: true,
  env: publicApiUrl ? { NEXT_PUBLIC_API_URL: publicApiUrl } : undefined,
};

export default nextConfig;
