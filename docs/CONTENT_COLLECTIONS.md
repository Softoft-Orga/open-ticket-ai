# Content Collections Guide

All collections are defined in `src/content/config.ts`.

## Accessing Localized Content

**ALWAYS** filter content by the current locale when querying collections. Use Astro's native `getCollection` function and filter the results:

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

## i18n Strategy

- **Data Collections (YAML)**: Stored in locale folders: `src/content/{collection}/{locale}/`.
- **Content Collections (MDX)**: Currently stored primarily in English under `src/content/{collection}/`.
- **Locales**: Configured in `astro.config.mjs`.

## Collections Overview

| Collection | Type    | Purpose                                |
| ---------- | ------- | -------------------------------------- |
| `docs`     | Content | Technical documentation and guides     |
| `blog`     | Content | Blog posts and announcements           |
| `products` | Data    | Product listings and tiers             |
| `services` | Data    | Service offerings and consulting       |
| `site`     | Data    | Global site config (nav, footer, meta) |

## Key Schemas

### 1. Docs & Blogs (Common Fields)

- `title`: string (Required)
- `description`: string
- `lang`: string (Default: 'en')
- `nav`: `{ group: string, order: number, hidden: boolean }`
- `draft`: boolean
- `date`: Date (**Blogs only**, Required)
- `tags`, `category`: (**Blogs only**)
- `image`: string (**Blogs only**, Optional) - URL or path to blog post image

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
