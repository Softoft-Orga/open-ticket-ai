# Refactoring Analysis: Component & Helper Opportunities

## Executive Summary

This analysis identifies key opportunities to reduce code duplication and improve maintainability through reusable Astro components and helper functions. The codebase shows good component organization but has repetitive patterns across pages that can be abstracted.

## 1. Recommended Astro Components

### 1.1 HeroSection.astro **[HIGH PRIORITY]**

**Pattern Found:** Hero sections are repeated across multiple pages (index, products, services, blog) with similar structure: title, description, badge, and CTAs.

**Current Duplication:**
- 5+ pages with similar hero structures
- Each manually implements: gradient backgrounds, badge with pulse animation, title with gradient text, description, and button groups

**Proposed Component:**

```typescript
// src/components/HeroSection.astro
interface Props {
  badge?: { text: string; variant?: string };
  title: string;
  titleGradient?: string;
  description: string;
  ctas?: Array<{ label: string; href: string; variant: string; tone: string }>;
  background?: 'radial' | 'gradient' | 'dark';
}
```

**Benefits:** Consistent hero styling, reduced code by ~80-100 lines per page, centralized animation logic.

---

### 1.2 PageBreadcrumb.astro **[MEDIUM PRIORITY]**

**Pattern Found:** Breadcrumb navigation appears in product detail pages (tagging-full-pro, tagging-lite-pro, etc.).

**Current Duplication:**
```astro
// Repeated in 3+ product pages
<a href={...} class="group inline-flex items-center gap-2...">
  <Icon name="heroicons:arrow-left" class="...transition-transform..." />
  <span>PRODUCTS</span>
</a>
<span class="mx-3 text-text-dim">/</span>
<span class="font-bold">FULL PRO</span>
```

**Proposed Component:**

```typescript
interface Props {
  items: Array<{ label: string; href?: string }>;
}
```

**Benefits:** DRY principle, consistent breadcrumb styling, easier to add schema.org markup later.

---

### 1.3 FeatureGrid.astro **[HIGH PRIORITY]**

**Pattern Found:** Feature grids with icon + title + description appear on multiple pages (index.astro has 2-3 variations).

**Current Duplication:**
- Services section (3 cards)
- Tagging features (6 cards)
- Privacy features (4 cards)
- Each manually maps over arrays and duplicates Card + Icon structure

**Proposed Component:**

```typescript
interface Props {
  features: Array<{
    title: string;
    description: string;
    icon: string;
    highlight?: boolean;
  }>;
  columns?: 2 | 3 | 4;
  variant?: 'default' | 'highlight';
}
```

**Benefits:** Reduces ~40-60 lines per grid, ensures consistent spacing and responsive behavior.

---

### 1.4 SectionHeader.astro **[MEDIUM PRIORITY]**

**Pattern Found:** Section headers with Badge + Title + Description pattern repeated 8+ times across pages.

**Current Duplication:**
```astro
// Repeated pattern:
<Badge variant="..." tone="..." client:load>Label</Badge>
<h2 class="font-display mb-6 mt-6 text-4xl...">Title</h2>
<p class="mx-auto max-w-3xl text-lg...">Description</p>
```

**Proposed Component:**

```typescript
interface Props {
  badge?: { text: string; variant?: string; tone?: string };
  title: string;
  description?: string;
  centered?: boolean;
}
```

**Benefits:** Consistent section styling, ~15-20 lines saved per section.

---

### 1.5 ContactSalesModal.astro **[HIGH PRIORITY]**

**Pattern Found:** ModalTrigger + ContactForm combination appears in 4+ pages with near-identical configuration.

**Current Duplication:**
```astro
// Repeated in products.astro, services.astro, about.astro, etc.
<ModalTrigger title="Contact Sales" buttonText="CONTACT SALES" ...>
  <ContactForm
    title="Contact Sales"
    submitButtonText="Submit"
    messageLabel="Message"
    // ... 8 more props
  />
</ModalTrigger>
```

**Proposed Component:**

```typescript
interface Props {
  buttonText?: string;
  buttonVariant?: string;
  buttonSize?: string;
  // All other props with defaults from siteConfig
}
```

**Benefits:** Eliminates ~25 lines per usage, centralizes i18n text handling, consistent UX.

---

## 2. Recommended Helper Functions

### 2.1 `getLocalizedContentCollection()` **[HIGH PRIORITY]**

**Pattern Found:** Content collection filtering by locale is repeated in 4+ files with slight variations.

**Current Duplication:**
```typescript
// Repeated pattern with minor differences:
const currentLocale = (Astro.currentLocale || 'en').toLowerCase();
const allItems = await getCollection('collectionName');
const localizedItems = allItems.filter(entry =>
  entry.id.toLowerCase().startsWith(`${currentLocale}/`)
);
```

**Proposed Helper:**
```typescript
// src/utils/content.ts
export async function getLocalizedContentCollection<T extends CollectionKey>(
  collection: T,
  locale: string = 'en'
): Promise<CollectionEntry<T>[]> {
  const normalized = locale.toLowerCase();
  const all = await getCollection(collection);
  return all.filter(entry =>
    entry.id.toLowerCase().startsWith(`${normalized}/`)
  );
}
```

**Benefits:** Reduces 4-5 lines per usage, ensures consistent filtering logic, centralized locale handling.

---

### 2.2 `createLocalizedUrl()` **[MEDIUM PRIORITY]**

**Pattern Found:** Inconsistent handling of `Astro.currentLocale` with `getRelativeLocaleUrl()`.

