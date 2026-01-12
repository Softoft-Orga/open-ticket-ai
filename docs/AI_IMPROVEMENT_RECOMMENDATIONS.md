# AI Capabilities Improvement Report for `/docs`

**Date:** January 2026  
**Scope:** Astro 5 + Vue 3 Documentation Website  
**Goal:** Enhance AI's ability to maintain and develop the documentation site through improved tooling, testing, and automation

---

## Executive Summary

This report analyzes the current state of the `/docs` directory and provides actionable recommendations to improve AI capabilities through better linting, testing, type safety, and automated validation. The recommendations are prioritized by impact and implementation complexity.

**Current State:**
- ✅ ESLint with flat config (Astro, Vue, TypeScript support)
- ✅ Storybook with 11 stories for 18 Vue components
- ✅ Accessibility addon enabled in Storybook
- ✅ TypeScript with strict mode
- ❌ No automated component testing (unit/integration)
- ❌ No visual regression testing
- ❌ No E2E tests for user workflows
- ❌ No CI/CD pipeline for docs-specific checks
- ❌ Limited type coverage validation

---

## 1. Component Testing Infrastructure

### 1.1 Unit Testing with Vitest + Vue Test Utils

**Priority:** HIGH  
**Impact:** Significantly improves AI's confidence in component changes  
**Effort:** Medium

#### Recommended Setup

```bash
npm install -D vitest @vitest/ui @vue/test-utils happy-dom
```

**Configuration:** `vitest.config.ts`

```typescript
import { defineConfig } from 'vitest/config';
import vue from '@vitejs/plugin-vue';
import { resolve } from 'path';

export default defineConfig({
  plugins: [vue()],
  test: {
    environment: 'happy-dom',
    globals: true,
    coverage: {
      provider: 'v8',
      reporter: ['text', 'json', 'html'],
      exclude: [
        'node_modules/',
        '.storybook/',
        'dist/',
        '**/*.stories.ts',
        '**/*.config.*'
      ],
      thresholds: {
        lines: 70,
        functions: 70,
        branches: 70,
        statements: 70
      }
    }
  },
  resolve: {
    alias: {
      '@': resolve(__dirname, './src'),
      '@data': resolve(__dirname, './data')
    }
  }
});
```

#### Package.json Scripts

```json
{
  "scripts": {
    "test": "vitest",
    "test:ui": "vitest --ui",
    "test:run": "vitest run",
    "test:coverage": "vitest run --coverage"
  }
}
```

#### Example Test Structure

```
docs/
├── src/
│   └── components/
│       └── vue/
│           └── core/
│               ├── basic/
│               │   ├── Button.vue
│               │   └── __tests__/
│               │       └── Button.test.ts
│               ├── forms/
│               │   ├── RadioGroup.vue
│               │   └── __tests__/
│               │       └── RadioGroup.test.ts
│               └── transitions/
│                   └── __tests__/
│                       └── transitions.test.ts
```

#### Sample Test: `Button.test.ts`

```typescript
import { describe, it, expect } from 'vitest';
import { mount } from '@vue/test-utils';
import Button from '../Button.vue';

describe('Button.vue', () => {
  it('renders slot content', () => {
    const wrapper = mount(Button, {
      slots: { default: 'Click me' }
    });
    expect(wrapper.text()).toContain('Click me');
  });

  it('applies correct variant classes', () => {
    const wrapper = mount(Button, {
      props: { variant: 'solid', tone: 'primary' }
    });
    expect(wrapper.classes()).toContain('variant-solid');
  });

  it('emits click event when not disabled', async () => {
    const wrapper = mount(Button);
    await wrapper.trigger('click');
    expect(wrapper.emitted()).toHaveProperty('click');
  });

  it('does not emit click when disabled', async () => {
    const wrapper = mount(Button, {
      props: { disabled: true }
    });
    await wrapper.trigger('click');
    expect(wrapper.emitted()).not.toHaveProperty('click');
  });

  it('shows loading state', () => {
    const wrapper = mount(Button, {
      props: { loading: true }
    });
    expect(wrapper.find('[role="status"]').exists()).toBe(true);
  });
});
```

