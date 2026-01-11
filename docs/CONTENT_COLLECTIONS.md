# Content Collections Guide

This document describes all content collections used in the Open Ticket AI website (Astro 5). All collections are defined in `src/content/config.ts`.

## Overview

The website uses four content collections:

1. **docs** - Documentation pages (Markdown/MDX)
2. **blog** - Blog articles (Markdown/MDX)
3. **products** - Product listings (YAML data)
4. **services** - Service offerings (YAML data)

## 1. Docs Collection

**Purpose**: Technical documentation, guides, and product documentation for Open Ticket AI.

**Type**: Content collection (Markdown/MDX files)

**Location**: `src/content/docs/`

**Schema Source**: `src/content/config.ts` → `docsCollection`

**Directory Structure**:
```
src/content/docs/
└── open-ticket-automation/
    ├── details/
    ├── developers/
    ├── guides/
    ├── products/
    └── users/
```

### Required Frontmatter Fields

```yaml
---
title: string                    # REQUIRED - Page title
description: string              # optional - Page description for SEO
lang: string                     # optional - Language code (default: 'en')
nav:                             # optional - Navigation metadata
  group: string                  # optional - Group name in nav
  order: number                  # optional - Sort order in nav
  hidden: boolean                # optional - Hide from navigation
draft: boolean                   # optional - Draft status
---
```

### Slug/ID Conventions

- Slugs are automatically derived from the file path relative to `src/content/docs/`
- Example: `src/content/docs/open-ticket-automation/guides/quick_start.md` → slug: `open-ticket-automation/guides/quick_start`
- File extensions (`.md`, `.mdx`) are stripped from the slug

### Language/i18n Conventions

- **Default**: English (`lang: en`)
- **No i18n structure currently**: All content is in English
- **Future**: If German content is added, it could use a `/de/` subdirectory or lang-specific files

### Routing

**Page Files**: `src/pages/docs/[...slug].astro`

**How It Works**:
1. `getStaticPaths()` calls `getCollection('docs')` to fetch all docs entries
2. Each entry is mapped to a route based on its ID (file path)
3. The page renders the entry using `DocsLayout` with breadcrumbs and TOC

**URL Pattern**: `/docs/{slug}/` where `{slug}` is the file path

### How to Add a New Docs Entry

1. Create a new `.md` or `.mdx` file in the appropriate directory under `src/content/docs/`
2. Add required frontmatter (at minimum, `title`)
3. Write your content using Markdown or MDX
4. Build the site (`npm run docs:build`) to verify
5. The page will automatically appear at `/docs/{filepath}/`

**Example**:
```markdown
---
title: My New Guide
description: A comprehensive guide to feature X
lang: en
nav:
  group: Guides
  order: 10
---

# My New Guide

Content goes here...
```

### Common Pitfalls

- **Missing title**: The `title` field is required
- **Incorrect path**: Ensure the file is under `src/content/docs/`
- **Slug conflicts**: Two files with the same relative path will conflict
- **Navigation order**: Use the `nav.order` field to control sidebar ordering
- **Draft content**: Set `draft: true` to hide work-in-progress content

---

## 2. Blog Collection

**Purpose**: Blog articles, announcements, and news posts.

**Type**: Content collection (Markdown/MDX files)

**Location**: `src/content/blog/`

**Schema Source**: `src/content/config.ts` → `blogCollection`

**Directory Structure**:
```
src/content/blog/
├── ai-in-ticketsystems.md
├── introducing-open-ticket-ai.md
├── ai-powered-classification.md
└── ...
```

### Required Frontmatter Fields

```yaml
---
title: string                    # REQUIRED - Article title
description: string              # optional - Article description/excerpt
lang: string                     # optional - Language code (default: 'en')
date: Date                       # REQUIRED - Publication date (YYYY-MM-DD)
tags: string[]                   # optional - Article tags
category: string                 # optional - Article category
nav:                             # optional - Navigation metadata
  order: number                  # optional - Sort order
draft: boolean                   # optional - Draft status
---
```

### Slug/ID Conventions

- Slugs are automatically derived from the filename (without extension)
- Example: `src/content/blog/introducing-open-ticket-ai.md` → slug: `introducing-open-ticket-ai`
- Use kebab-case for filenames

### Language/i18n Conventions

- **Default**: English (`lang: en`)
- **No i18n structure currently**: All blog posts are in English
- **Future**: Could use filename suffix pattern like `post-name.de.md` or `/de/` subdirectory

