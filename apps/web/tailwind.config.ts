import type { Config } from "tailwindcss";

const config: Config = {
  content: ["./src/**/*.{js,ts,jsx,tsx,mdx}"],
  theme: {
    extend: {
      colors: {
        ink: {
          DEFAULT: "#0f1419",
          card: "#1a2332",
          border: "#2a3544",
          muted: "#8b9cb3",
        },
        mint: "#3dd68c",
      },
    },
  },
  plugins: [],
};

export default config;