**Benefits for AI:**
- Provides immediate feedback on component changes
- Prevents regressions when modifying props/slots
- Documents expected behavior through tests
- Enables confident refactoring

---

### 1.2 Storybook Test Runner + Interaction Tests

**Priority:** HIGH  
**Impact:** Validates all Storybook stories automatically  
**Effort:** Low

#### Setup

```bash
npm install -D @storybook/test-runner @storybook/testing-library @storybook/jest
```

**Configuration:** `package.json`

```json
{
  "scripts": {
    "test:storybook": "test-storybook",
    "test:storybook:ci": "concurrently -k -s first -n \"SB,TEST\" -c \"magenta,blue\" \"npm run storybook\" \"wait-on tcp:6006 && npm run test:storybook\""
  }
}
```

#### Enhance Existing Stories with Interactions

**Example:** `stories/Modal.stories.ts`

```typescript
import { userEvent, within, expect } from '@storybook/test';

export const OpenClose: Story = {
  args: { open: true },
  play: async ({ canvasElement }) => {
    const canvas = within(canvasElement);
    
    // Verify modal is visible
    await expect(canvas.getByRole('dialog')).toBeVisible();
    
    // Test close button
    const closeButton = canvas.getByLabelText('Close');
    await userEvent.click(closeButton);
    
    // Verify modal closes
    await expect(canvas.queryByRole('dialog')).not.toBeInTheDocument();
  }
};
```

**Benefits for AI:**
- Tests components in isolation with real interactions
- Catches accessibility issues (ARIA roles, labels)
- Validates keyboard navigation
- Documents user interactions

---

## 2. Visual Regression Testing

### 2.1 Playwright + Storybook Visual Tests

**Priority:** MEDIUM  
**Impact:** Prevents unintended visual changes  
**Effort:** Medium

#### Setup

```bash
npm install -D @playwright/test @storybook/addon-playwright
```

**Configuration:** `playwright.config.ts`

```typescript
import { defineConfig, devices } from '@playwright/test';

export default defineConfig({
  testDir: './tests/visual',
  fullyParallel: true,
  forbidOnly: !!process.env.CI,
  retries: process.env.CI ? 2 : 0,
  workers: process.env.CI ? 1 : undefined,
  reporter: [['html'], ['list']],
  
  use: {
    baseURL: 'http://localhost:6006',
    trace: 'on-first-retry',
    screenshot: 'only-on-failure'
  },

  projects: [
    {
      name: 'chromium',
      use: { ...devices['Desktop Chrome'] },
    },
    {
      name: 'webkit',
      use: { ...devices['Desktop Safari'] },
    }
  ],

  webServer: {
    command: 'npm run storybook',
    url: 'http://localhost:6006',
    reuseExistingServer: !process.env.CI,
    timeout: 120000
  }
});
```

#### Example Visual Test

```typescript
import { test, expect } from '@playwright/test';

test.describe('Button Visual Tests', () => {
  test('all button variants match snapshots', async ({ page }) => {
    await page.goto('/iframe.html?id=core-button--all-variants');
    await expect(page).toHaveScreenshot('button-variants.png', {
      fullPage: true,
      animations: 'disabled'
    });
  });

  test('button hover state', async ({ page }) => {
    await page.goto('/iframe.html?id=core-button--primary');
    const button = page.getByRole('button');
    await button.hover();
    await expect(page).toHaveScreenshot('button-hover.png');
  });
});
```

**Directory Structure:**

```
docs/
├── tests/
│   └── visual/
│       ├── button.spec.ts
│       ├── modal.spec.ts
│       └── __snapshots__/
│           ├── button-variants.png
│           └── button-hover.png
```

**Benefits for AI:**
- Detects unintended visual regressions
- Validates responsive behavior
- Tests dark mode / theme variations
- Ensures cross-browser consistency

---

### 2.2 Chromatic (Cloud-based Visual Testing)

**Priority:** LOW  
**Impact:** Professional visual regression testing  
**Effort:** Low (paid service)

Alternative to self-hosted Playwright visual testing. Integrates directly with Storybook.

```bash
npm install -D chromatic
```

Provides:
- Automated visual regression tests
- UI review workflow
- Component history tracking
- Collaboration features

---

## 3. Accessibility Testing Enhancements

