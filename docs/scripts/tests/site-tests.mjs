#!/usr/bin/env node

/* global process */

/**
 * Site Testing Suite
 *
 * Runs comprehensive site validation including:
 * - Broken link checking (via astro-broken-links-checker)
 * - Localized link validation (internal links must match page locale)
 * - Localized content marker validation (locale markers present on key pages)
 */

import { readdir, readFile } from 'fs/promises';
import { join, resolve, dirname } from 'path';
import { fileURLToPath } from 'url';
import { JSDOM } from 'jsdom';

const __filename = fileURLToPath(import.meta.url);
const __dirname = dirname(__filename);
const DIST_DIR = resolve(__dirname, '../../dist');

// ANSI color codes for output
const colors = {
  reset: '\x1b[0m',
  red: '\x1b[31m',
  green: '\x1b[32m',
  yellow: '\x1b[33m',
  blue: '\x1b[34m',
  cyan: '\x1b[36m',
};

class TestResults {
  constructor() {
    this.errors = [];
    this.warnings = [];
    this.passed = 0;
  }

  addError(test, message, details = null) {
    this.errors.push({ test, message, details });
  }

  addWarning(test, message, details = null) {
    this.warnings.push({ test, message, details });
  }

  pass() {
    this.passed++;
  }

  hasErrors() {
    return this.errors.length > 0;
  }

  report() {
    console.log('\n' + '='.repeat(80));
    console.log(`${colors.cyan}Site Test Results${colors.reset}`);
    console.log('='.repeat(80));

    if (this.passed > 0) {
      console.log(`${colors.green}✓ ${this.passed} test(s) passed${colors.reset}`);
    }

    if (this.warnings.length > 0) {
      console.log(`${colors.yellow}⚠ ${this.warnings.length} warning(s)${colors.reset}`);
      this.warnings.forEach(({ test, message, details }) => {
        console.log(`  ${test}: ${message}`);
        if (details) {
          console.log(`    ${JSON.stringify(details, null, 2)}`);
        }
      });
    }

    if (this.errors.length > 0) {
      console.log(`${colors.red}✗ ${this.errors.length} error(s)${colors.reset}`);
      this.errors.forEach(({ test, message, details }) => {
        console.log(`  ${test}: ${message}`);
        if (details) {
          if (Array.isArray(details)) {
            details.forEach(detail => console.log(`    - ${detail}`));
          } else {
            console.log(`    ${JSON.stringify(details, null, 2)}`);
          }
        }
      });
    }

    console.log('='.repeat(80) + '\n');

    return !this.hasErrors();
  }
}

/**
 * Find all HTML files in the dist directory
 */
async function findHtmlFiles(dir, files = []) {
  const entries = await readdir(dir, { withFileTypes: true });

  for (const entry of entries) {
    const fullPath = join(dir, entry.name);

    if (entry.isDirectory()) {
      await findHtmlFiles(fullPath, files);
    } else if (entry.isFile() && entry.name.endsWith('.html')) {
      files.push(fullPath);
    }
  }

  return files;
}

/**
 * Extract locale from a path like /de/... or /en/...
 * Note: Currently supports 2-letter locale codes only (en, de).
 * For multi-part locales (en-US, zh-CN), update the regex pattern below.
 */
function getLocaleFromPath(pathname) {
  // Match paths like /de/, /en/, /de/products, etc.
  // Pattern: /^\/([a-z]{2})(\/|$)/
  // For multi-part locales, use: /^\/([a-z]{2}(?:-[A-Z]{2})?)(\/|$)/i
  const match = pathname.match(/^\/([a-z]{2})(\/|$)/);
  return match ? match[1] : null;
}

/**
 * Resolve a relative URL against a base path
 */
function resolveUrl(href, basePath) {
  try {
    // Handle absolute URLs (http://, https://, mailto:, tel:, etc.)
    if (/^[a-z][a-z0-9+.-]*:/i.test(href)) {
      return { isExternal: true, resolved: href };
    }

    // Handle fragment-only links
    if (href.startsWith('#')) {
      return { isExternal: true, resolved: href };
    }

    // Resolve relative paths
    const base = basePath.endsWith('/') ? basePath : basePath + '/';
    const url = new URL(href, `https://example.com${base}`);
    return { isExternal: false, resolved: url.pathname };
  } catch (e) {
    return { isExternal: true, resolved: href, error: e.message };
  }
}

/**
 * Check localized links rule:
 * Pages under /<locale>/ should only link to internal URLs with the same locale prefix
 */
async function checkLocalizedLinks(results) {
  console.log(`${colors.blue}Checking localized link rules...${colors.reset}`);

  const htmlFiles = await findHtmlFiles(DIST_DIR);
  const violations = [];
  let checkedPages = 0;
  let checkedLinks = 0;

  for (const filePath of htmlFiles) {
    // Convert file path to URL path
    const relativePath = filePath.substring(DIST_DIR.length);
    const urlPath = relativePath.replace(/index\.html$/, '').replace(/\.html$/, '/');

    const pageLocale = getLocaleFromPath(urlPath);

    // Only check pages that are under a locale path
    if (!pageLocale) {
      continue;
    }

    checkedPages++;
    const content = await readFile(filePath, 'utf-8');
    const dom = new JSDOM(content);
    const links = dom.window.document.querySelectorAll('a[href]');

    for (const link of links) {
      const href = link.getAttribute('href');
      const { isExternal, resolved } = resolveUrl(href, urlPath);

      // Skip external links
      if (isExternal) {
        continue;
      }

      checkedLinks++;
      const linkLocale = getLocaleFromPath(resolved);

      // Internal link from localized page should point to same locale or no locale
      // (some shared resources might not be localized)
      if (linkLocale && linkLocale !== pageLocale) {
        violations.push({
          page: urlPath,
          href,
          resolved,
          pageLocale,
          linkLocale,
        });
      }
    }
  }

  if (violations.length > 0) {
    results.addError(
      'Localized Links',
      `Found ${violations.length} link(s) pointing to wrong locale`,
      violations.map(
        v => `${v.page} (${v.pageLocale}) → ${v.href} → ${v.resolved} (${v.linkLocale})`
      )
    );
  } else if (checkedPages > 0) {
    results.pass();
    console.log(`  ✓ Checked ${checkedLinks} links in ${checkedPages} localized pages`);
  } else {
    results.addWarning(
      'Localized Links',
      'No localized pages found (no pages under /<locale>/ paths)',
      { hint: 'This check is skipped if locale routing is not enabled' }
    );
  }
}

