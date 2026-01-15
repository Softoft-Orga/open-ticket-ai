# Icons in Open Ticket AI Docs

This project uses `astro-icon` for SVG icons. It is configured to use both Iconify (on-demand) and local icons.

## Usage in Astro Components

Import the `Icon` component from `astro-icon/components`:

```astro
---
import { Icon } from 'astro-icon/components'
---

<!-- Using Iconify (automatically fetches/bundles) -->
<Icon name="heroicons:home" />
<Icon name="heroicons:check-circle" />

<!-- Using Local Icons (from src/icons/) -->
<Icon name="local:local-test" />
```

## Configured Icon Sets

The following icon sets are pre-installed as npm dependencies for offline use and better performance:

- `heroicons` (Heroicons) - `@iconify-json/heroicons`
- `simple-icons` (Brand icons) - `@iconify-json/simple-icons`

You can use any other Iconify set by using the `prefix:name` syntax.

## Local Icons

Local icons should be placed in `docs/src/icons/` as `.svg` files.
They can be referenced using the `local:` prefix followed by the filename (without extension).

Example: `docs/src/icons/my-icon.svg` -> `<Icon name="local:my-icon" />`

## Styling Icons

You can style icons using standard CSS or Tailwind classes:

```astro
<Icon name="mdi:home" class="w-6 h-6 text-primary" />
```