### Routing

**Page Files**: `src/pages/blog/[...slug].astro`

**How It Works**:
1. `getStaticPaths()` calls `getCollection('blog')` to fetch all blog posts
2. Each post is mapped to a route based on its ID (filename without extension)
3. The page renders the post with `BaseLayout` and article styling

**URL Pattern**: `/blog/{slug}/` where `{slug}` is the filename without extension

### How to Add a New Blog Post

1. Create a new `.md` file in `src/content/blog/`
2. Add required frontmatter (`title` and `date` are mandatory)
3. Write your article content
4. Optionally add `tags` and `category` for organization
5. Build the site to verify
6. The post will automatically appear at `/blog/{filename}/`

**Example**:
```markdown
---
title: Introducing Feature X
description: Learn about our new AI-powered feature
lang: en
date: 2024-03-15
tags:
  - announcement
  - features
  - ai
category: News
nav:
  order: 1
draft: false
---

# Introducing Feature X

Content goes here...
```

### Common Pitfalls

- **Missing date**: The `date` field is required and must be a valid date (YYYY-MM-DD)
- **Invalid date format**: Use ISO format (YYYY-MM-DD), not text dates
- **Filename conflicts**: Each blog post filename must be unique
- **Tags array**: `tags` must be an array, even for a single tag
- **Draft posts**: Remember to set `draft: false` when ready to publish

---

## 3. Products Collection

**Purpose**: Product listings and product metadata for the Open Ticket AI product suite.

**Type**: Data collection (YAML file with Astro loader)

**Location**: `src/content/products.yaml` (single YAML file)

**Schema Source**: `src/content/config.ts` → `productsCollection`

### Required Fields

```yaml
- slug: string                   # REQUIRED - Unique product identifier
  title: string                  # REQUIRED - Product name
  tagline: string                # optional - Short tagline
  description: string            # optional - Full product description
  features: string[]             # optional - List of features
  tier: 'lite' | 'pro' | 'enterprise'  # optional - Product tier
  lang: string                   # optional - Language (default: 'en')
  nav:                           # optional - Navigation metadata
    group: string                # optional - Group name
    order: number                # optional - Sort order
    hidden: boolean              # optional - Hide from listings
  status: string                 # optional - Product status
  badges: string[]               # optional - Badge labels
  image: string                  # optional - Product image URL
  icon: string                   # optional - Icon identifier
```

### Slug/ID Conventions

- Each product entry MUST have a unique `slug` field
- Use kebab-case for slugs (e.g., `open-ticket-ai-lite`, `synthetic-data-generator`)
- The slug is used to filter/find products in pages

### Language/i18n Conventions

- **Default**: English (`lang: en`)
- **No i18n currently**: All products are in English
- **Future**: Could duplicate entries with language-specific slugs or use a nested structure

### Routing

**Page Files**: 
- `src/pages/products.astro` - Main products listing page
- `src/pages/products/*.astro` - Individual product detail pages

**How It Works**:
1. Pages call `getCollection('products')` to fetch all product data
2. Products are filtered by `slug` or other criteria
3. Data is passed to Vue components (e.g., `ProductCard.vue`)

**URL Pattern**: 
- Listing: `/products/`
- Details: Custom pages like `/products/lite-pro/`, `/products/full-pro/`

### How to Add a New Product

1. Open `src/content/products.yaml`
2. Add a new YAML entry with required fields (`slug`, `title`)
3. Fill in optional fields as needed
4. Save the file
5. Use the product in pages by filtering: `allProducts.find(p => p.data.slug === 'your-slug')`
6. Build the site to verify

**Example**:
```yaml
- slug: new-product
  title: New Product Name
  tagline: A revolutionary solution
  description: |
    Detailed description of the product.
    Can span multiple lines.
  features:
    - Feature one
    - Feature two
    - Feature three
  tier: pro
  lang: en
  nav:
    group: Products
    order: 5
    hidden: false
  image: https://example.com/image.png
```

### Common Pitfalls

- **YAML syntax errors**: Indentation matters! Use 2 spaces, not tabs
- **Missing slug**: Every entry needs a unique `slug`
- **Duplicate slugs**: Will cause conflicts when filtering products
- **Array syntax**: Use `- item` format for arrays (features, badges)
- **Multiline strings**: Use `|` for multiline descriptions
- **Schema validation**: Invalid `tier` values will fail validation (must be 'lite', 'pro', or 'enterprise')

