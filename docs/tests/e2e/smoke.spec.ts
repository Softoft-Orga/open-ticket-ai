import { test, expect, Page, ConsoleMessage } from '@playwright/test';
import { readdirSync } from 'fs';
import { join, relative } from 'path';

/**
 * Crash-smoke tests: verify pages load without crashes.
 *
 * These tests check for:
 * - HTTP response is OK (2xx or 3xx)
 * - No uncaught page errors (pageerror event)
 * - No JavaScript console.error messages (excluding resource load failures)
 *
 * We deliberately avoid:
 * - Visual regression/snapshots
 * - Exact text matching
 * - UI element selectors
 *
 * Resource loading errors (404s for images, fonts, etc.) are filtered out
 * as they don't indicate page crashes.
 */

/**
 * Recursively scan the pages directory to discover all routes.
 * Converts file paths to URL routes, excluding dynamic routes ([...slug]).
 */
function discoverRoutes(dir: string, baseDir: string): string[] {
  const routes: string[] = [];
  const entries = readdirSync(dir, { withFileTypes: true });

  for (const entry of entries) {
    const fullPath = join(dir, entry.name);

    if (entry.isDirectory()) {
      // Recursively scan subdirectories
      routes.push(...discoverRoutes(fullPath, baseDir));
    } else if (entry.isFile() && entry.name.endsWith('.astro')) {
      // Skip dynamic routes (e.g., [...slug].astro)
      if (entry.name.includes('[')) continue;

      // Convert file path to route
      const relativePath = relative(baseDir, fullPath);
      let route = '/' + relativePath
        .replace(/\.astro$/, '')
        .replace(/\/index$/, '')
        .replace(/index$/, '');

      // Ensure trailing slash
      if (route !== '/' && !route.endsWith('/')) {
        route += '/';
      }

      routes.push(route);
    }
  }

  return routes.sort();
}

// Dynamically discover all static routes from the pages directory
const pagesDir = join(process.cwd(), 'src', 'pages');
const routes = discoverRoutes(pagesDir, pagesDir);

const locales = ['en'];

// Helper to collect errors during page load
interface PageErrors {
  pageErrors: Error[];
  consoleErrors: string[];
}

async function collectPageErrors(page: Page): Promise<PageErrors> {
  const errors: PageErrors = {
    pageErrors: [],
    consoleErrors: [],
  };

  page.on('pageerror', (error: Error) => {
    errors.pageErrors.push(error);
  });

  page.on('console', (msg: ConsoleMessage) => {
    if (msg.type() === 'error') {
      const text = msg.text();
      // Ignore resource loading errors (404s, network errors) as they're not crash signals
      if (!text.includes('Failed to load resource') && !text.includes('ERR_NAME_NOT_RESOLVED')) {
        errors.consoleErrors.push(text);
      }
    }
  });

  return errors;
}

// Test each route in each locale
for (const locale of locales) {
  test.describe(`Smoke tests - ${locale.toUpperCase()} locale`, () => {
    for (const route of routes) {
      test(`${route} loads without crashes`, async ({ page }) => {
        // Set up error collection BEFORE navigating
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
        expect(errors.pageErrors, `${url} should have no uncaught page errors`).toHaveLength(0);

        // Verify no console.error messages
        expect(errors.consoleErrors, `${url} should have no console.error messages`).toHaveLength(
          0
        );
      });
    }
  });
}
