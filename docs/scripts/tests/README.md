# Site Test Suite

This directory contains automated tests for the Astro website build.

## Running Tests

```bash
npm run test:site
```

This command:
1. Builds the site (`npm run docs:build`)
2. Runs the site validation tests

## What Gets Tested

### 1. Broken Links
- Validates all internal links using `astro-broken-links-checker`
- Results written to `broken-links.log` during build
- Test reads and reports any broken links found

### 2. Localized Links
- For pages under `/<locale>/` paths (e.g., `/de/`, `/en/`)
- Ensures internal links point to URLs with the same locale prefix
- Example violation: `/de/products/` linking to `/en/services/`
- Skipped if no locale-based routes exist

### 3. Locale Content Markers
- Validates key pages have correct `data-locale` attributes
- Checks root pages and main sections per locale
- Example: `/de/` should have `data-locale="de"`
- Skipped if no locale-based routes exist

## Test Output

Tests produce colored, actionable output:
- ✓ Green: Passed tests
- ⚠ Yellow: Warnings (non-blocking issues)
- ✗ Red: Errors (test failures)

Exit code:
- `0`: All tests passed (warnings allowed)
- `1`: One or more tests failed

## Implementation

- **Language**: Node.js ESM
- **HTML Parsing**: jsdom (library-first approach)
- **URL Resolution**: Native URL API
- **Design**: Deterministic, CI-friendly, no snapshots or CSS selectors
