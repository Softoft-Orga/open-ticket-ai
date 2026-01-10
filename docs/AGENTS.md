# Agent Notes: Docs Frontend

## Stack at a glance
- Docs site: Astro + Vite, Vue 3 components, Storybook (`docs/.storybook`) for UI review.
- Styling: Tailwind (see `docs/tailwind.config.cjs`) with the mandated palette (`primary`, `primary-dark`, `primary-light`, `background-dark`, `surface-dark`, `surface-lighter`, `border-dark`, `text-dim`, `cyan-glow`) and gradient helpers (`cyber-gradient`, `glow-radial`).
- Global UI: `docs/src/styles/global.css` sets the Inter/system font stack and dark background; keep the same font everywhere.


## Design alignment
- Match the vibe of the **open-ticket-ai-platform-prototype**: deep purple/cyan glow, dark surfaces, soft glassy cards, generous spacing, and pill-shaped badges.
- Do not copy layouts verbatim—mirror the style and structure: layered surfaces (`surface-dark`/`surface-lighter`), neon accents (`primary`, `cyan-glow`), subtle rings/shadows, and consistent typography.
- Use the gradient utilities (`bg-cyber-gradient`, `bg-glow-radial`) and the color tokens above; avoid ad-hoc hex codes.

## Quick references
- Components live under `docs/src/components/vue/**` and are showcased via Storybook stories in `docs/stories/**`.
- Base layout imports `../styles/global.css`; ensure new views/components respect the global palette and font.
- **Design-system tokens**: Shared prop types defined in `docs/src/components/vue/core/design-system/tokens.ts`:
  - `Variant`: 'primary' | 'secondary' | 'outline' | 'ghost' (for buttons and UI variants)
  - `Size`: 'sm' | 'md' | 'lg' (for component sizing)
  - `Tone`: 'info' | 'success' | 'warning' | 'danger' (for semantic colors/alerts)
  - Use these types in components and their corresponding arrays (VARIANTS, SIZES, TONES) in Storybook stories for consistency.

## Workflow expectations
- Use Playwright MCP to visually check UI changes (Astro on :4321, Storybook on :6006) when tweaking design-sensitive components.
- Prefer MCP-driven Storybook checks/screenshots over manual eyeballing when validating regressions.
- Whenever components or story configs change, update the corresponding Storybook stories in `docs/stories/**` to reflect new props, variants, and states.

## Testing Contract (Playwright)
- Avoid brittle selectors (IDs, classes, ad-hoc `data-*`). Lean on roles, labels, and visible text.
- Keep CTA accessible names stable: "Get Demo" and "Contact Sales".
- Navbar links must expose "Home", "Products", "Services", "Docs" accessible names.
- Semantic HTML + correct roles/labels are required so tests can target UX copy.
- Intentional text changes must ship with updated Playwright specs and snapshots in the same PR.
- Never merge changes that break `npm run test:e2e` (run from `docs/`).

## Misc
Prefer Tailwind over custom CSS where possible.
Always try avoiding merge conflicts!
