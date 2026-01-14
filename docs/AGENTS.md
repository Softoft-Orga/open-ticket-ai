# Agent Notes: Docs Frontend

## Stack at a glance

- Docs site: Astro + Vite, Vue 3 components, Tailwind, HeadlessUI, Storybook (`docs/.storybook`) for
  UI review.
- Styling: Tailwind (see `docs/tailwind.config.cjs`)
- Global UI: `docs/src/styles/global.css`
- **Formatting**: Prettier with plugins for Astro and Tailwind CSS. Run `npm run format` to format
  all files. Use `npm run format:check` to verify formatting.
- **Linting**: ESLint with Flat Config (eslint.config.mjs). Run `npm run lint` before committing.
  Use `npm run lint:fix` to auto-fix issues.
- **Link checking**: Broken link checker via `astro-broken-links-checker` integration. Runs during
  build to validate internal links. Configure in `astro.config.mjs`.

## Link checking

The site uses `astro-broken-links-checker` to validate internal links during the build process.

**Configuration** (in `astro.config.mjs`):

- `logFilePath`: Path to the log file (default: `broken-links.log`)
- `checkExternalLinks`: Whether to check external links (default: `false` for performance)
- `throwError`: Whether to fail the build on broken links (default: `false`)

**Usage**:

- Run `npm run lint:links` to build the site and check for broken links
- Check the console output for immediate feedback
- Review `broken-links.log` for detailed results grouped by broken URL
- The checker caches results and checks links in parallel for better performance

## Image handling

- **Image storage locations**:
  - **Local assets**: Store in `docs/src/assets/` for imported images that need optimization
  - **Public images**: Store in `docs/public/assets/` or `docs/public/images/` for static images
    served as-is
  - **Subdirectories**: Organize by category (e.g., `public/assets/`, `public/images/`,
    `public/icons/`)
- **Image optimization**: Configured in `docs/astro.config.mjs` using Sharp service
  - Automatically optimizes images from `src/` directory
  - Authorized domains: `astro.build`, `doc.otobo.org`, `softoft.sirv.com`
  - Remote patterns allowed: `**.githubusercontent.com`, `**.sirv.com`
- **Using images in Astro components/pages**:
  - **For local images in `src/assets/`**: Import and use with `<Image>` component

    ```astro
    ---
    import { Image } from 'astro:assets';
    import myImage from '../assets/my-image.png';
    ---

    <Image src={myImage} alt="Description" />
    ```

  - **For public folder images**: Use path string with required width/height

    ```astro
    ---
    import { Image } from 'astro:assets';
    ---

    <Image src="/assets/my-image.png" alt="Description" width="800" height="600" />
    ```

  - **For remote images**: Use full URL with required width/height

    ```astro
    ---
    import { Image } from 'astro:assets';
    ---

    <Image src="https://example.com/image.jpg" alt="Description" width="800" height="600" />
    ```

  - **Always** include `alt` attribute for accessibility
  - Local imported images auto-generate width/height; public/remote images require explicit
    dimensions
  - The `<Image>` component automatically optimizes formats (WebP, AVIF) and sizes

- **In Markdown/MDX content**: Use standard markdown syntax `![alt text](/images/file.png)` - Astro
  will optimize these automatically

## Design alignment

- Use Tailwind utility classes to implement designs; avoid custom CSS unless necessary. Use our
  Tailwind config tokens docs/tailwind.config.cjs
- Use our Vue core components, see COMPONENTS.md

## Vue Components

We have Core Components and Domain Components. Core Components are used very often and are basic
Components like Badge, Alert
Button and similar.
Domain Components are specific components like a BeyondSavingCard that is shown on ROI Page. We use
them for reactivity that can not be achieved with Astro but these are not reused.

## Quick references

- Core **Components**: Live under `docs/src/components/vue/core/**` and are showcased via Storybook
  stories in
  `docs/stories/**`.
  - Inventory: See `COMPONENTS.md` for a complete list with brief descriptions
  - Detailed docs: Check Storybook stories (`.stories.ts` files) for usage examples and props

## Testing

The site includes automated testing via `npm run test:site`:

- **Broken links**: Validates all internal links using `astro-broken-links-checker` (runs during
  build)
- **Localized links**: Ensures pages under `/<locale>/` paths only link to URLs with the same locale
  prefix
- **Locale markers**: Verifies key localized pages have correct `data-locale` attributes matching
  their locale

Results are deterministic and CI-friendly. See `scripts/tests/site-tests.mjs` for implementation.

## Workflow expectations

- **Always format code after each task**: Run `npm run format` to format all files with Prettier
  after completing any task or making changes. This ensures consistent code style across the
  project.
- **Always lint before committing**: Run `npm run lint` to check for issues. Run `npm run lint:fix`
  to auto-fix.
- **Check for broken links**: Run `npm run lint:links` to build the site and check for broken
  internal links. Results are logged to the console and written to `broken-links.log`.
- Use Playwright MCP to visually check UI changes (Astro on :4321, Storybook on :6006) when tweaking
  design-sensitive components.
- Prefer MCP-driven Storybook checks/screenshots over manual eyeballing when validating regressions.
- Use Context7 for getting the newest Documentation for our packages: like astro, vue and other
  libaries/frameworks
- Whenever core components or story configs change, update the corresponding Storybook stories in
  `docs/stories/**` to reflect new props, variants, and states.

## Testing

- **Crash-smoke tests**: Run `npm run test:playwright` to verify pages load without errors
  - Checks: no console.error, no pageerror events, response status OK
  - Tests all key routes (/, /products/, /pricing/, /roi-calculator/, /blog/, /docs/)
  - Auto-starts Astro dev server via Playwright's `webServer` config
  - Stable, fast tests with no UI/snapshot dependencies
  - Resource loading errors (404s for images/fonts) are filtered out

## Documentation update rules

### When changing Vue components

**ALWAYS** update when you add/remove/rename/move Vue core components under
`docs/src/components/vue/core`:

- [ ] Update `COMPONENTS.md` with the new component entry (name, description, props, slots)
- [ ] Create or update corresponding Storybook story in `docs/stories/**/*.stories.ts`
- [ ] Follow story naming convention: `{ComponentName}.stories.ts`
- [ ] Ensure component appears in Storybook and renders correctly

### When changing content collections

**ALWAYS** update when you modify `src/content/**` or `src/content/config.ts`:

- [ ] Update `CONTENT_COLLECTIONS.md` if schemas, fields, or conventions change
- [ ] Verify all required frontmatter fields are documented
- [ ] Test that pages using content collections still work
- [ ] Run `npm run docs:build` to verify no errors

### Using localized content collections

**ALWAYS** filter content by the current locale when querying collections:

**Important:** `Astro.currentLocale` is always defined (never null or undefined) due to the i18n configuration in `astro.config.mjs`. All content collection IDs start with the locale prefix followed by a slash (e.g., `en/`, `de/`).

```astro
---
import { getCollection } from 'astro:content';

// Get current locale (always defined, no fallback needed)
const currentLocale = Astro.currentLocale.toLowerCase();

// For data collections (YAML) - filter by ID prefix with slash
const allServices = await getCollection('services');
const localizedServices = allServices.filter(entry =>
  entry.id.toLowerCase().startsWith(`${currentLocale}/`)
);

// For content collections (MD/MDX) - filter by locale prefix with slash
const allDocs = await getCollection('docs');
const localizedDocs = allDocs.filter(entry =>
  entry.id.toLowerCase().startsWith(`${currentLocale}/`)
);

// For singleton data collections - find the first matching entry
const allSiteConfigs = await getCollection('site');
const siteConfig = allSiteConfigs.find(entry =>
  entry.id.toLowerCase().startsWith(`${currentLocale}/`)
);
---
```

This ensures content is automatically filtered by locale.

### Quick checklist

Before finalizing component or content changes:

- Formatting: Run `npm run format` to format all files with Prettier
- Core Components: `COMPONENTS.md` updated + Storybook story exists + story renders, when a core
  component was changed not if a Domain Component changes!
- Content: `CONTENT_COLLECTIONS.md` accurate + schema valid + pages render
- Build passes: `npm run docs:build` succeeds
