# Code Quality & Test Improvement Suggestions

## Executive Summary

This document provides actionable strategies to improve code quality, test maintainability, and AI agent compatibility for the Open Ticket AI documentation website. The recommendations focus on leveraging existing libraries, enforcing design system consistency, and implementing comprehensive test coverage.

---

## 1. Testing Strategy Improvements

### 1.1 Current State

- **E2E Tests**: Playwright smoke tests exist (`tests/e2e/smoke.spec.ts`) but require `npx playwright install`
- **Component Tests**: **NONE** - No unit tests for Vue components
- **Storybook**: 12 story files (3,760 lines) serve as visual documentation only
- **Site Tests**: Custom script validates links and locale markers

### 1.2 Recommended Improvements

#### **A. Add Component Unit Tests with Vitest + Vue Test Utils**

**Why**: Unbreakable tests that validate component behavior independently.

**Implementation**:

```bash
npm install -D vitest @vitest/ui @vue/test-utils jsdom happy-dom
```

**Structure**:

```
docs/
  tests/
    unit/
      components/
        core/
          Button.test.ts
          Modal.test.ts
          Accordion.test.ts
    integration/
      navigation/
        NavBar.integration.test.ts
```

**Example Test Pattern** (AI-friendly, declarative):

```typescript
// tests/unit/components/core/Button.test.ts
import { describe, it, expect } from 'vitest';
import { mount } from '@vue/test-utils';
import Button from '@/components/vue/core/basic/Button.vue';

describe('Button', () => {
  it('renders with default props', () => {
    const wrapper = mount(Button, { slots: { default: 'Click me' } });
    expect(wrapper.text()).toBe('Click me');
    expect(wrapper.classes()).toContain('bg-primary');
  });

  it('applies variant classes correctly', () => {
    const wrapper = mount(Button, {
      props: { variant: 'outline', tone: 'success' },
      slots: { default: 'Save' },
    });
    expect(wrapper.classes()).toContain('border-success');
  });

  it('disables button when disabled prop is true', () => {
    const wrapper = mount(Button, {
      props: { disabled: true },
      slots: { default: 'Disabled' },
    });
    expect(wrapper.attributes('disabled')).toBeDefined();
  });
});
```

**AI Agent Benefits**:

- **Clear test names** describe exact behavior
- **Prop-based testing** maps directly to component API
- **CSS class assertions** validate design system usage
- Tests break immediately when components change

#### **B. Visual Regression Testing with Storybook**

**Why**: Catch unintended UI changes automatically.

**Implementation**:

```bash
npm install -D @storybook/test-runner playwright @storybook/addon-interactions
```

Add to `package.json`:

```json
{
  "scripts": {
    "test:storybook": "test-storybook",
    "test:storybook:ci": "concurrently -k -s first -n \"SB,TEST\" -c \"magenta,blue\" \"npm run build-storybook -- --quiet\" \"wait-on tcp:6006 && npm run test:storybook\""
  }
}
```

**Benefits**:

- Existing stories become automated tests
- AI can update stories to fix broken tests
- Visual diffs catch subtle CSS changes

#### **C. Contract Testing for Component Props**

**Why**: Ensure component APIs remain stable.

**Pattern**: Use TypeScript + Vitest to validate prop types:

```typescript
// tests/unit/components/contracts/Button.contract.test.ts
import { describe, it, expectTypeOf } from 'vitest';
import type Button from '@/components/vue/core/basic/Button.vue';

type ButtonProps = InstanceType<typeof Button>['$props'];

describe('Button Contract', () => {
  it('enforces strict variant types', () => {
    expectTypeOf<ButtonProps['variant']>().toEqualTypeOf<
      'surface' | 'outline' | 'subtle' | undefined
    >();
  });

  it('enforces strict tone types', () => {
    expectTypeOf<ButtonProps['tone']>().toEqualTypeOf<
      'neutral' | 'primary' | 'success' | 'warning' | 'danger' | 'info' | undefined
    >();
  });
});
```

