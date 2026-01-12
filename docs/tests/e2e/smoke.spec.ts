import { test, expect } from '@playwright/test';

/**
 * Crash-smoke tests: verify pages load without crashes.
 * 
 * These tests check for:
 * - HTTP response is OK (2xx or 3xx)
 * - No uncaught page errors (pageerror event)
 * - No console.error messages
 * 
 * We deliberately avoid:
 * - Visual regression/snapshots
 * - Exact text matching
 * - UI element selectors
 */

// URLs to test across both locales
const routes = [
  '/',
  '/products/',
  '/pricing/',
  '/roi-calculator/',
  '/blog/',
  '/docs/',
];

const locales = ['en', 'de'];

// Helper to collect errors during page load
interface PageErrors {
  pageErrors: Error[];
  consoleErrors: string[];
}

async function collectPageErrors(page: any): Promise<PageErrors> {
  const errors: PageErrors = {
    pageErrors: [],
    consoleErrors: [],
  };

  page.on('pageerror', (error: Error) => {
    errors.pageErrors.push(error);
  });

  page.on('console', (msg: any) => {
    if (msg.type() === 'error') {
      errors.consoleErrors.push(msg.text());
    }
  });

  return errors;
}

// Test each route in each locale
for (const locale of locales) {
  test.describe(`Smoke tests - ${locale.toUpperCase()} locale`, () => {
    for (const route of routes) {
      test(`${route} loads without crashes`, async ({ page }) => {
        const errors = await collectPageErrors(page);
        
        // Navigate to the page with generous timeout
        const url = locale === 'en' ? route : `/${locale}${route}`;
        const response = await page.goto(url, {
          waitUntil: 'networkidle',
          timeout: 30000,
        });

        // Verify response is OK
        expect(response?.status(), `${url} should return OK status`).toBeLessThan(400);

        // Wait a bit for any delayed errors
        await page.waitForTimeout(1000);

        // Verify no page errors occurred
        expect(
          errors.pageErrors,
          `${url} should have no uncaught page errors`
        ).toHaveLength(0);

        // Verify no console.error messages
        expect(
          errors.consoleErrors,
          `${url} should have no console.error messages`
        ).toHaveLength(0);
      });
    }
  });
}
