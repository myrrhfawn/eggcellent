import react from "@vitejs/plugin-react";
import { defineConfig } from "vite";
import svgr from "vite-plugin-svgr";

export default defineConfig({
  plugins: [
    react(),
    // dimensions:false — strip hardcoded width/height (Inkscape leaves mm),
    // control size via className. viewBox is preserved.
    svgr({ svgrOptions: { dimensions: false } }),
  ],
  server: {
    host: true,
    port: 5173,
    // Dev proxy to Django so that /api and /media work without CORS pain.
    proxy: {
      "/api": "http://localhost:8000",
      "/media": "http://localhost:8000",
      "/django-static": "http://localhost:8000",
    },
  },
});