/**
 * Check localized content marker rule:
 * Key localized pages should have a data-locale marker matching their locale
 */
async function checkLocalizedMarkers(results) {
  console.log(`${colors.blue}Checking localized content markers...${colors.reset}`);

  const htmlFiles = await findHtmlFiles(DIST_DIR);
  const violations = [];
  const validMarkers = [];

  // Check key pages (index and main section pages per locale)
  // Note: Update this list when adding new main sections to the site
  const keyPagePatterns = [
    /^\/[a-z]{2}\/(index\.html)?$/, // /de/, /en/
    /^\/[a-z]{2}\/products\/(index\.html)?$/,
    /^\/[a-z]{2}\/services\/(index\.html)?$/,
    /^\/[a-z]{2}\/pricing\/(index\.html)?$/,
  ];

  for (const filePath of htmlFiles) {
    const relativePath = filePath.substring(DIST_DIR.length);
    const urlPath = relativePath.replace(/index\.html$/, '').replace(/\.html$/, '/');

    // Check if this is a key page
    const isKeyPage = keyPagePatterns.some(pattern => pattern.test(urlPath));
    if (!isKeyPage) {
      continue;
    }

    const pageLocale = getLocaleFromPath(urlPath);
    if (!pageLocale) {
      continue;
    }

    const content = await readFile(filePath, 'utf-8');
    const dom = new JSDOM(content);

    // Look for data-locale marker (could be on html, body, or a wrapper element)
    const markerElements = dom.window.document.querySelectorAll('[data-locale]');

    if (markerElements.length === 0) {
      violations.push({
        page: urlPath,
        expected: pageLocale,
        found: null,
      });
    } else {
      const marker = markerElements[0].getAttribute('data-locale');
      if (marker !== pageLocale) {
        violations.push({
          page: urlPath,
          expected: pageLocale,
          found: marker,
        });
      } else {
        validMarkers.push(urlPath);
      }
    }
  }

  if (violations.length > 0) {
    results.addError(
      'Locale Markers',
      `Found ${violations.length} page(s) with missing or incorrect locale markers`,
      violations.map(v =>
        v.found === null
          ? `${v.page}: missing data-locale (expected: ${v.expected})`
          : `${v.page}: data-locale="${v.found}" (expected: ${v.expected})`
      )
    );
  } else if (validMarkers.length > 0) {
    results.pass();
    console.log(`  ✓ Verified ${validMarkers.length} key pages have correct locale markers`);
  } else {
    results.addWarning('Locale Markers', 'No key localized pages found to check markers', {
      hint: 'This check is skipped if locale routing is not enabled',
    });
  }
}

/**
 * Check broken links (via log file from astro-broken-links-checker)
 */
async function checkBrokenLinks(results) {
  console.log(`${colors.blue}Checking for broken links...${colors.reset}`);

  const logPath = resolve(__dirname, '../../broken-links.log');

  try {
    const content = await readFile(logPath, 'utf-8');

    // Parse the log file from astro-broken-links-checker
    // The checker outputs broken links grouped by URL with source pages listed below
    // Format: Broken URL on its own line, followed by source pages indented
    const lines = content.trim().split('\n');

    if (lines.length === 0 || (lines.length === 1 && lines[0] === '')) {
      results.pass();
      console.log(`  ✓ No broken links found`);
      return;
    }

    // Count unique broken URLs (non-indented lines that aren't empty or separators)
    const brokenUrls = lines.filter(line => {
      const trimmed = line.trim();
      return (
        trimmed.length > 0 &&
        !line.startsWith(' ') &&
        !line.startsWith('\t') &&
        !trimmed.match(/^[-=]+$/)
      );
    });

    if (brokenUrls.length === 0) {
      results.pass();
      console.log(`  ✓ No broken links found`);
      return;
    }

    results.addError(
      'Broken Links',
      `Found ${brokenUrls.length} broken link(s) - see broken-links.log for details`,
      { logPath, preview: brokenUrls.slice(0, 5) }
    );
  } catch (err) {
    if (err.code === 'ENOENT') {
      results.addWarning(
        'Broken Links',
        'broken-links.log not found - link checking may not have run',
        { hint: 'The astro-broken-links-checker should create this during build' }
      );
    } else {
      results.addError('Broken Links', `Failed to read broken-links.log: ${err.message}`);
    }
  }
}

/**
 * Main test runner
 */
async function runTests() {
  console.log(`${colors.cyan}Starting site tests...${colors.reset}\n`);

  const results = new TestResults();

  try {
    // Run all checks
    await checkBrokenLinks(results);
    await checkLocalizedLinks(results);
    await checkLocalizedMarkers(results);

    // Report results
    const success = results.report();
    process.exit(success ? 0 : 1);
  } catch (err) {
    console.error(`${colors.red}Test runner failed:${colors.reset}`, err);
    process.exit(1);
  }
}

// Run tests
runTests();
