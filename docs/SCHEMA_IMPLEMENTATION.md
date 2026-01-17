# Schema.org Structured Data Implementation

This document describes the structured data schemas that have been implemented across the Open Ticket AI website using `astro-seo-schema`.

## Overview

All schemas are implemented using the `astro-seo-schema` package with TypeScript support via `schema-dts`. This provides type-safe JSON-LD structured data markup for better SEO and search engine visibility.

## Site-Wide Schemas

### Organization Schema

**Location**: `BaseLayout.astro` (applied to all pages)

Provides information about Open Ticket AI as an organization:

- Organization name, URL, and logo
- Contact information
- Available languages (English, German)
- Business description

## Page-Specific Schemas

### Homepage (`/en/index.astro`)

- **WebSite Schema**: Defines the website with search action capability
- **Organization Schema**: Inherited from BaseLayout

### Product Pages

All product pages include:

- **Product Schema**: Product details including name, price, specifications
- **BreadcrumbList Schema**: Navigation breadcrumbs
- **Organization Schema**: Inherited from BaseLayout

Pages:

- `/en/products/tagging-lite-free/` - Free tier product
- `/en/products/tagging-lite-pro/` - Professional tier product
- `/en/products/tagging-full-pro/` - Enterprise tier product

### Blog Posts (`/en/blog/[...slug].astro`)

- **Article Schema**: Article metadata including headline, date, author, keywords
- **Organization Schema**: Inherited from BaseLayout

### Services Page (`/en/services.astro`)

- **WebPage Schema**: General page information
- **Organization Schema**: Inherited from BaseLayout

### About Page (`/en/company/about.astro`)

- **AboutPage Schema**: Information about the organization
- **Organization Schema**: Inherited from BaseLayout

### Products Listing (`/en/products.astro`)

- **CollectionPage Schema**: Collection of products
- **Organization Schema**: Inherited from BaseLayout

## Schema Utilities

**File**: `src/utils/schemas.ts`

Contains reusable schema generation functions:

- `getOrganizationSchema()`: Returns the base Organization schema

## How Schemas are Added

Schemas are added to pages using the `<Schema>` component from `astro-seo-schema`:

```astro
---
import { Schema } from 'astro-seo-schema';
import type { Product, WithContext } from 'schema-dts';

const productSchema: WithContext<Product> = {
  '@context': 'https://schema.org',
  '@type': 'Product',
  // ... schema properties
};
---

<BaseLayout>
  <div slot="head">
    <Schema item={productSchema} />
  </div>
  <!-- page content -->
</BaseLayout>
```

## Validation

All schemas can be validated using:

1. Google's Rich Results Test: https://search.google.com/test/rich-results
2. Schema.org Validator: https://validator.schema.org/
3. Browser DevTools: Search for `application/ld+json` in the page source

## Future Enhancements

Potential schemas to add:

- **FAQPage Schema**: For FAQ sections
- **HowTo Schema**: For tutorial/guide pages
- **SoftwareApplication Schema**: For detailed product descriptions
- **Review/Rating Schema**: When customer reviews are added
- **Event Schema**: For webinars or events
