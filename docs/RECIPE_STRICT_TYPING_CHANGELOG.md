# Recipe Strict Typing Migration - Changelog

## Summary
All `tailwind-variants` (`tv()`) recipes in `/docs` have been updated to use **strict typing** with values exclusively from `docs/src/design-system/tokens.ts`.

## Recipe Changes

### 1. Variant Type Updates
**Old variants → New variants (aligned with tokens.ts):**
- `solid` → `surface`
- `soft` → `subtle`
- `ghost` → `subtle`

**Affected recipes:**
- `alert.ts`: Variants updated to `surface`, `subtle`, `outline`
- `badge.ts`: Variants updated to `surface`, `subtle`, `outline`
- `button.ts`: Variants updated to `surface`, `outline`, `subtle`

### 2. Non-Token Keys Renamed
**Keys that didn't match token types were renamed:**
- `input.ts`: `state` → `validation` (values: `default`, `error`, `success`)
- `surface.ts`: `tint` → `intensity` (values: `none`, `soft`)
- `tabs.ts`: `variant` → `style` (values: `underline`, `pill`)

**Reason:** These keys use custom values that don't match any token type, so they needed different names to avoid confusion.

### 3. Strict Typing Implementation
All recipes now use `satisfies Record<TokenType, string>` to enforce strict typing:

```typescript
// Before
export const button = tv({
  variants: {
    variant: {
      solid: '...',
      outline: '...',
      ghost: '...'
    }
  }
})

// After
export const button = tv({
  variants: {
    variant: {
      surface: '...',
      outline: '...',
      subtle: '...'
    } satisfies Record<Variant, string>
  }
})
```

## Component Updates

### Vue Components
All Vue components updated to use new token types:
- `Button.vue`: Updated `variant` prop to use `Variant` type
- `Badge.vue`: Updated `variant` prop to use `Variant` type
- `Alert.vue`: Updated `variant` prop to use `Variant` type
- `Tabs.vue`: Updated `variant` → `style` prop
- `Card.vue`: Updated to import `Variant` type
- `Modal.vue`: Updated usage of `ghost` → `subtle`, `tint` → `intensity`
- `AccordionItem.vue`: Updated usage of `ghost` → `subtle`, `tint` → `intensity`
- `RadioGroupOption.vue`: Updated usage of `tint` → `intensity`

### Storybook Stories
All stories updated to use new variant names:
- `Button.stories.ts`: `BUTTON_VARIANTS` → uses `VARIANTS` from tokens, stories updated
- `Badge.stories.ts`: `BADGE_VARIANTS` → uses `VARIANTS` from tokens, stories updated
- `Alert.stories.ts`: `ALERT_VARIANTS` → uses `VARIANTS` from tokens, stories updated
- `Tabs.stories.ts`: `variant` → `style` prop, `TAB_VARIANTS` → `TAB_STYLES`
- `Card.stories.ts`: `variant="secondary"` → `variant="outline"`, `radius="md"` → `radius="lg"`
- `Table.stories.ts`: `radius="md"` → `radius="lg"`

### Astro Pages
All Astro pages updated with comprehensive replacements:
- `variant="solid"` → `variant="surface"`
- `variant="soft"` → `variant="subtle"`
- `variant="ghost"` → `variant="subtle"`
- `variant="primary"` → `variant="surface"` (primary is a tone, not a variant)
- `variant="secondary"` → `variant="outline"` (secondary was not a valid variant)
- `tone="secondary"` → `tone="neutral"` (secondary is not a valid tone)
- `size="xs"` → `size="sm"` (xs is not in Size tokens)
- Badge `type="..."` → `tone="..."` (Badge uses tone prop, not type)

**Affected pages:**
- `blog.astro`
- `index.astro`
- `products.astro`
- `products/tagging-full-pro.astro`
- `products/tagging-lite-free.astro`
- `products/tagging-lite-pro.astro`
- `roi-calculator.astro`
- `services.astro`

## Token Types (Reference)
From `docs/src/design-system/tokens.ts`:

```typescript
export type Variant = 'surface' | 'outline' | 'subtle'
export type Tone = 'neutral' | 'primary' | 'success' | 'warning' | 'danger' | 'info'
export type Size = 'sm' | 'md' | 'lg'
export type Radius = 'lg' | 'xl' | '2xl'
export type Elevation = 'none' | 'sm' | 'md' | 'lg'
export type Hoverable = boolean
export type Highlighted = boolean
```

## TypeScript Enforcement
The `satisfies` keyword ensures TypeScript will:
1. ✅ **Catch invalid variant values** at compile time
2. ✅ **Enforce token-only keys** for reserved variant names
3. ✅ **Provide autocomplete** for valid values
4. ✅ **Prevent typos** in variant definitions

Example error when using non-token values:
```
Type '"solid"' is not assignable to type '"outline" | "surface" | "subtle"'
```

## Build Status
- ✅ TypeScript check passes (21 pre-existing Storybook type warnings remain)
- ✅ Build succeeds (`npm run docs:build`)
- ✅ All recipes strictly typed with token values
- ✅ No runtime errors

## Migration Guide for Future Changes

### Adding a New Variant Value
1. Add to the appropriate type in `tokens.ts`
2. Add to the corresponding array constant (e.g., `VARIANTS`)
3. The recipe will automatically enforce the new value

### Creating a New Recipe
1. Import token types: `import type { Variant, Tone, Size } from '../tokens'`
2. Use `satisfies` for token-based variants:
   ```typescript
   variant: { ... } satisfies Record<Variant, string>
   ```
3. For custom values, use a different key name (not `variant`, `tone`, `size`, etc.)

### Forbidden Patterns
❌ Don't use token keys with custom values:
```typescript
variant: {
  custom: '...',  // Wrong! Use a different key name
  special: '...'
}
```

✅ Instead, rename the key:
```typescript
appearance: {  // Different semantic meaning
  custom: '...',
  special: '...'
}
```
