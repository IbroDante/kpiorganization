import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';

// Both local Vite modes must forward inquiries to Flask, just as production does
// when Flask serves the built React files. The API key never reaches the browser.
const proxy = { '/api': 'http://127.0.0.1:5000' };
export default defineConfig({
  plugins: [react()],
  server: { host: '0.0.0.0', allowedHosts: true, proxy },
  preview: { host: '0.0.0.0', allowedHosts: true, proxy },
});
