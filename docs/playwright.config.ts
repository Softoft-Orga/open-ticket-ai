import { defineConfig, devices } from '@playwright/test';

const PORT = process.env.PORT ?? '4321';
const BASE_URL = process.env.PLAYWRIGHT_BASE_URL ?? `http://localhost:${PORT}`;

export default defineConfig({
  testDir: './tests/e2e',
  reporter: 'list',
  use: {
    baseURL: BASE_URL,
    viewport: { width: 1280, height: 720 },
    headless: true,
    trace: 'on-first-retry',
    actionTimeout: 30_000,
    navigationTimeout: 45_000,
    video: 'off',
    screenshot: 'off',
    launchOptions: {
      slowMo: 0,
    },
    contextOptions: {
      reducedMotion: 'reduce',
    },
    permissions: [],
  },
  fullyParallel: true,
  forbidOnly: !!process.env.CI,
  retries: process.env.CI ? 2 : 0,
  workers: process.env.CI ? 2 : undefined,
  projects: [
    {
      name: 'chromium',
      use: { ...devices['Desktop Chrome'] },
    },
  ],
  webServer: {
    command: process.platform === 'win32'
      ? 'pwsh -NoProfile -Command "Set-Location .; npm run docs:dev"'
      : 'npm run docs:dev',
    url: BASE_URL,
    reuseExistingServer: !process.env.CI,
    timeout: 120_000,
  },
});

