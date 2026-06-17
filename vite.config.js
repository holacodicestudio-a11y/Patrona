import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";

// Esta app SIEMPRE es la de Producción (rosa).
export default defineConfig({
  plugins: [react()],
  base: "./",
  define: { __APP_ROLE__: JSON.stringify("productor") },
  build: { outDir: "dist", emptyOutDir: true },
});