---

## 2. Code Quality Issues & Fixes

### 2.1 Inconsistent Component Usage

**Issue**: Native `<button>` elements used instead of `Button` component.

**Found In**:

- `src/components/vue/domain/BlogOverview.vue` (lines 138, 196)
- `src/components/vue/core/navigation/NavBar.vue` (mobile menu toggle)
- `src/components/vue/core/basic/Tabs.vue` (tab buttons)

**Fix Strategy**:

```bash
# Create ESLint custom rule to detect native button usage
npm install -D eslint-plugin-local
```

**ESLint Rule** (add to `eslint.config.mjs`):

```javascript
{
  rules: {
    'vue/prefer-button-component': 'error',
    'vue/no-raw-button-element': 'warn'
  }
}
```

**AI-Friendly Rule**: When AI sees this error, it knows to replace `<button>` with `<Button>` from `@/components/vue/core/basic/Button.vue`.

### 2.2 Hardcoded Tailwind Classes Instead of Design System

**Issue**: Direct Tailwind classes bypass design system recipes.

**Found In**:

- `BlogOverview.vue`: 30+ instances of hardcoded `rounded-xl`, `bg-primary/10`, etc.
- `ContactSalesButton.vue`: Form input styling
- `SuccessfullFormSubmisionCard.vue`: Icon container styling

**Recommendation**: Create design system tokens for common patterns.

**Example Fix**:

```typescript
// src/components/vue/core/design-system/recipes/input.ts
export const input = tv({
  base: ['w-full rounded-xl border transition-all', 'focus:border-primary focus:ring-primary'],
  variants: {
    tone: {
      neutral: 'border-surface-lighter bg-surface-dark',
      primary: 'border-primary/30 bg-primary/5',
    },
    size: {
      sm: 'px-3 py-2 text-sm',
      md: 'px-4 py-3 text-base',
      lg: 'px-5 py-4 text-lg',
    },
  },
});
```

**Usage**:

```vue
<!-- BEFORE (hardcoded) -->
<input class="py-3... w-full rounded-xl border border-surface-lighter bg-surface-dark px-4" />

<!-- AFTER (design system) -->
<input :class="input({ tone: 'neutral', size: 'md' })" />
```

**AI Benefit**: AI can search for `class=".*rounded.*border.*bg-"` and know to replace with recipe imports.

### 2.3 Missing Transitions on Interactive Components

**Issue**: Components like `Modal`, `Accordion`, and dropdowns lack smooth transitions.

**Available**: `UiTransitionFade`, `UiTransitionSlide` exist but are **unused**.

**Fix**:

```vue
<!-- src/components/vue/core/basic/Modal.vue -->
<script setup>
import UiTransitionFade from '../transitions/UiTransitionFade.vue';
import UiTransitionFadeScale from '../transitions/UiTransitionFadeScale.vue';
</script>

<template>
  <TransitionRoot :show="open" as="template">
    <UiTransitionFade>
      <div class="fixed inset-0 bg-black/80" />
    </UiTransitionFade>
    <UiTransitionFadeScale strength="sm">
      <DialogPanel>
        <!-- Modal content -->
      </DialogPanel>
    </UiTransitionFadeScale>
  </TransitionRoot>
</template>
```

**AI Rule**: When creating/updating modals, dialogs, dropdowns, or slide-overs, ALWAYS use transition wrappers from `AGENTS.md`.

### 2.4 ESLint Violations

**Current Issues** (from `npm run lint`):

- `@typescript-eslint/ban-ts-comment`: 1 error (`.storybook/preview.ts`)
- `@typescript-eslint/no-unused-vars`: 6 errors (unused type imports)
- `vue/max-attributes-per-line`: 58 warnings

**Fix Plan**:

1. **Auto-fix formatting**: `npm run lint:fix && npm run format`
2. **Enforce on CI**: Add pre-commit hook with `husky` + `lint-staged`
3. **Remove unused types**: Delete or comment out unused types in recipe files

