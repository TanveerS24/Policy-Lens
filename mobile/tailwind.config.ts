import type { Config } from "tailwindcss";

export default {
  content: ["./App.{js,jsx,ts,tsx}", "./src/**/*.{js,jsx,ts,tsx}"],
  theme: {
    extend: {
      colors: {
        primary: "#1E88E5",
        secondary: "#42A5F5",
        background: "#F4F8FB",
        card: "#FFFFFF",
        text: "#1A1A1A",
      },
      boxShadow: {
        soft: "0 8px 20px rgba(0,0,0,0.05)",
      },
      borderRadius: {
        xl: "18px",
      },
    },
  },
  plugins: [],
} satisfies Config;
