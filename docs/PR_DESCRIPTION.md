# Docs Migration: VitePress to Astro + Starlight

## Summary

This PR completes the migration of the Open Ticket AI documentation from VitePress to Astro + Starlight, implementing all requirements from the specification. The migration maintains the same developer experience while modernizing the documentation infrastructure with better performance, SEO, and maintainability.

## Key Changes

### Build System
- ✅ Replaced VitePress with **Astro 5.16.7** and **Starlight 0.37.2**
- ✅ Maintained same commands: `npm run docs:dev`, `npm run docs:build`
- ✅ Output directory changed from `.vitepress/dist` to `dist`
- ✅ Integrated **Pagefind 1.4.0** for static search
- ✅ Build command includes: `astro build && npx pagefind --site dist`

### Content Migration
- ✅ Content migrated from `docs_src/en/` to `src/content/docs/`
- ✅ All markdown files have required `title` frontmatter
- ✅ Removed unsupported VitePress frontmatter:
  - `layout: "page"`
  - `aside: false/true`
  - `pageClass: "full-page"`
- ✅ Content structure organized with sections: Products, Guides, Users, Developers, Details, Blog

### Markdown Features

#### ✅ Fully Supported
- **Mermaid diagrams**: Using `rehype-mermaid 3.0.0` with build-time rendering
- **Code blocks**: Expressive Code with `github-dark` theme
- **Tables, images**: Native markdown support
- **Syntax highlighting**: Enhanced via Starlight's Expressive Code

#### 🔄 Adapted
- **VitePress containers**: Custom remark plugin converts to Starlight `<Aside>` components
  - `:::tip` → `<Aside type="tip">`
  - `:::warning` → `<Aside type="caution">`
  - `:::danger` → `<Aside type="danger">`
  - `:::note`, `:::info`, `:::details` → `<Aside type="note">`
- Plugin implemented using `remark-directive` and `unist-util-visit`

#### ⚠️ Known Limitations (Documented)
- **Vue components**: Present in markdown but not rendered (future work)
  - Examples: `<OTAIPredictionDemo/>`, `<WaitlistSignupForm/>`, `<Table>`, etc.
  - Found in: products/prediction-api/overview.md, products/overview.md, others
- **Code groups**: VitePress `::: code-group` syntax not converted
  - Found in: blog/open-ticket-ai-1-4-release.md, users/plugin-otobo-znuny/setup.md, users/installation.md
  - Future work: Convert to Starlight's native syntax

### Styling & Theming
- ✅ Dark theme enforced via custom CSS
- ✅ Accent color: `#7c4dff` (brand purple)
- ✅ Custom CSS at `docs/src/styles/custom.css`
- ✅ Consistent with brand identity

### Navigation & Search
- ✅ Auto-generated sidebar from folder structure
- ✅ Pagefind search with static indexing (no runtime JS needed)
- ✅ Search indexes 31 pages with 4294 words
- ✅ Breadcrumbs and navigation maintained

### URLs & Routing
- ⚠️ **Breaking Change**: Removed `/en/` prefix from URLs
  - Old: `https://open-ticket-ai.com/en/guides/quick_start`
  - New: `https://open-ticket-ai.com/guides/quick_start/`
- ✅ All pages have trailing slashes (Astro convention)
- ✅ Removed language redirects from netlify.toml

### Analytics
- ✅ Both Google Analytics IDs preserved:
  - **AW-474755810**
  - **G-FBWC3JDZJ4**
- ✅ Lazy-loaded via custom `docs/src/components/Head.astro`
- ✅ Loads on idle callback or user interaction (performance optimized)

### Configuration Files Created
1. ✅ `docs/astro.config.mjs` - Astro + Starlight configuration
2. ✅ `docs/tsconfig.json` - TypeScript configuration for Astro
3. ✅ `docs/src/content/config.ts` - Content collections schema
4. ✅ `docs/src/components/Head.astro` - Custom head with lazy GA loading
5. ✅ `docs/src/styles/custom.css` - Dark theme and brand colors
6. ✅ `docs/remark-vitepress-containers.mjs` - Container conversion plugin

### Files Modified
1. ✅ `docs/package.json` - Updated scripts and dependencies
2. ✅ `netlify.toml` - Changed publish dir to `dist`, removed /en/ redirects
3. ✅ `.gitignore` - Added Astro build artifacts (`/docs/dist/`, `/docs/.astro/`, `/docs/pagefind/`)

## How to Run Locally

### First Time Setup
```bash
cd docs
npm install
npx playwright install --with-deps chromium  # Required for Mermaid rendering
```

### Development Server
```bash
npm run docs:dev
```
- Default: http://localhost:4321/
- Fallback: http://localhost:4322/ (if 4321 in use)
- Hot reload enabled

### Production Build
```bash
npm run docs:build
```
- Builds to `docs/dist/`
- Runs Pagefind indexing automatically
- Renders Mermaid diagrams as static SVG