### 3.1 Automated A11y Checks with axe-core

**Priority:** HIGH  
**Impact:** Ensures WCAG compliance  
**Effort:** Low

#### Current State
- ✅ `@storybook/addon-a11y` installed
- ⚠️ Minimal configuration in `.storybook/preview.ts`

#### Enhanced Configuration

**.storybook/preview.ts:**

```typescript
import type { Preview } from '@storybook/vue3-vite';
import '../src/styles/global.css';

const preview: Preview = {
  parameters: {
    controls: {
      matchers: {
        color: /(background|color)$/i,
        date: /Date$/i,
      },
    },
    a11y: {
      config: {
        rules: [
          {
            id: 'color-contrast',
            enabled: true
          },
          {
            id: 'label',
            enabled: true
          },
          {
            id: 'button-name',
            enabled: true
          }
        ]
      },
      options: {
        runOnly: {
          type: 'tag',
          values: ['wcag2a', 'wcag2aa', 'wcag21aa']
        }
      }
    }
  },
  tags: ['autodocs']
};

export default preview;
```

#### Automated Accessibility Tests

```bash
npm install -D @axe-core/playwright axe-core
```

**tests/a11y/components.spec.ts:**

```typescript
import { test, expect } from '@playwright/test';
import AxeBuilder from '@axe-core/playwright';

test.describe('Component Accessibility', () => {
  test('Button has no accessibility violations', async ({ page }) => {
    await page.goto('/iframe.html?id=core-button--primary');
    
    const results = await new AxeBuilder({ page })
      .withTags(['wcag2a', 'wcag2aa', 'wcag21aa'])
      .analyze();
    
    expect(results.violations).toEqual([]);
  });

  test('Modal keyboard navigation', async ({ page }) => {
    await page.goto('/iframe.html?id=core-modal--open');
    
    // Test focus trap
    await page.keyboard.press('Tab');
    const focused = await page.evaluate(() => document.activeElement?.tagName);
    expect(focused).toBe('BUTTON');
    
    // Test escape key
    await page.keyboard.press('Escape');
    const dialog = await page.locator('[role="dialog"]');
    await expect(dialog).not.toBeVisible();
  });
});
```

**Benefits for AI:**
- Catches accessibility issues automatically
- Validates keyboard navigation
- Ensures ARIA attributes are correct
- Tests focus management

---

### 3.2 Manual Accessibility Testing Checklist

Create `docs/ACCESSIBILITY_CHECKLIST.md`:

```markdown
# Accessibility Testing Checklist

For each interactive component, verify:

## Keyboard Navigation
- [ ] All interactive elements are keyboard accessible
- [ ] Tab order is logical
- [ ] Focus indicators are visible
- [ ] Escape key closes modals/menus
- [ ] Arrow keys work in menus/lists

## Screen Reader Support
- [ ] All images have alt text
- [ ] Form inputs have labels
- [ ] Buttons have accessible names
- [ ] ARIA roles are correct
- [ ] Live regions announce changes

## Visual Accessibility
- [ ] Color contrast meets WCAG AA (4.5:1 text, 3:1 UI)
- [ ] Focus indicators are visible
- [ ] Text is resizable to 200%
- [ ] No content relies on color alone

## Motion & Animation
- [ ] Respects prefers-reduced-motion
- [ ] Animations can be paused
- [ ] No auto-playing content
```

---

## 4. Type Safety Enhancements

### 4.1 Stricter TypeScript Configuration

**Priority:** MEDIUM  
**Impact:** Better type inference for AI  
**Effort:** Low

#### Enhanced `tsconfig.json`

```json
{
  "extends": "astro/tsconfigs/strict",
  "compilerOptions": {
    "jsx": "preserve",
    "jsxImportSource": "vue",
    "strict": true,
    "noUncheckedIndexedAccess": true,
    "noImplicitOverride": true,
    "noPropertyAccessFromIndexSignature": true,
    "exactOptionalPropertyTypes": true,
    "skipLibCheck": false,
    "moduleResolution": "bundler",
    "resolveJsonModule": true,
    "isolatedModules": true,
    "paths": {
      "@/*": ["./src/*"],
      "@data/*": ["./data/*"]
    }
  },
  "include": ["src/**/*", "stories/**/*", ".storybook/**/*"],
  "exclude": ["node_modules", "dist", ".astro"]
}
```

