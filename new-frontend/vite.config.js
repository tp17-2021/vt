import { svelte } from '@sveltejs/vite-plugin-svelte';
import { defineConfig } from 'vite';

let basePath

// if process.env.VITE_BASE_PATH is not undefined, use it as the base path
if (process.env.VITE_BASE_PATH) {
  basePath = process.env.VITE_BASE_PATH + '/'
} else {
  basePath = '/'
}

export default defineConfig({
    server: {
        port: 5000,
    },
    
    plugins: [svelte()],
    base: basePath,
    build: {
        // generate sourcemap
        sourcemap: true
    }
});
