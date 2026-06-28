import type { Config } from "tailwindcss";

export default {
  content: ["./index.html", "./src/**/*.{ts,tsx}"],
  theme: {
    extend: {
      colors: {
        // EGGCELLENT brand palette (synchronized with logo.svg)
        cream: "#f1f3d8",
        brand: {
          DEFAULT: "#ff0049",
          dark: "#d6003e",
        },
        ink: "#252422",
      },
      fontFamily: {
        // display — Montserrat (headings/large numbers, poster vibe like the logo,
        //   with Cyrillic — because League Spartan has NO Cyrillic and won't work here).
        // sans/body — Onest (all body text, full Cyrillic).
        // League Spartan / Aka-AcidGR remain only inside logo.svg.
        display: ["'Montserrat'", "system-ui", "sans-serif"],
        script: ["'Aka-AcidGR-FatItalic'", "cursive"],
        sans: ["'Onest'", "system-ui", "sans-serif"],
      },
      borderRadius: {
        pill: "999px",
      },
      keyframes: {
        "fade-up": {
          "0%": { opacity: "0", transform: "translateY(20px)" },
          "100%": { opacity: "1", transform: "translateY(0)" },
        },
        "pop-in": {
          "0%": { opacity: "0", transform: "scale(0.92)" },
          "100%": { opacity: "1", transform: "scale(1)" },
        },
        float: {
          "0%,100%": { transform: "translateY(0)" },
          "50%": { transform: "translateY(-10px)" },
        },
      },
      animation: {
        "fade-up": "fade-up 0.6s ease-out both",
        "pop-in": "pop-in 0.7s ease-out both",
        float: "float 4s ease-in-out infinite",
      },
    },
  },
  plugins: [],
} satisfies Config;
