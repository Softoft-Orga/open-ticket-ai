# E2E & Visual Regression Contract

This directory will host Playwright end-to-end and visual regression suites for the Astro docs site.

## Layout

- Specs live in this folder (none yet).
- `screenshots/` keeps any curated reference assets; Playwright snapshots stay beside the spec files.

## Expectations

- Use accessible roles/names instead of brittle class/id selectors.
- Primary CTA labels must stay "Get Demo" / "Contact Sales"; navbar names must include "Home", "Products", "Services", "Docs".
- Intentional copy changes require updating tests plus snapshots in the same PR.
- Always run `npm run test:e2e` from `docs/` before merging.