---

## 4. Services Collection

**Purpose**: Service offerings, consulting packages, and professional services.

**Type**: Data collection (YAML file with Astro loader)

**Location**: `src/content/services.yaml` (single YAML file)

**Schema Source**: `src/content/config.ts` → `servicesCollection`

### Required Fields

```yaml
- slug: string                   # REQUIRED - Unique service identifier
  title: string                  # REQUIRED - Service name
  oneLiner: string               # optional - Brief tagline
  description: string            # optional - Full service description
  outcomes: string[]             # optional - List of deliverables/outcomes
  startingPrice: number          # optional - Starting price in currency
  lang: string                   # optional - Language (default: 'en')
  serviceGroup: string           # REQUIRED - Service category/group
  serviceOrder: number           # optional - Sort order within group
  hidden: boolean                # optional - Hide from listings
```

### Slug/ID Conventions

- Each service entry MUST have a unique `slug` field
- Use kebab-case for slugs (e.g., `custom-development`, `integration-basic`)
- The slug is used to filter/find services in pages

### Service Groups

Services are organized by `serviceGroup`:
- `"Synthetic Data Creation"` - Data generation services
- `"Extensions"` - Extension and plugin services
- `"Integration"` - Integration services
- `"Model Development"` - Custom model development
- (Add new groups as needed)

### Language/i18n Conventions

- **Default**: English (`lang: en`)
- **No i18n currently**: All services are in English
- **Future**: Could duplicate entries with language-specific slugs

### Routing

**Page Files**: 
- `src/pages/services.astro` - Main services listing page

**How It Works**:
1. Page calls `getCollection('services')` to fetch all service data
2. Services are filtered by `serviceGroup` and sorted by `serviceOrder`
3. Data is rendered directly in the services page using inline Astro markup and Tailwind classes

**URL Pattern**: `/services/` (single page with all services grouped)

### How to Add a New Service

1. Open `src/content/services.yaml`
2. Add a new YAML entry with required fields (`slug`, `title`, `serviceGroup`)
3. Fill in optional fields as needed
4. Set `serviceOrder` to control position within its group
5. Save the file
6. The service will automatically appear on `/services/` grouped by `serviceGroup`

**Example**:
```yaml
- slug: new-service
  title: New Service Name
  oneLiner: Brief description
  description: |
    Full description of the service.
    Multiple lines supported.
  outcomes:
    - Deliverable one
    - Deliverable two
    - Deliverable three
  startingPrice: 5000
  lang: en
  serviceGroup: Integration
  serviceOrder: 10
  hidden: false
```

### Common Pitfalls

- **YAML syntax errors**: Indentation matters! Use 2 spaces, not tabs
- **Missing required fields**: `slug`, `title`, and `serviceGroup` are required
- **Duplicate slugs**: Will cause conflicts
- **Service order**: Use `serviceOrder` to control positioning; defaults to 0 if omitted
- **Price field**: `startingPrice` must be a number, not a string
- **Hidden services**: Set `hidden: true` to remove from display (useful for WIP entries)

---

## Updating Content Collections

### When You Change Collections

**If you modify `src/content/config.ts`** (add/remove collections, change schemas):
1. **MUST** update this file (`CONTENT_COLLECTIONS.md`)
2. **MUST** verify all pages using `getCollection()` still work
3. **MUST** check TypeScript types are valid

**If you add/remove/modify collection entries**:
1. Update this file if conventions or structure change
2. Test the relevant pages (`npm run docs:dev`)
3. Rebuild the site (`npm run docs:build`)

### Validation Checklist

Before committing changes to content collections:

- [ ] Schema changes reflected in `config.ts`
- [ ] `CONTENT_COLLECTIONS.md` updated with new fields/collections
- [ ] All required frontmatter fields present
- [ ] No YAML syntax errors (for products/services)
- [ ] Site builds without errors (`npm run docs:build`)
- [ ] Pages render correctly (`npm run docs:dev`)
- [ ] Links and routes work as expected

---

## Related Documentation

- **Component Documentation**: See `COMPONENTS.md` for Vue component inventory
- **Component Details**: Check Storybook stories in `stories/**/*.stories.ts`
- **Agent Instructions**: See `AGENTS.md` and `.github/copilot-instructions.md`
- **Astro Content Collections**: [Astro Docs](https://docs.astro.build/en/guides/content-collections/)