**Benefits:**
- Catches more type errors at build time
- Better autocomplete for AI code generation
- Prevents runtime errors from undefined access

---

### 4.2 Vue Component Type Checking

**Priority:** MEDIUM  
**Impact:** Validates props and emits  
**Effort:** Low

Add to `package.json`:

```json
{
  "scripts": {
    "type-check": "vue-tsc --noEmit",
    "type-check:watch": "vue-tsc --noEmit --watch"
  }
}
```

Install:
```bash
npm install -D vue-tsc
```

**Benefits:**
- Validates prop types in templates
- Checks emit signatures
- Ensures type safety in composition API

---

### 4.3 Prop Type Documentation with JSDoc

Enhance component props with JSDoc:

```typescript
export interface ButtonProps {
  /** Button visual style variant */
  variant?: 'solid' | 'outline' | 'ghost';
  
  /** Color scheme - undefined uses default theme color */
  tone?: Tone;
  
  /** Button size preset */
  size?: Size;
  
  /** Disables interaction and shows disabled styling */
  disabled?: boolean;
  
  /** Shows loading spinner and disables interaction */
  loading?: boolean;
  
  /** Makes button full width of container */
  block?: boolean;
}
```

**Benefits:**
- Better IDE autocomplete
- Self-documenting code
- AI can understand intent without reading implementation

---

## 5. Build-Time Validation

### 5.1 Content Collection Schema Validation

**Priority:** HIGH  
**Impact:** Prevents broken content  
**Effort:** Low

#### Current State
- ✅ Content collections configured
- ✅ `CONTENT_COLLECTIONS.md` documents schemas
- ⚠️ No automated validation in CI

#### Add to CI Workflow

Create `.github/workflows/docs-quality.yml`:

```yaml
name: Docs Quality Checks

on:
  push:
    paths:
      - 'docs/**'
  pull_request:
    paths:
      - 'docs/**'

jobs:
  quality:
    runs-on: ubuntu-latest
    defaults:
      run:
        working-directory: docs
    
    steps:
      - uses: actions/checkout@v4
      
      - uses: actions/setup-node@v4
        with:
          node-version: '20'
          cache: 'npm'
          cache-dependency-path: 'docs/package-lock.json'
      
      - name: Install dependencies
        run: npm ci
      
      - name: Lint
        run: npm run lint
      
      - name: Type check
        run: npm run type-check
      
      - name: Astro check (validates content schemas)
        run: npm run docs:check
      
      - name: Build
        run: npm run docs:build
      
      - name: Test
        run: npm run test:run
      
      - name: Visual tests
        run: npm run test:visual
      
      - name: Accessibility tests
        run: npm run test:a11y
```

**Benefits:**
- Catches schema violations before merge
- Validates all content frontmatter
- Ensures pages build successfully

---

### 5.2 Link Checking

**Priority:** MEDIUM  
**Impact:** Prevents broken links  
**Effort:** Low

```bash
npm install -D linkinator
```

**package.json:**

```json
{
  "scripts": {
    "check:links": "linkinator dist --recurse --skip 'external-domain.com'"
  }
}
```

Add to CI after build step.

---

### 5.3 Image Optimization Validation

**Priority:** LOW  
**Impact:** Ensures performant images  
**Effort:** Low

```bash
npm install -D sharp-cli
```

**Script to check image sizes:**

```javascript
// scripts/check-images.js
import fs from 'fs/promises';
import path from 'path';
import sharp from 'sharp';

const MAX_WIDTH = 2400;
const MAX_SIZE_KB = 500;

async function checkImages(dir) {
  const files = await fs.readdir(dir, { recursive: true });
  const issues = [];
  
  for (const file of files) {
    if (!/\.(jpg|jpeg|png|webp)$/i.test(file)) continue;
    
    const filePath = path.join(dir, file);
    const stats = await fs.stat(filePath);
    const metadata = await sharp(filePath).metadata();
    
    if (metadata.width > MAX_WIDTH) {
      issues.push(`${file}: width ${metadata.width}px exceeds ${MAX_WIDTH}px`);
    }
    
    if (stats.size > MAX_SIZE_KB * 1024) {
      issues.push(`${file}: size ${Math.round(stats.size/1024)}KB exceeds ${MAX_SIZE_KB}KB`);
    }
  }
  
  return issues;
}

const issues = await checkImages('public/images');
if (issues.length > 0) {
  console.error('Image optimization issues:', issues);
  process.exit(1);
}
```

