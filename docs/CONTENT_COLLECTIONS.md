# Content Collections Guide

All collections are defined in `src/content/config.ts`.

## Accessing Localized Content

**ALWAYS** use the localized content helpers from `Astro.locals.content` (set by middleware). Do NOT use `getCollection` directly for localized content.

```astro
---
// ✅ Recommended usage
const services = await Astro.locals.content.getLocalizedCollection('services')
const site = await Astro.locals.content.getLocalizedSingleton('site')
const product = await Astro.locals.content.getLocalizedEntry('products', 'xyz')
---
```

## i18n Strategy

- **Data Collections (YAML)**: Stored in locale folders: `src/content/{collection}/{locale}/`.
- **Content Collections (MDX)**: Currently stored primarily in English under `src/content/{collection}/`.
- **Locales**: Configured in `astro.config.mjs`.

## Collections Overview

| Collection | Type | Purpose |
|------------|------|---------|
| `docs` | Content | Technical documentation and guides |
| `blog` | Content | Blog posts and announcements |
| `products` | Data | Product listings and tiers |
| `services` | Data | Service offerings and consulting |
| `site` | Data | Global site config (nav, footer, meta) |

## Key Schemas

### 1. Docs & Blogs (Common Fields)
- `title`: string (Required)
- `description`: string
- `lang`: string (Default: 'en')
- `nav`: `{ group: string, order: number, hidden: boolean }`
- `draft`: boolean
- `date`: Date (**Blogs only**, Required)
- `tags`, `category`: (**Blogs only**)

### 2. Products (YAML)
- `slug`: string (Required)
- `title`: string (Required)
- `tier`: 'lite' | 'pro' | 'enterprise'
- `features`, `badges`, `image`, `icon`

### 3. Services (YAML)
- `slug`, `title`, `serviceGroup`: string (Required)
- `oneLiner`, `description`: string
- `outcomes`: string[]
- `startingPrice`: number

### 4. Site (YAML)
- `slug`: string (Use "main")
- `meta`: `{ siteName, tagline, logoUrl }`
- `nav`: Array of `{ label, url }`
- `footer`: `{ brandName, sections, social, legal, copyright }`

## Maintenance Rules

1. **Schema Changes**: Update `src/content/config.ts`.
2. **Translation**: Ensure consistency of `slug` across all locale versions of the same entry.
3. **Build Validation**: Run `npm run docs:build` to verify content against schemas.

