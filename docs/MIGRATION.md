# Documentation Migration: VitePress to Astro

This document describes the migration of the Open Ticket AI documentation from VitePress to Astro with Starlight theme.

## Migration Summary

- **From**: VitePress 1.6.3
- **To**: Astro 5.16.7 with Starlight 0.37.2
- **Date**: January 2026
- **Status**: ✅ Complete

## What Changed

### Build System
- Replaced VitePress with Astro + Starlight
- Build command remains the same: `npm run docs:build`
- Dev command remains the same: `npm run docs:dev`
- Output directory changed from `.vitepress/dist` to `dist`

### Content Structure
- Content moved from `docs_src/en/` to `src/content/docs/`
- All markdown files now require a `title` field in frontmatter (Starlight requirement)
- VitePress-specific frontmatter fields removed:
  - `layout: "page"` → removed (not supported in Astro 5)
  - `aside: false` → removed
  - `pageClass: "full-page"` → removed

### Markdown Features

#### ✅ Supported
- **Mermaid diagrams**: Using rehype-mermaid plugin
- **Code blocks**: Using Expressive Code (enhanced syntax highlighting)
- **Frontmatter**: title, description
- **Tables**: Native markdown tables
- **Images**: Markdown images and HTML img tags

#### 🔄 Adapted
- **VitePress containers**: `:::tip`, `:::warning`, `:::note`, etc.
  - Converted via custom remark plugin to Starlight's `<Aside>` component
  - Mapping:
    - `:::tip` → `<Aside type="tip">`
    - `:::warning` → `<Aside type="caution">`
    - `:::danger` → `<Aside type="danger">`
    - `:::note`, `:::info`, `:::details` → `<Aside type="note">`

#### ❌ Not Yet Supported
- **Vue Components**: VitePress custom Vue components not migrated
  - `<LatestNews />`, `<YoutubeVideo />`, `<OTAIPredictionDemo />`, etc.
  - These components are present in the markdown but won't render
  - Future work: Convert to Astro components or use MDX

- **Code Groups**: VitePress `::: code-group` syntax
  - Need to convert to Starlight's native code group syntax

### Search
- Replaced VitePress built-in search with Pagefind
- Static site search, no JavaScript required for indexing
- Search runs after build: `astro build && npx pagefind --site dist`
- Indexes all built pages automatically

### Styling
- Dark theme enforced (matching VitePress configuration)
- Custom CSS in `src/styles/custom.css`
- Purple accent color (#7c4dff) matching brand

### Navigation & Sidebar
- Auto-generated from folder structure
- Sections:
  - Products
  - Guides
  - Users
  - Developers
  - Details
  - Blog

### URLs & Routing
- **Breaking Change**: URLs no longer include `/en/` prefix
- **Old**: `https://open-ticket-ai.com/en/guides/quick_start`
- **New**: `https://open-ticket-ai.com/guides/quick_start/`
- All pages get trailing slashes (Astro default)

### Analytics
- Google Analytics maintained (AW-474755810 and G-FBWC3JDZJ4)
- Lazy-loaded via custom Head component

## How to Run Docs Locally

### Development Server
```bash
cd docs
npm install
npx playwright install --with-deps chromium  # Required for Mermaid diagram rendering
npm run docs:dev
```
Visit http://localhost:4321/ (or 4322 if 4321 is in use)

### Build for Production
```bash
cd docs
npm install
npx playwright install --with-deps chromium  # Required for Mermaid diagram rendering
npm run docs:build
```
Output: `docs/dist/`

### Preview Production Build
```bash
cd docs
npm run docs:preview
```

## Dependencies

### Added
- `astro` (^5.16.7)
- `@astrojs/starlight` (^0.37.2)
- `@astrojs/mdx` (^4.3.13)
- `sharp` (^0.34.5) - Image optimization
- `pagefind` (^1.4.0) - Search
- `rehype-mermaid` (^3.0.0) - Mermaid diagram support (requires Playwright)
- `playwright` (^1.53.2) - Browser automation for Mermaid rendering
- `remark-directive` (^4.0.0) - Custom directive support
- `unist-util-visit` (^5.0.0) - AST traversal for plugins

### Build Requirements
- **Playwright Browsers**: Required for Mermaid diagram rendering
  - Install with: `npx playwright install --with-deps chromium`
  - rehype-mermaid uses Playwright to render Mermaid diagrams as SVG at build time
  - Without this, builds will fail with "Executable doesn't exist" errors

### Kept (for Storybook)
- VitePress and Vue dependencies remain for Storybook components
- These don't interfere with Astro build

## Known Issues & Limitations

### 1. Vue Components Not Rendered
Custom Vue components from VitePress are referenced in markdown but don't render:
- `<ExamplesGallery>` in users/config_examples.md
- `<PluginsMarketplace>` in users/plugin-marketplace.md
- `<MultiTagPredictionDemo>` in multiTagDemo/demo.md
- Homepage components (LatestNews, YoutubeVideo, etc.)

**Solution**: Convert to Astro components or create MDX versions

### 2. URL Changes
URLs no longer include the `/en/` language prefix. This is a breaking change for external links.

**Mitigation**: Netlify redirects can be added to netlify.toml to redirect old URLs

### 3. Duplicate ID Warnings
Build shows warnings about duplicate IDs for some files. This is harmless (files exist in both docs_src and src/content/docs during transition).

**Solution**: Remove docs_src/en/ content after migration is complete

### 4. Code Group Syntax
VitePress code groups (`::: code-group`) need manual conversion to Starlight syntax

### 5. Files Starting with Underscore
Files like `_config_rendering.md` are included but Starlight convention uses underscore for draft/unlisted pages.

**Recommendation**: Rename or decide if these should be hidden

## Files Created

- `/docs/astro.config.mjs` - Astro configuration
- `/docs/tsconfig.json` - TypeScript configuration
- `/docs/src/content/config.ts` - Content collections config
- `/docs/src/components/Head.astro` - Custom head component for analytics
- `/docs/src/styles/custom.css` - Custom styles
- `/docs/remark-vitepress-containers.mjs` - Plugin to convert VitePress containers

## Files Modified

- `/docs/package.json` - Updated scripts
- `/netlify.toml` - Changed publish directory from `.vitepress/dist` to `dist`
- `/.gitignore` - Added Astro build artifacts

## Migration Checklist

- [x] Set up Astro with Starlight
- [x] Copy markdown content
- [x] Add titles to all markdown files
- [x] Fix YAML frontmatter syntax
- [x] Configure sidebar navigation
- [x] Add Mermaid support
- [x] Add VitePress container conversion
- [x] Integrate Pagefind search
- [x] Update netlify.toml
- [x] Add .gitignore entries
- [ ] Convert Vue components to Astro (future work)
- [ ] Add URL redirects for /en/ prefix
- [ ] Test all internal links
- [ ] Remove docs_src/en/ after verifying migration

## Rollback Plan

If needed, rollback involves:
1. Revert changes to package.json, netlify.toml
2. Delete src/ directory
3. VitePress files remain intact in docs_src/

## Resources

- [Astro Documentation](https://docs.astro.build/)
- [Starlight Documentation](https://starlight.astro.build/)
- [Pagefind Documentation](https://pagefind.app/)
- [Migration Guide](https://docs.astro.build/en/guides/migrate-to-astro/)