---

## 6. End-to-End Testing

### 6.1 Critical User Flows

**Priority:** MEDIUM  
**Impact:** Validates complete user journeys  
**Effort:** Medium

#### Test Structure

```
docs/
├── tests/
│   └── e2e/
│       ├── navigation.spec.ts
│       ├── search.spec.ts
│       └── responsive.spec.ts
```

#### Example: Navigation Test

```typescript
import { test, expect } from '@playwright/test';

test.describe('Site Navigation', () => {
  test('home to docs navigation', async ({ page }) => {
    await page.goto('/');
    
    // Click docs link
    await page.click('text=Documentation');
    await expect(page).toHaveURL(/\/docs/);
    
    // Verify docs page loaded
    await expect(page.locator('h1')).toContainText('Documentation');
  });

  test('mobile menu works', async ({ page }) => {
    await page.setViewportSize({ width: 375, height: 667 });
    await page.goto('/');
    
    // Open mobile menu
    await page.click('[aria-label="Open menu"]');
    await expect(page.locator('[role="dialog"]')).toBeVisible();
    
    // Navigate
    await page.click('text=Features');
    await expect(page).toHaveURL(/\/features/);
  });
});
```

#### Search Testing

```typescript
test('pagefind search works', async ({ page }) => {
  await page.goto('/');
  
  // Wait for pagefind to initialize
  await page.waitForFunction(() => window.pagefind !== undefined);
  
  // Open search
  await page.click('[data-search-trigger]');
  
  // Type query
  await page.fill('[data-search-input]', 'button component');
  
  // Verify results
  await expect(page.locator('[data-search-results]')).toContainText('Button');
});
```

**Benefits:**
- Validates complete user workflows
- Tests JavaScript-dependent features
- Ensures responsive behavior
- Catches integration issues

---

## 7. Linting Enhancements

### 7.1 Additional ESLint Rules

**Priority:** LOW  
**Impact:** Better code quality  
**Effort:** Low

Add to `eslint.config.mjs`:

```javascript
export default [
  // ... existing config
  
  {
    files: ['**/*.vue', '**/*.ts', '**/*.astro'],
    rules: {
      // Complexity
      'complexity': ['warn', 10],
      'max-depth': ['warn', 3],
      'max-lines-per-function': ['warn', { max: 50, skipBlankLines: true }],
      
      // Best practices
      'no-console': ['warn', { allow: ['warn', 'error'] }],
      'no-debugger': 'error',
      'eqeqeq': ['error', 'always'],
      
      // TypeScript specific
      '@typescript-eslint/explicit-function-return-type': 'off',
      '@typescript-eslint/no-explicit-any': 'warn',
      '@typescript-eslint/no-unused-vars': ['error', { 
        argsIgnorePattern: '^_',
        varsIgnorePattern: '^_'
      }],
      
      // Vue specific
      'vue/component-name-in-template-casing': ['error', 'PascalCase'],
      'vue/require-default-prop': 'warn',
      'vue/require-prop-types': 'error',
      'vue/no-unused-properties': 'warn'
    }
  }
];
```

---

### 7.2 Stylelint for CSS

**Priority:** LOW  
**Impact:** Consistent styling  
**Effort:** Low

```bash
npm install -D stylelint stylelint-config-standard postcss-html
```

**stylelint.config.cjs:**

```javascript
module.exports = {
  extends: ['stylelint-config-standard'],
  rules: {
    'at-rule-no-unknown': [
      true,
      {
        ignoreAtRules: ['tailwind', 'apply', 'layer', 'config']
      }
    ]
  }
};
```

---

### 7.3 Markdown Linting

**Priority:** LOW  
**Impact:** Consistent documentation  
**Effort:** Low

```bash
npm install -D markdownlint-cli2
```

**.markdownlint.json:**