```bash
npm install -D husky lint-staged
npx husky init
```

**`.husky/pre-commit`**:

```bash
#!/bin/sh
npx lint-staged
```

**`package.json`**:

```json
{
  "lint-staged": {
    "*.{vue,ts,astro}": ["eslint --fix", "prettier --write"],
    "*.{md,json}": ["prettier --write"]
  }
}
```

---

## 3. Test Maintainability & AI Agent Compatibility

### 3.1 Golden File Testing for Complex Outputs

**Use Case**: ROI Calculator, Blog filtering, complex forms.

**Pattern**:

```typescript
// tests/unit/domain/BlogOverview.golden.test.ts
import { describe, it, expect } from 'vitest';
import { mount } from '@vue/test-utils';
import BlogOverview from '@/components/vue/domain/BlogOverview.vue';
import { readFileSync } from 'fs';
import { resolve } from 'path';

const goldenPosts = JSON.parse(
  readFileSync(resolve(__dirname, 'fixtures/blog-posts.golden.json'), 'utf-8')
);

describe('BlogOverview - Golden File Tests', () => {
  it('filters posts by search query', () => {
    const wrapper = mount(BlogOverview, { props: { posts: goldenPosts } });
    wrapper.vm.searchQuery = 'engineering';

    const filtered = wrapper.vm.filteredAndSortedPosts;
    expect(filtered).toHaveLength(3);
    expect(filtered.map(p => p.id)).toMatchSnapshot();
  });
});
```

**AI Update Rule**: When blog post structure changes, AI updates `blog-posts.golden.json` and reruns tests.

### 3.2 Data-Driven Test Tables

**Pattern**:

```typescript
describe.each([
  { variant: 'surface', tone: 'primary', expectedClass: 'bg-primary' },
  { variant: 'outline', tone: 'success', expectedClass: 'border-success' },
  { variant: 'subtle', tone: 'danger', expectedClass: 'text-danger' },
])('Button variant=$variant tone=$tone', ({ variant, tone, expectedClass }) => {
  it(`applies ${expectedClass}`, () => {
    const wrapper = mount(Button, { props: { variant, tone } });
    expect(wrapper.classes()).toContain(expectedClass);
  });
});
```

**AI Benefit**: Easy to add new test cases by extending the table.

### 3.3 Component Test Checklist (for AI agents)

When creating/updating a component, AI should verify:

```markdown
- [ ] Component has corresponding `.stories.ts` file
- [ ] Component has unit test in `tests/unit/components/`
- [ ] All props are typed with strict token types
- [ ] Component uses design system recipes (no hardcoded Tailwind)
- [ ] Interactive components use transitions from `core/transitions/`
- [ ] Component is documented in `COMPONENTS.md`
- [ ] ESLint passes without warnings
- [ ] Storybook renders without errors
```

---

## 4. Recommended Libraries & Tools

### 4.1 Testing

- **Vitest**: Fast unit test runner (Vite-native)
- **@vue/test-utils**: Official Vue testing library
- **@storybook/test-runner**: Automated Storybook testing
- **msw**: Mock Service Worker for API mocking
- **@testing-library/vue**: User-centric testing utilities

### 4.2 Code Quality

- **eslint-plugin-tailwindcss**: Enforce Tailwind best practices
- **eslint-plugin-vue-scoped-css**: Prevent scoped CSS issues
- **typescript-eslint**: Strict TypeScript rules
- **prettier-plugin-tailwindcss**: Auto-sort Tailwind classes

### 4.3 AI Agent Helpers

- **ts-morph**: Programmatic TypeScript AST manipulation
- **vue-component-meta**: Extract component prop types
- **zod**: Runtime schema validation for test data

---

## 5. Implementation Roadmap

### Phase 1: Foundation (Week 1)

1. Install Vitest + Vue Test Utils
2. Create test directory structure
3. Write unit tests for 5 core components (Button, Modal, Card, Badge, Alert)
4. Fix all ESLint errors
5. Set up pre-commit hooks

