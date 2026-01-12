# Locale-Aware Content Collections Implementation

## Overview

This document explains the implementation of locale-aware content collections for the Open Ticket AI website. The implementation enables automatic content loading based on the user's locale using Astro 5's i18n features.

## Architecture

### 1. i18n Configuration

The site is configured in `astro.config.mjs` to support multiple locales:

```javascript
i18n: {
  locales: ['en', 'de'],
  defaultLocale: 'en',
}
```

**Note**: The custom loader and helper functions dynamically read this configuration at build time using Astro's `astro:config/server` virtual module, so you don't need to hardcode locales anywhere else.

### 2. Custom Locale YAML Loader

**File**: `src/utils/locale-yaml-loader.ts`

This custom loader:
- **Dynamically reads locales** from `astro.config.mjs` using `astro:config/server`
- Scans locale-specific folders based on the configured locales
- Loads YAML files containing arrays of items
- Assigns each entry an ID in the format `{locale}/{slug}`
- Automatically sets the `lang` field based on the folder

**Key Implementation Details**:
```typescript
import { i18n } from 'astro:config/server';
import { toCodes } from 'astro:i18n';

// Dynamically get locales from Astro config
const locales = toCodes(i18n.locales);
```

**Benefits**:
- No hardcoded locales - everything is configured in `astro.config.mjs`
- Automatic locale detection from folder structure
- Support for YAML arrays (multiple items per file)
- Easy to extend - just add new locales to `astro.config.mjs`

### 3. Content Structure

```
src/content/
├── products/
│   ├── en/
│   │   └── products.yaml
│   └── de/
│       └── products.yaml
├── services/
│   ├── en/
│   │   └── services.yaml
│   └── de/
│       └── services.yaml
└── site/
    ├── en/
    │   └── site.yml
    └── de/
        └── site.yml
```

### 4. Helper Functions

**File**: `src/utils/i18n.ts`

Provides easy-to-use functions that **dynamically get the default locale** from the Astro config:
- `getLocalizedProducts(locale)` - Get products for a specific locale
- `getLocalizedServices(locale)` - Get services for a specific locale
- `getLocalizedSiteConfig(locale)` - Get site configuration for a locale

**Key Implementation Details**:
```typescript
import { i18n } from 'astro:config/server';

function getDefaultLocale(): string {
  if (!i18n) return 'en';
  return i18n.defaultLocale || 'en';
}
```

**Usage in .astro files**:
```astro
---
import { getLocalizedProducts } from '../utils/i18n';

const currentLocale = Astro.currentLocale;
const products = await getLocalizedProducts(currentLocale);
---
```

**Note**: The locale parameter is optional. If not provided, it defaults to the `defaultLocale` from your Astro config.

## Usage Examples

### In a Page Component

```astro
---
import { getLocalizedServices } from '../utils/i18n';
import BaseLayout from '../layouts/BaseLayout.astro';

const currentLocale = Astro.currentLocale;
const allServices = await getLocalizedServices(currentLocale);

// Filter by service group
const dataServices = allServices
  .filter(s => s.data.serviceGroup === 'Synthetic Data Creation')
  .sort((a, b) => (a.data.serviceOrder || 0) - (b.data.serviceOrder || 0));
---

<BaseLayout title="Services">
  {dataServices.map(service => (
    <div>
      <h2>{service.data.title}</h2>
      <p>{service.data.description}</p>
    </div>
  ))}
</BaseLayout>
```

### In a Layout

```astro
---
import { getLocalizedSiteConfig } from '../utils/i18n';
import NavBar from '../components/vue/core/navigation/NavBar.vue';

const currentLocale = Astro.currentLocale;
const siteConfig = await getLocalizedSiteConfig(currentLocale);
const navLinks = siteConfig?.data.nav || [];
---

<NavBar client:load links={navLinks} />
```

## Adding a New Locale

To add French (`fr`) as a new locale, you only need to:

### Step 1: Update Astro Config

```javascript
// astro.config.mjs
i18n: {
  locales: ['en', 'de', 'fr'],
  defaultLocale: 'en',
}
```

**That's it!** The custom loader and helper functions will automatically detect the new locale from the config.

### Step 2: Create Content Files

```bash
mkdir -p src/content/products/fr
mkdir -p src/content/services/fr
mkdir -p src/content/site/fr

# Copy and translate files
cp src/content/products/en/products.yaml src/content/products/fr/products.yaml
cp src/content/services/en/services.yaml src/content/services/fr/services.yaml
cp src/content/site/en/site.yml src/content/site/fr/site.yml

# Edit the fr files with French translations
```

### Step 3: Test

```bash
npm run docs:build
```

**No code changes needed!** The system automatically:
- Reads the new locale from `astro.config.mjs`
- Scans the `fr/` folders for content
- Loads French content when users visit `/fr/` URLs
- Falls back to the default locale if French files are missing
cp src/content/site/en/site.yml src/content/site/fr/site.yml

# Edit the fr files with French translations
```

### Step 5: Test

```bash
npm run docs:build
```

## Best Practices

1. **Consistent Slugs**: Always use the same `slug` value across all locale files for the same item
2. **Complete Translations**: Ensure all required fields are translated in each locale
3. **Fallback Behavior**: The system defaults to English if a locale file is missing
4. **Testing**: Always test with `npm run docs:build` after adding/modifying locale files

## Troubleshooting

### Warning: "File not found: src/content/.../locale/file.yaml"

This is expected if you haven't created files for all locales. The loader will continue with available locales.

### Content not showing for a locale

1. Check that the locale folder exists
2. Verify the YAML syntax is correct
3. Ensure the `slug` matches across locales
4. Check TypeScript types in `i18n.ts`

### Build errors

1. Run `npm run lint` to check for syntax errors
2. Verify YAML indentation (2 spaces, no tabs)
3. Check that all required fields are present

## Technical Notes

- The custom loader runs during build time, not at runtime
- Each locale creates separate entries in the collection
- The `id` format `{locale}/{slug}` ensures unique identification
- Astro's `currentLocale` is automatically set based on URL routing