```json
{
  "default": true,
  "MD013": false,
  "MD033": false,
  "MD041": false
}
```

---

## 8. CI/CD Improvements

### 8.1 Dedicated Docs Workflow

**Priority:** HIGH  
**Impact:** Fast feedback on docs changes  
**Effort:** Low

See section 5.1 for complete workflow example.

**Key additions:**
- Run only when `docs/**` changes
- Parallel job execution
- Cache dependencies
- Upload test artifacts
- Comment PR with build preview

---

### 8.2 Preview Deployments

**Priority:** MEDIUM  
**Impact:** Visual verification before merge  
**Effort:** Low (if using Netlify)

Already configured via `netlify.toml`. Enhance with:

```toml
[build]
  command = "npm run docs:build"
  publish = "dist"

[context.deploy-preview]
  command = "npm run docs:build"

[context.branch-deploy]
  command = "npm run docs:build"

[[plugins]]
  package = "@netlify/plugin-lighthouse"

  [plugins.inputs]
    output_path = "reports/lighthouse.html"

[[plugins]]
  package = "netlify-plugin-checklinks"

  [plugins.inputs]
    checkExternal = false
    skipPatterns = ["admin"]
```

---

### 8.3 Performance Budgets

**Priority:** LOW  
**Impact:** Prevents performance regressions  
**Effort:** Medium

**lighthouse-budget.json:**

```json
{
  "budgets": [
    {
      "path": "/*",
      "timings": [
        {
          "metric": "first-contentful-paint",
          "budget": 2000
        },
        {
          "metric": "largest-contentful-paint",
          "budget": 2500
        },
        {
          "metric": "interactive",
          "budget": 3500
        }
      ],
      "resourceSizes": [
        {
          "resourceType": "script",
          "budget": 150
        },
        {
          "resourceType": "stylesheet",
          "budget": 50
        },
        {
          "resourceType": "image",
          "budget": 300
        }
      ]
    }
  ]
}
```

---

## 9. Documentation Quality

### 9.1 Component Documentation Standards

**Priority:** MEDIUM  
**Impact:** Better AI understanding of components  
**Effort:** Low

Update `COMPONENTS.md` to require:

1. **Component Purpose**: One-line description
2. **Props Table**: Name, type, default, description
3. **Slots Table**: Name, scope, description
4. **Events Table**: Name, payload, when emitted
5. **Usage Examples**: Common patterns
6. **Accessibility Notes**: ARIA roles, keyboard support
7. **Styling Notes**: CSS classes, Tailwind usage

**Template:**

```markdown
## ComponentName

**Purpose:** Brief description of what this component does.

**Location:** `src/components/vue/path/ComponentName.vue`

**Story:** `stories/ComponentName.stories.ts`

### Props

| Prop | Type | Default | Description |
|------|------|---------|-------------|
| `variant` | `'solid' \| 'outline'` | `'solid'` | Visual style variant |
| `disabled` | `boolean` | `false` | Disables interaction |

### Slots

| Slot | Scope | Description |
|------|-------|-------------|
| `default` | `{ open: boolean }` | Main content |

### Events

| Event | Payload | Description |
|-------|---------|-------------|
| `update:modelValue` | `string` | Emitted when value changes |

### Usage

```vue
<ComponentName variant="outline" @update:modelValue="handleChange">
  Content
</ComponentName>
```

### Accessibility

- Uses `role="button"` for clickable elements
- Supports keyboard navigation (Enter/Space)
- Manages focus on open/close

### Styling

- Uses `button()` recipe from design system
- Supports all tone/size variants
- Respects `motion-reduce` preference
```

---

### 9.2 ADR (Architecture Decision Records)

**Priority:** LOW  
**Impact:** Documents design decisions for AI context  
**Effort:** Low

Create `docs/architecture/decisions/`:

```
docs/
├── architecture/
│   └── decisions/
│       ├── 001-use-headlessui.md
│       ├── 002-tailwind-variants.md
│       └── 003-transition-system.md
```

**Template (ADR-001):**

