import { defineConfig } from "@playwright/test";

export default defineConfig({
  testDir: "./tests/browser",
  testMatch: "**/*.spec.mjs",
  fullyParallel: true,
  workers: 2,
  timeout: 60000,
  retries: 0,
  reporter: "list",
  use: {
    browserName: "chromium",
    // Optional fallback when the bundled Chromium download is blocked: point at
    // an installed browser channel, e.g. CV_TAILOR_BROWSER_CHANNEL=msedge.
    channel: process.env.CV_TAILOR_BROWSER_CHANNEL || undefined,
    baseURL: "http://127.0.0.1:8765",
    trace: "retain-on-failure",
    screenshot: "only-on-failure",
  },
  webServer: {
    command: "node tests/browser/server.mjs",
    url: "http://127.0.0.1:8765/health",
    reuseExistingServer: false,
  },
});
