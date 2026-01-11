# Astro Content Collections

This directory contains the Astro Content Collections setup for Open Ticket AI documentation.

## Structure

```
src/content/
├── config.ts          # Collection definitions and schemas
├── docs/              # Documentation (MD/MDX)
├── blog/              # Blog posts (MD/MDX)
├── products/          # Product data (YAML)
└── services/          # Service data (YAML)
```

## Collections

### 1. Docs Collection (Content)
- **Type**: `content` (MD/MDX files)
- **Path**: `src/content/docs/**/*.md(x)`
- **Schema**:
  - `title` (string, required)
  - `description` (string, optional)
  - `lang` (string, default "en")
  - `nav.group` (string, optional)
  - `nav.order` (number, optional)
  - `nav.hidden` (boolean, optional)
  - `draft` (boolean, optional)

**Example:**
```md
---
title: Getting Started
description: A comprehensive guide to getting started
lang: en
nav:
  group: Introduction
  order: 1
draft: false
---

# Your content here
```

### 2. Blog Collection (Content)
- **Type**: `content` (MD/MDX files)
- **Path**: `src/content/blog/**/*.md(x)`
- **Schema**: Extends docs schema plus:
  - `date` (date, required)
  - `tags` (string[], optional)
  - `category` (string, optional)

**Example:**
```md
---
title: Introducing Open Ticket AI
description: Discover how AI is revolutionizing ticket management
date: 2024-01-15
tags:
  - announcement
  - ai
category: News
---

# Your content here
```

### 3. Products Collection (Data)
- **Type**: `data` (YAML files)
- **Path**: `src/content/products.yaml` (consolidated list)
- **Schema**:
  - `slug` (string, required)
  - `title` (string, required)
  - `tagline` (string, optional)
  - `description` (string, optional)
  - `features` (string[], optional)
  - `tier` (lite | pro | enterprise, optional)
  - `lang` (string, default "en")
  - `nav.group`, `nav.order`, `nav.hidden` (optional)

**Example:**
```yaml
- slug: open-ticket-ai-lite
  title: Open Ticket AI Lite
  tagline: Start automating your tickets with AI
  features:
    - Automatic ticket classification
    - Queue assignment
  tier: lite
```

### 4. Services Collection (Data)
- **Type**: `data` (YAML files)
- **Path**: `src/content/services.yaml`
- **Schema**:
  - `slug` (string, required)
  - `title` (string, required)
  - `oneLiner` (string, optional)
  - `description` (string, optional)
  - `outcomes` (string[], optional)
  - `startingPrice` (number, optional)
  - `lang` (string, default "en")
  - `nav.group`, `nav.order`, `nav.hidden` (optional)

**Example:**
```yaml
slug: implementation-support
title: Implementation Support
oneLiner: Get expert help setting up Open Ticket AI
startingPrice: 5000
outcomes:
  - Fully configured deployment
  - Team training
```

## Usage

### Fetching All Entries

```ts
import { getCollection } from 'astro:content';

const docs = await getCollection('docs');
const blog = await getCollection('blog');
const products = await getCollection('products');
const services = await getCollection('services');
```

### Fetching a Specific Entry

```ts
import { getEntry } from 'astro:content';

const entry = await getEntry('docs', 'getting-started');
const product = await getEntry('products', 'open-ticket-ai-lite');
```

### Filtering Entries

```ts
// Get non-draft blog posts
const publishedPosts = await getCollection('blog', ({ data }) => {
  return !data.draft;
});

// Get visible products
const visibleProducts = await getCollection('products', ({ data }) => {
  return !data.nav?.hidden;
});

// Sort by navigation order
const sortedDocs = docs.sort((a, b) => {
  return (a.data.nav?.order ?? 999) - (b.data.nav?.order ?? 999);
});
```

### Rendering Content

```astro
---
import { getEntry } from 'astro:content';

const post = await getEntry('blog', 'introducing-open-ticket-ai');
const { Content } = await post.render();
---

<article>
  <h1>{post.data.title}</h1>
  <p>{post.data.description}</p>
  <Content />
</article>
```

## Navigation

All collections support optional navigation metadata:
- `nav.group`: Group name for navigation menus
- `nav.order`: Order within the group (lower numbers first)
- `nav.hidden`: Hide from navigation (still accessible via URL)

## TypeScript Support

Type definitions are automatically generated in `.astro/content.d.ts`:

```ts
// Types are inferred from your schema
import type { CollectionEntry } from 'astro:content';

type DocEntry = CollectionEntry<'docs'>;
type BlogEntry = CollectionEntry<'blog'>;
type ProductEntry = CollectionEntry<'products'>;
type ServiceEntry = CollectionEntry<'services'>;
```

## Validation

Run `npm run docs:check` to validate your content against the schemas:

```bash
npm run docs:check
```

This will check:
- Required fields are present
- Field types match the schema
- Enum values are valid
- Date formats are correct

## Adding New Content

1. **For Docs/Blog**: Create a new `.md` or `.mdx` file in the appropriate directory
2. **For Products/Services**: Create a new `.yaml` file in the appropriate directory
3. **Validate**: Run `npm run docs:check` to ensure the schema is satisfied
4. **Build**: Run `npm run docs:build` to generate the static site

## References

- [Astro Content Collections Documentation](https://docs.astro.build/en/guides/content-collections/)
- [Zod Schema Validation](https://github.com/colinhacks/zod)