```markdown
# ADR 001: Use HeadlessUI for Accessible Components

**Status:** Accepted

**Date:** 2024-01-15

## Context

Need accessible, unstyled components for modals, menus, etc.

## Decision

Use HeadlessUI for complex interactive components.

## Consequences

**Positive:**
- WCAG 2.1 AA compliance out of the box
- Keyboard navigation handled
- Focus management automatic
- Well-documented API

**Negative:**
- Additional dependency
- Vue 3 specific
- Less control over ARIA attributes

## Alternatives Considered

- Build custom accessible components (too much maintenance)
- Radix Vue (less mature ecosystem)
- Ark UI (newer, less adoption)
```

---

## 10. AI-Specific Improvements

### 10.1 Enhanced AGENTS.md

**Priority:** HIGH  
**Impact:** Better AI guidance  
**Effort:** Low

Add sections to `AGENTS.md`:

```markdown
## Testing Requirements

Before submitting changes:

1. **Run all checks:**
   ```bash
   npm run lint
   npm run type-check
   npm run test:run
   npm run docs:check
   ```

2. **Add tests for:**
   - New components → Unit test + Storybook story
   - Prop changes → Update existing tests
   - User interactions → Interaction tests
   - Visual changes → Visual regression test

3. **Update documentation:**
   - Component changes → Update COMPONENTS.md
   - New patterns → Add to relevant guide
   - Breaking changes → Add migration note

## Common Patterns

### Creating a new component

1. Create component file: `src/components/vue/core/category/ComponentName.vue`
2. Add unit test: `src/components/vue/core/category/__tests__/ComponentName.test.ts`
3. Create story: `stories/ComponentName.stories.ts`
4. Document in: `COMPONENTS.md`
5. Run tests: `npm run test ComponentName`

### Modifying an existing component

1. Update component
2. Update tests to match new behavior
3. Update story if props changed
4. Update COMPONENTS.md if API changed
5. Run: `npm run test:run && npm run lint`

## Error Resolution

### "Component not found" in tests

Add to `vitest.config.ts` aliases or check import path.

### Visual regression failure

Review diff, update snapshot if intentional:
```bash
npm run test:visual -- --update-snapshots
```

### Type error in .vue file

Run `npm run type-check` for detailed error location.
```

---

### 10.2 Code Examples Repository

**Priority:** LOW  
**Impact:** Faster AI code generation  
**Effort:** Medium

Create `docs/_examples/` with common patterns:

```
docs/
├── _examples/
│   ├── component-with-form.vue
│   ├── modal-with-confirmation.vue
│   ├── accessible-dropdown.vue
│   └── data-fetching-pattern.ts
```

Each example includes:
- Complete working code
- Comments explaining key decisions
- Links to relevant documentation
- Common pitfalls to avoid

---

### 10.3 JSON Schema for Content

**Priority:** MEDIUM  
**Impact:** Better content validation  
**Effort:** Low

Export content schemas as JSON:

```typescript
// scripts/export-schemas.ts
import { z } from 'astro:content';
import fs from 'fs/promises';

// Import your content config schemas
import { collections } from '../src/content/config';

// Generate JSON schema from Zod schemas
const schemas = Object.entries(collections).reduce((acc, [key, value]) => {
  acc[key] = {
    // Document the schema structure for validation
    // Note: Zod doesn't directly export JSON schema, 
    // so document key fields manually or use zod-to-json-schema package
    description: `Schema for ${key} collection`
  };
  return acc;
}, {});

await fs.writeFile(
  'docs/content-schemas.json',
  JSON.stringify(schemas, null, 2)
);
```

Benefits:
- AI can validate content before writing
- IDE autocomplete for frontmatter
- External tools can validate

---

## Implementation Roadmap

### Phase 1: Foundation (Week 1-2)

**High Priority, Quick Wins:**

1. ✅ Create this report
2. Setup Vitest + basic component tests
3. Add docs CI workflow
4. Enhance `tsconfig.json` with strict options
5. Add automated content validation

**Deliverables:**
- Test infrastructure working
- CI catching basic errors
- Coverage baseline established

---

### Phase 2: Testing Expansion (Week 3-4)

**Medium Priority:**

1. Write tests for all core components
2. Add Playwright visual regression tests
3. Setup Storybook test runner
4. Add E2E tests for critical flows
5. Achieve 70% code coverage

**Deliverables:**
- All components have unit tests
- Visual regressions caught automatically
- E2E flows validated