### Phase 2: Coverage Expansion (Week 2)

1. Add tests for remaining core components
2. Implement visual regression testing with Storybook
3. Create golden file fixtures for domain components
4. Add contract tests for component APIs

### Phase 3: Automation (Week 3)

1. Configure CI pipeline to run all tests
2. Add test coverage reporting (>80% target)
3. Create custom ESLint rules for component usage
4. Document testing patterns in `TESTING.md`

### Phase 4: AI Integration (Week 4)

1. Create test template generators for AI
2. Add AI-readable component metadata
3. Implement automated test update scripts
4. Train AI on test patterns via examples

---

## 6. Success Metrics

- **Test Coverage**: >80% for core components
- **Test Speed**: Unit tests complete in <10s
- **ESLint Compliance**: Zero warnings in CI
- **Visual Regression**: All Storybook stories pass
- **AI Agent Success Rate**: >90% correct component usage
- **Test Maintainability**: Tests update automatically when props change

---

## 7. Quick Wins (Start Here)

1. **Add Vitest** (30 min)
2. **Write Button tests** (1 hour)
3. **Fix ESLint errors** (1 hour)
4. **Add pre-commit hooks** (30 min)
5. **Document test patterns** (1 hour)

**Total**: ~4 hours for immediate impact.

---

## 8. AI Agent Guidelines (Summary)

**When creating/updating components**:

1. Use `Button` component instead of `<button>`
2. Use design system recipes instead of hardcoded Tailwind
3. Add transitions to interactive elements
4. Create unit tests + Storybook story
5. Run `npm run lint:fix && npm run format`
6. Update `COMPONENTS.md`

**When tests fail**:

1. Check if component props changed → update test props
2. Check if design system recipes changed → update expected classes
3. Check if test fixtures are stale → regenerate golden files
4. Check if Storybook args changed → sync with component props

**Red Flags** (AI should flag these):

- Native `<button>` in Vue files
- `class="rounded-..."` without recipe import
- Component without Storybook story
- Component without unit test
- ESLint warnings in CI

---

## Appendix: Test File Templates

### A. Component Unit Test Template

```typescript
// tests/unit/components/core/ComponentName.test.ts
import { describe, it, expect } from 'vitest';
import { mount } from '@vue/test-utils';
import ComponentName from '@/components/vue/core/basic/ComponentName.vue';

describe('ComponentName', () => {
  it('renders with default props', () => {
    const wrapper = mount(ComponentName);
    expect(wrapper.exists()).toBe(true);
  });

  it('applies design system classes', () => {
    const wrapper = mount(ComponentName, {
      props: { variant: 'surface', tone: 'primary' },
    });
    expect(wrapper.classes()).toContain('bg-primary');
  });

  it('emits events correctly', async () => {
    const wrapper = mount(ComponentName);
    await wrapper.trigger('click');
    expect(wrapper.emitted('click')).toHaveLength(1);
  });
});
```

### B. Storybook Story Template

```typescript
// stories/ComponentName.stories.ts
import ComponentName from '../src/components/vue/core/basic/ComponentName.vue';
import type { Meta, StoryObj } from '@storybook/vue3';
import { VARIANTS, TONES, SIZES } from '../src/components/vue/core/design-system/tokens.ts';

const meta: Meta<typeof ComponentName> = {
  title: 'Core/ComponentName',
  component: ComponentName,
  argTypes: {
    variant: { control: { type: 'select' }, options: VARIANTS },
    tone: { control: { type: 'select' }, options: TONES },
    size: { control: { type: 'select' }, options: SIZES },
  },
};
export default meta;

type Story = StoryObj<typeof meta>;

export const Default: Story = {
  args: { variant: 'surface', tone: 'primary', size: 'md' },
};
```

---

**Document Version**: 1.0  
**Last Updated**: 2026-01-14  
**Author**: GitHub Copilot  
**Review Status**: Pending Team Review
