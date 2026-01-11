# Design System Recipes

This directory contains **Tailwind Variants** recipes for the Open Ticket AI design system. These recipes provide a consistent, type-safe way to apply styling across components.

## Overview

All recipes use `tailwind-variants` (`tv`) to create composable, reusable styling patterns. Each recipe exports:
- A recipe function (e.g., `button()`, `card()`)
- TypeScript types for variants (e.g., `ButtonVariants`, `CardVariants`)

## Architecture

### Shared Utilities
Foundation recipes used across the design system:

- **`surface.ts`** - Container surface styles with variant, tone, radius, elevation, hoverable, highlighted, and tint options
- **`text.ts`** - Text styling with tone and emphasis (normal/dim/strong)
- **`focus.ts`** - Focus ring styles for interactive elements

### Core UI Primitives
Component-specific recipes:

- **`card.ts`** - Card component (extends `surface` with size-based padding)
- **`button.ts`** - Button component (solid/outline/ghost variants)
- **`badge.ts`** - Badge/label component (solid/soft/outline variants)
- **`input.ts`** - Form input styling (text inputs, textareas, selects)
- **`tabs.ts`** - Tab navigation (underline/pill variants)
- **`alert.ts`** - Alert/notification component (solid/soft/outline variants)

### Documentation-Specific
- **`prose.ts`** - MDX/Markdown content wrapper with typography styles

## Usage

### Import

```typescript
// Import individual recipes
import { button, badge, card } from '@/design-system/recipes'

// Import with types
import { button, type ButtonVariants } from '@/design-system/recipes'

// Import all recipes
import * as recipes from '@/design-system/recipes'
```

### Basic Example

```typescript
import { button } from '@/design-system/recipes'

// Generate class string
const classes = button({ 
  variant: 'solid', 
  tone: 'primary', 
  size: 'md' 
})

// Use in component
<button className={classes}>Click me</button>
```

### In Vue Components

```vue
<script setup lang="ts">
import { button } from '@/design-system/recipes'

const primaryBtn = button({ variant: 'solid', tone: 'primary' })
const outlineBtn = button({ variant: 'outline', tone: 'neutral' })
</script>

<template>
  <button :class="primaryBtn">Submit</button>
  <button :class="outlineBtn">Cancel</button>
</template>
```

## Design Tokens

All recipes use the shared token vocabulary defined in `/docs/src/design-system/tokens.ts`:

- **`Variant`** - `'surface' | 'outline' | 'subtle'`
- **`Tone`** - `'neutral' | 'primary' | 'success' | 'warning' | 'danger' | 'info'`
- **`Size`** - `'sm' | 'md' | 'lg'`
- **`Radius`** - `'lg' | 'xl' | '2xl'`
- **`Elevation`** - `'none' | 'sm' | 'md' | 'lg'`

## Tailwind Classes

All recipes use existing semantic Tailwind classes from `tailwind.config.cjs`:
- Colors: `primary`, `success`, `warning`, `danger`, `info`, `surface-dark`, `border-dark`, etc.
- No hardcoded hex colors
- Compatible with dark theme

## Composition

Recipes can be composed and extended:

```typescript
import { tv } from 'tailwind-variants'
import { surface } from '@/design-system/recipes/surface'

export const customCard = tv({
  extend: surface,
  base: 'custom-additional-classes',
  variants: {
    // Add custom variants
  }
})
```

## TypeScript Support

All recipes are fully typed:

```typescript
import type { ButtonVariants } from '@/design-system/recipes'

// Use in props
interface Props {
  buttonVariant?: ButtonVariants
}

// Infer types
const btnClass = button({ variant: 'solid' })
// btnClass is type: string
```

## Best Practices

1. **Prefer recipes over inline Tailwind** - Use recipes for consistent styling
2. **Use tone, not direct colors** - Use `tone='primary'` instead of `bg-primary`
3. **Compose, don't duplicate** - Extend existing recipes instead of creating new ones
4. **Type everything** - Always import and use VariantProps types
5. **Keep defaults sensible** - Most recipes have good defaults, only override when needed

## Files

```
recipes/
├── index.ts           # Exports all recipes
├── surface.ts         # Base surface styling
├── text.ts            # Text styling
├── focus.ts           # Focus ring
├── card.ts            # Card component
├── button.ts          # Button component
├── badge.ts           # Badge component
├── input.ts           # Form input
├── tabs.ts            # Tab navigation
├── alert.ts           # Alert component
└── prose.ts           # Markdown/MDX content
```

## Examples

See individual recipe files for detailed examples and variant options.

## Migration

When migrating from inline Tailwind to recipes:

**Before:**
```vue
<button class="px-4 py-2 bg-primary text-white rounded-xl hover:bg-primary-dark">
  Click me
</button>
```

**After:**
```vue
<script setup>
import { button } from '@/design-system/recipes'
</script>

<template>
  <button :class="button({ variant: 'solid', tone: 'primary' })">
    Click me
  </button>
</template>
```

## Contributing

When adding new recipes:
1. Follow the existing pattern (import tv, export recipe + types)
2. Use existing design tokens
3. Add JSDoc comments
4. Set sensible defaults
5. Keep compoundVariants minimal (use helper variants like `tint` if needed)
6. Export in `index.ts`
