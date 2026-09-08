import type { Metadata } from "next";

import "./globals.css";

export const metadata: Metadata = {
  title: "InmoNExo",
  description: "Real estate market intelligence for Lima",
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="es">
      <body className="bg-ink text-white antialiased">{children}</body>
    </html>
  );
}