**Current Issues:**
- Some pages use `Astro.currentLocale` (assumes always defined)
- Others use `Astro.currentLocale || 'en'` (defensive)
- Mixing these approaches across the codebase

**Proposed Helper:**
```typescript
// src/utils/i18n.ts
export function createLocalizedUrl(
  locale: string | undefined,
  path: string
): string {
  return getRelativeLocaleUrl(locale || 'en', path);
}
```

**Benefits:** Single source of truth for locale fallback, clearer intent, ~3-5 characters saved but better readability.

---

### 2.3 `formatPrice()` **[LOW PRIORITY]**

**Pattern Found:** Price formatting helper already exists in services.astro but could be extracted.

**Current State:**
```typescript
// In services.astro:
function formatPrice(price: number | undefined): string {
  if (!price || price === 0) return 'On Request';
  return `${price.toLocaleString('de-DE')} €`;
}
```

**Proposed Helper:**
```typescript
// src/utils/formatting.ts
export function formatPrice(
  price: number | undefined,
  locale: string = 'de-DE',
  currency: string = '€'
): string {
  if (!price || price === 0) return 'On Request';
  return `${price.toLocaleString(locale)} ${currency}`;
}
```

**Benefits:** Reusable across pages, consistent price display, i18n-ready.

---

### 2.4 `getSiteConfig()` **[MEDIUM PRIORITY]**

**Pattern Found:** BaseLayout.astro has complex siteConfig loading and URL localization logic that could benefit other pages.

**Current State:**
- 47 lines in BaseLayout.astro to load and process site config
- Logic for nav links, footer data, and UI text localization

**Proposed Helper:**
```typescript
// src/utils/siteConfig.ts
export async function getSiteConfig(locale: string) {
  const normalized = locale.toLowerCase();
  const allConfigs = await getCollection('site');
  const config = allConfigs.find(entry =>
    entry.id.toLowerCase().startsWith(`${normalized}/`)
  );

  return {
    raw: config,
    navLinks: localizeUrls(config?.data.nav || [], locale),
    footerData: localizeFooter(config?.data.footer, locale),
    // ... other localized helpers
  };
}
```

**Benefits:** Cleaner BaseLayout, reusable for other layouts, testable business logic.

---

## 3. Internationalization Analysis

### Current Approach: **Content-Based with Astro i18n**

**Strengths:**
✅ Uses Astro's built-in i18n routing (`prefixDefaultLocale: true`)  
✅ Content collections organized by locale prefix (`en/`, `de/`)  
✅ Centralized UI text in `site` collection (YAML)  
✅ Type-safe with Zod schemas  
✅ `getRelativeLocaleUrl()` ensures correct URL structure  

**Weaknesses:**
⚠️ **Inconsistent locale handling**: Mix of `Astro.currentLocale` vs `Astro.currentLocale || 'en'`  
⚠️ **Scattered UI text**: Some hardcoded strings in pages (e.g., "Contact Sales", "Submit")  
⚠️ **Repeated filtering logic**: Content collection locale filtering duplicated  
⚠️ **No centralized locale constant**: Fallback locale `'en'` repeated across files  

### Recommended Improvements

#### 3.1 Create i18n Constants File
```typescript
// src/utils/i18n.ts
export const DEFAULT_LOCALE = 'en' as const;
export const SUPPORTED_LOCALES = ['en', 'de'] as const;

export function getCurrentLocale(astroLocale: string | undefined): string {
  return (astroLocale || DEFAULT_LOCALE).toLowerCase();
}
```

#### 3.2 Consolidate UI Text
Move remaining hardcoded strings to `site` collection:
- Form labels (currently in ContactForm props)
- Common CTAs ("Learn More", "Read More", "Get Started")
- Status messages

#### 3.3 Create Translation Helper
```typescript
// src/utils/i18n.ts
export async function getTranslations(locale: string) {
  const config = await getSiteConfig(locale);
  return {
    t: (key: string, fallback?: string) =>
      config.raw?.data.translations?.[key] ?? fallback ?? key,
  };
}
```

### Overall i18n Assessment: **7/10**

**Good foundation** with Astro i18n and content collections. Main issues are **inconsistent patterns** and **scattered UI text**, not fundamental architecture problems. Implementing the helpers above would bring it to **9/10**.

---

## 4. Implementation Priority

### Phase 1 (Quick Wins - 2-4 hours)
1. `getLocalizedContentCollection()` helper
2. `HeroSection.astro` component
3. `ContactSalesModal.astro` component

### Phase 2 (Medium Effort - 4-6 hours)
4. `FeatureGrid.astro` component
5. `getSiteConfig()` helper
6. i18n constants and `getCurrentLocale()`

### Phase 3 (Polish - 2-3 hours)
7. `SectionHeader.astro` component
8. `PageBreadcrumb.astro` component
9. `createLocalizedUrl()` helper

---

## 5. Code Reduction Estimate

**Current State:**
- ~18 page files with significant duplication
- Estimated ~2,500-3,000 lines in pages directory

**After Refactoring:**
- Save ~800-1,000 lines across pages
- Add ~300-400 lines for new components/helpers
- **Net reduction: ~500-600 lines (20-25% reduction)**
- **Maintenance burden: -40%** (fewer places to update)

---

## Conclusion

The codebase has **solid Vue component architecture** (well-documented in COMPONENTS.md) but **pages have high duplication**. Extracting **5 key Astro components** and **4 helper functions** would significantly improve maintainability without changing functionality.

**Recommended Next Steps:**
1. Review this analysis with the team
2. Prioritize Phase 1 items (highest ROI)
3. Create feature branch for refactoring
4. Implement incrementally with tests
5. Update COMPONENTS.md for new Astro components
