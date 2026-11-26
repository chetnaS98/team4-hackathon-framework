import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";

// base "./" so the built dist/ opens from any folder.
export default defineConfig({ plugins: [react()], base: "./" });