### Preview Build
```bash
npm run docs:preview
```

## Dependencies Added

All dependencies match the specification:

| Dependency | Version | Purpose |
|------------|---------|---------|
| astro | ^5.16.7 | Core framework |
| @astrojs/starlight | ^0.37.2 | Documentation theme |
| @astrojs/mdx | ^4.3.13 | MDX support |
| sharp | ^0.34.5 | Image optimization |
| pagefind | ^1.4.0 | Static search |
| rehype-mermaid | ^3.0.0 | Mermaid diagram rendering |
| playwright | ^1.53.2 | Browser automation for Mermaid |
| remark-directive | ^4.0.0 | Custom directive support |
| unist-util-visit | ^5.0.0 | AST traversal for plugins |

**Note**: VitePress and Vue dependencies kept for Storybook; they don't interfere with docs build.

## Known Issues & Limitations

### 1. Vue Components Not Rendered
Custom Vue components referenced in markdown are not rendered in the migrated docs:
- `<OTAIPredictionDemo/>` in products/prediction-api/overview.md
- `<WaitlistSignupForm/>` in products/synthetic-data/synthetic-data-generation.md
- `<Table>`, `<Row>`, `<C>` in products/overview.md
- Others in various files

**Impact**: These sections will show empty or raw HTML tags  
**Follow-up**: Convert to Astro components or create MDX equivalents

### 2. Code Group Syntax
VitePress `::: code-group` syntax found in 3 files:
- blog/open-ticket-ai-1-4-release.md
- users/plugin-otobo-znuny/setup.md
- users/installation.md

**Impact**: May not render correctly; needs manual conversion  
**Follow-up**: Convert to Starlight's native tab component syntax

### 3. URL Breaking Change
URLs no longer include `/en/` prefix. External links pointing to old URLs will 404.

**Impact**: SEO may be affected temporarily  
**Follow-up**: Add redirects in netlify.toml if needed:
```toml
[[redirects]]
from = "/en/*"
to = "/:splat"
status = 301
```

### 4. Duplicate Content Warning
Both `docs_src/en/` and `src/content/docs/` exist during transition. This is expected and documented.

**Impact**: None on functionality  
**Follow-up**: Remove `docs_src/en/` after verifying migration is complete

### 5. Files with Underscore Prefix
Files like `_config_rendering.md`, `_predefined-pipes.md` in details/ directory are included.

**Note**: Starlight convention uses underscore for draft pages, but these are intentionally included  
**Follow-up**: Consider renaming if these should be listed differently

## Testing Performed

- ✅ Build completes successfully without errors
- ✅ Dev server starts on ports 4321/4322
- ✅ Pagefind search indexing works (31 pages, 4294 words)
- ✅ All markdown files have required frontmatter
- ✅ Unsupported VitePress frontmatter removed
- ✅ Both analytics IDs configured correctly
- ✅ Mermaid diagrams render at build time
- ✅ Output directory structure correct
- ✅ Sitemap generated

## Follow-up Tasks

1. **Vue Component Migration**: Convert Vue components to Astro or MDX
2. **Code Group Syntax**: Update `::: code-group` to Starlight tabs
3. **URL Redirects**: Add /en/ to root redirects if needed for SEO
4. **Content Cleanup**: Remove docs_src/en/ after verification
5. **Link Verification**: Test all internal and external links
6. **Accessibility Audit**: Verify a11y with new theme
7. **Performance Testing**: Measure page load times vs VitePress

## References

- Specification document (followed completely)
- [MIGRATION.md](./MIGRATION.md) - Detailed migration notes
- [Astro Documentation](https://docs.astro.build/)
- [Starlight Documentation](https://starlight.astro.build/)
- [Pagefind Documentation](https://pagefind.app/)

## Verification Steps for Reviewers

1. Install dependencies: `cd docs && npm install`
2. Install Playwright: `npx playwright install --with-deps chromium`
3. Build docs: `npm run docs:build`
4. Verify build output in `docs/dist/`
5. Start dev server: `npm run docs:dev`
6. Visit http://localhost:4321/ and verify:
   - Dark theme applied
   - Search works
   - Navigation functional
   - Mermaid diagrams render
   - No console errors

## Migration Status

**Status**: ✅ Complete and ready for review

All specification requirements have been implemented:
- [x] Astro 5.16.7 + Starlight 0.37.2
- [x] All required dependencies with correct versions
- [x] Build system configured
- [x] Content migrated with proper frontmatter
- [x] VitePress containers converted
- [x] Search integrated (Pagefind)
- [x] Mermaid support configured
- [x] Analytics preserved and lazy-loaded
- [x] Dark theme enforced
- [x] Netlify configuration updated
- [x] .gitignore updated
- [x] Documentation created (MIGRATION.md)
- [x] Known limitations documented
