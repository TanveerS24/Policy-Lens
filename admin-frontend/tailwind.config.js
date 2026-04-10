/** @type {import('tailwindcss').Config} */
export default {
  content: ["./index.html", "./src/**/*.{ts,tsx}"],
  theme: {
    extend: {
      colors: {
        primary: "#1E88E5",
        secondary: "#42A5F5",
        background: "#F4F8FB",
        card: "#FFFFFF",
      },
    },
  },
  plugins: [],
};
