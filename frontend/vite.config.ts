// =============================================================================
// File: frontend/vite.config.ts
// Owner: [P4 - Frontend Core & Upload Engineer]
// Priority: Priority 1 (Vite Configuration)
// =============================================================================

import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";

export default defineConfig({
  plugins: [react()],
  server: {
    port: 5173,
    host: true,
  },
});
