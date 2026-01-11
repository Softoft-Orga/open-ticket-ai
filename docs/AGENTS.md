# Agent Notes: Docs Frontend

## Stack at a glance
- Docs site: Astro + Vite, Vue 3 components, HeadlessUI Storybook (`docs/.storybook`) for UI review.
- Styling: Tailwind (see `docs/tailwind.config.cjs`) with the mandated palette (`primary`, `primary-dark`, `primary-light`, `background-dark`, `surface-dark`, `surface-lighter`, `border-dark`, `text-dim`, `cyan-glow`) and gradient helpers (`cyber-gradient`, `glow-radial`).
- Global UI: `docs/src/styles/global.css` sets the Inter/system font stack and dark background; keep the same font everywhere.
- **Linting**: ESLint with Flat Config (eslint.config.mjs). Run `npm run lint` before committing. Use `npm run lint:fix` to auto-fix issues.
- Global UI: `docs/src/styles/global.css` set the Inter/system font stack and dark background; keep the same font everywhere.
- Base layout imports `../styles/global.css`; ensure new views/components respect the global palette and font.

## Image handling
- **Image storage locations**:
  - **Local assets**: Store in `docs/src/assets/` for imported images that need optimization
  - **Public images**: Store in `docs/public/assets/` or `docs/public/images/` for static images served as-is
  - **Subdirectories**: Organize by category (e.g., `public/assets/`, `public/images/`, `public/icons/`)
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
  - Local imported images auto-generate width/height; public/remote images require explicit dimensions
  - The `<Image>` component automatically optimizes formats (WebP, AVIF) and sizes
- **In Markdown/MDX content**: Use standard markdown syntax `![alt text](/images/file.png)` - Astro will optimize these automatically

## Design alignment
- Match the vibe of the **open-ticket-ai-platform-prototype**: deep purple/cyan glow, dark surfaces, soft glassy cards, generous spacing, and pill-shaped badges.
- Do not copy layouts verbatim—mirror the style and structure: layered surfaces (`surface-dark`/`surface-lighter`), neon accents (`primary`, `cyan-glow`), subtle rings/shadows, and consistent typography.
- Use the gradient utilities (`bg-cyber-gradient`, `bg-glow-radial`) and the color tokens above; avoid ad-hoc hex codes.

## Quick references
- **Components**: Live under `docs/src/components/vue/**` and are showcased via Storybook stories in `docs/stories/**`.
  - Inventory: See `COMPONENTS.md` for a complete list with brief descriptions
  - Detailed docs: Check Storybook stories (`.stories.ts` files) for usage examples and props
- **Content Collections**: Defined in `src/content/config.ts`. See `CONTENT_COLLECTIONS.md` for full documentation.
  - `docs` - Documentation pages (MD/MDX in `src/content/docs/`)
  - `blog` - Blog articles (MD/MDX in `src/content/blog/`)
  - `products` - Product listings (YAML in `src/content/products.yaml`)
  - `services` - Service offerings (YAML in `src/content/services.yaml`)
- Base layout imports `../styles/global.css`; ensure new views/components respect the global palette and font.
- **Design-system tokens**: Shared prop types defined in `docs/src/components/vue/core/design-system/tokens.ts`:
  - `Variant`: 'primary' | 'secondary' | 'outline' | 'ghost' (for buttons and UI variants)
  - `Size`: 'sm' | 'md' | 'lg' (for component sizing)
  - `Tone`: 'info' | 'success' | 'warning' | 'danger' (for semantic colors/alerts)
  - Use these types in components and their corresponding arrays (VARIANTS, SIZES, TONES) in Storybook stories for consistency.
- **Badge component**: Use `Badge` from `docs/src/components/vue/core/basic/Badge.vue` for all tag/label pills. Supports `type` prop with 'primary', 'secondary', and semantic tones. Avoid creating custom badge-like elements with inline Tailwind classes.

## Workflow expectations
- **Always lint before committing**: Run `npm run lint` to check for issues. Run `npm run lint:fix` to auto-fix.
- Use Playwright MCP to visually check UI changes (Astro on :4321, Storybook on :6006) when tweaking design-sensitive components.
- Prefer MCP-driven Storybook checks/screenshots over manual eyeballing when validating regressions.
- Whenever components or story configs change, update the corresponding Storybook stories in `docs/stories/**` to reflect new props, variants, and states.

## Documentation update rules

### When changing Vue components
**ALWAYS** update when you add/remove/rename/move Vue components under `docs/src/components/vue/`:
- [ ] Update `COMPONENTS.md` with the new component entry (name, description, props, slots)
- [ ] Create or update corresponding Storybook story in `docs/stories/**/*.stories.ts`
- [ ] Follow story naming convention: `{ComponentName}.stories.ts`
- [ ] Ensure component appears in Storybook and renders correctly

### When changing content collections
**ALWAYS** update when you modify `src/content/**` or `src/content/config.ts`:
- [ ] Update `CONTENT_COLLECTIONS.md` if schemas, fields, or conventions change
- [ ] Verify all required frontmatter fields are documented
- [ ] Test that pages using `getCollection()` still work
- [ ] Run `npm run docs:build` to verify no errors

### Quick checklist
Before finalizing component or content changes:
- Components: `COMPONENTS.md` updated + Storybook story exists + story renders
- Content: `CONTENT_COLLECTIONS.md` accurate + schema valid + pages render
- Build passes: `npm run docs:build` succeeds

## Misc
Prefer Tailwind over custom CSS where possible.
Always try avoiding merge conflicts!