---

### Phase 3: Quality & Polish (Week 5-6)

**Lower Priority, High Value:**

1. Enhanced accessibility testing
2. Performance budgets
3. Link checking
4. ADR documentation
5. Code examples repository

**Deliverables:**
- Comprehensive quality gates
- Documentation for all patterns
- AI has rich context for development

---

## Success Metrics

### Test Coverage
- **Target:** 70% overall, 90% for core components
- **Current:** 0%

### Build Time
- **Target:** < 2 minutes for docs build
- **Current:** ~1 minute (baseline)

### Accessibility
- **Target:** 0 violations in automated tests
- **Current:** Unknown (not tested)

### Type Safety
- **Target:** 0 TypeScript errors
- **Current:** Needs audit

### CI Feedback Time
- **Target:** < 5 minutes for docs PRs
- **Current:** No dedicated workflow

---

## Cost-Benefit Analysis

### High ROI Improvements

| Improvement | Setup Time | Maintenance | AI Benefit | Priority |
|-------------|-----------|-------------|------------|----------|
| Vitest setup | 2 hours | Low | Very High | ⭐⭐⭐ |
| Docs CI workflow | 1 hour | Low | Very High | ⭐⭐⭐ |
| Enhanced TypeScript | 30 min | None | High | ⭐⭐⭐ |
| Content validation | 1 hour | Low | High | ⭐⭐⭐ |
| Storybook interactions | 4 hours | Medium | High | ⭐⭐ |

### Medium ROI Improvements

| Improvement | Setup Time | Maintenance | AI Benefit | Priority |
|-------------|-----------|-------------|------------|----------|
| Visual regression | 4 hours | Medium | Medium | ⭐⭐ |
| E2E tests | 6 hours | Medium | Medium | ⭐⭐ |
| A11y automation | 2 hours | Low | Medium | ⭐⭐ |
| Link checking | 1 hour | Low | Low | ⭐ |

### Lower ROI Improvements

| Improvement | Setup Time | Maintenance | AI Benefit | Priority |
|-------------|-----------|-------------|------------|----------|
| Performance budgets | 3 hours | Medium | Low | ⭐ |
| Stylelint | 1 hour | Low | Low | ⭐ |
| ADR documentation | Ongoing | Medium | Medium | ⭐ |
| Code examples | 8 hours | High | High | ⭐⭐ |

---

## Conclusion

Implementing these recommendations will transform the `/docs` directory from a manually-validated codebase to a fully-tested, AI-friendly development environment. The phased approach allows for incremental improvement while delivering value at each stage.

**Immediate Next Steps:**

1. Review and approve this report
2. Set up Vitest and write first component test
3. Create docs CI workflow
4. Update `AGENTS.md` with testing requirements
5. Begin Phase 1 implementation

**Long-term Vision:**

An AI agent should be able to:
- Add/modify components with confidence
- Get instant feedback on breaking changes
- Understand architectural decisions through ADRs
- Generate code following established patterns
- Ensure accessibility and performance standards
- Validate changes before human review

This foundation will make the documentation site more maintainable, accessible, and reliable while enabling AI to contribute more effectively.

---

## Appendix: Useful Resources

### Testing
- [Vitest Documentation](https://vitest.dev/)
- [Vue Test Utils](https://test-utils.vuejs.org/)
- [Playwright](https://playwright.dev/)
- [Storybook Test Runner](https://storybook.js.org/docs/writing-tests/test-runner)

### Accessibility
- [axe-core](https://github.com/dequelabs/axe-core)
- [WCAG 2.1 Guidelines](https://www.w3.org/WAI/WCAG21/quickref/)
- [A11y Project Checklist](https://www.a11yproject.com/checklist/)

### Type Safety
- [TypeScript Strict Mode](https://www.typescriptlang.org/tsconfig#strict)
- [Vue TypeScript Guide](https://vuejs.org/guide/typescript/overview.html)

### Performance
- [Lighthouse CI](https://github.com/GoogleChrome/lighthouse-ci)
- [Web Vitals](https://web.dev/vitals/)

### Astro
- [Astro Testing](https://docs.astro.build/en/guides/testing/)
- [Content Collections](https://docs.astro.build/en/guides/content-collections/)
