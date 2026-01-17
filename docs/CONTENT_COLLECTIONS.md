# Content Collections Guide

All collections are defined in `src/content/config.ts`.

## Astro

Use Context7 to get the Information about how content collections in Astro work !

## Accessing Localized Content

**ALWAYS** filter content by the current locale when querying collections. Use Astro's native `getCollection` function and filter the results:

**Important:** `Astro.currentLocale` is always defined (never null or undefined) due to the i18n configuration in `astro.config.mjs`. All content collection IDs start with the locale prefix followed by a slash (e.g., `en/`, `de/`).

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
- `futureReleaseDate`: Date (**Blogs only**, Optional) - When set to a future date, the blog post will not appear in the blog overview and its static path will not be generated until that date is reached
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

- `slug`: string (Optional - omit to use file path as ID)
- `meta`: `{ siteName, tagline, logoUrl }`
- `companyImage`: image() (Optional) - Company office/location image (e.g., `'../../../assets/images/open_ticket_ai_mannheim.png'`)
- `nav`: Array of `{ label, url, children? }` - Navigation items. Each item can optionally include a `children` array with nested navigation items `{ label, url }` for dropdown menus.
- `footer`: `{ brandName, sections, social, legal, copyright }`
- `ui`: UI strings for components (Required)
  - `ctaLabel`: string - Call-to-action button label (e.g., "Contact Sales")
  - `cookieBanner`: Cookie consent banner text
    - `title`: string - Banner heading
    - `description`: string - Description text
    - `privacyPolicyText`: string - Privacy policy link text
    - `acceptText`: string - Accept button text
    - `declineText`: string - Decline button text
  - `contactForm`: Contact form labels and placeholders
    - `title`: string - Form modal title
    - `submitButtonText`: string - Submit button text
    - `messageLabel`: string - Message field label
    - `emailLabel`: string - Email field label
    - `subjectLabel`: string - Subject field label
    - `emailPlaceholder`: string - Email field placeholder
    - `messagePlaceholder`: string - Message field placeholder

**Important**: Site collection files should be named with locale codes (e.g., `en.yml`, `de.yml`) and placed in locale-specific directories (`src/content/site/en/`, `src/content/site/de/`). Do not include a `slug` field - the glob loader will use the file path to generate unique IDs per locale.

## Maintenance Rules

1. **Schema Changes**: Update `src/content/config.ts`.
2. **Translation**: Ensure consistency across all locale versions of the same entry.
3. **Build Validation**: Run `npm run docs:build` to verify content against schemas.
4. **Glob Patterns**: Data collections using glob loader should use patterns that preserve locale directory structure (e.g., `*/filename.yml` instead of `**/*.yml`).
