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

**Example Test Pattern** (AI-friendly, behavior-focused):

```typescript
// tests/unit/components/core/Button.test.ts
import { describe, it, expect } from 'vitest';
import { mount } from '@vue/test-utils';
import Button from '@/components/vue/core/basic/Button.vue';
import { button } from '@/components/vue/core/design-system/recipes';

describe('Button', () => {
  it('renders slot content', () => {
    const wrapper = mount(Button, { slots: { default: 'Click me' } });
    expect(wrapper.text()).toBe('Click me');
  });

  it('applies design system recipe classes', () => {
    const wrapper = mount(Button, {
      props: { variant: 'outline', tone: 'success', size: 'md', radius: 'xl' },
      slots: { default: 'Save' },
    });
    // Test against the recipe output, not hardcoded classes
    const expectedClasses = button({
      variant: 'outline',
      tone: 'success',
      size: 'md',
      radius: 'xl',
    });
    expect(wrapper.attributes('class')).toBe(expectedClasses);
  });

  it('becomes disabled when disabled prop is true', () => {
    const wrapper = mount(Button, {
      props: { disabled: true },
      slots: { default: 'Disabled' },
    });
    expect(wrapper.attributes('disabled')).toBeDefined();
    expect(wrapper.element).toBeDisabled();
  });

  it('emits click event when clicked', async () => {
    const wrapper = mount(Button, { slots: { default: 'Click' } });
    await wrapper.trigger('click');
    expect(wrapper.emitted('click')).toHaveLength(1);
  });
});
```

**AI Agent Benefits**:

- **Behavior-focused tests** verify component functionality, not implementation details
- **Recipe-based assertions** use the same design system source of truth
- Tests remain stable when design system recipes are updated
- **Event testing** validates component interactions
- Tests automatically adapt when design tokens change

**Why This Approach is Better**:

Testing against recipe outputs instead of hardcoded CSS classes means:

- When design system changes (e.g., `bg-primary` becomes `bg-brand-500`), tests still pass
- Tests verify the component correctly applies recipes, not specific class names
- AI agents can update recipes without breaking tests
- Maintenance is minimal - only update tests when behavior changes, not styling

#### **B. Visual Regression Testing with Storybook**

**Why**: Catch unintended UI changes automatically through visual snapshots.

**How it Works**:

Visual regression testing compares screenshots of components before and after changes:

1. **Baseline**: First run creates reference screenshots of all Storybook stories
2. **Comparison**: Subsequent runs compare new screenshots against baselines
3. **Review**: Differences are flagged for human review
4. **Update**: Approved changes become the new baseline

**Determining Intent**:

The test doesn't "know" if a change is intended - that's **your job**:

- ✅ **Intended change**: You review the diff, approve it, and update the baseline
- ❌ **Unintended change**: The diff reveals a bug; you fix the code and re-run
- 🔍 **Review workflow**: Use tools like Percy, Chromatic, or Playwright's trace viewer

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
- Catches subtle CSS bugs (margin shifts, color changes, layout breaks)
- AI can help review diffs by describing what changed
- Human approval required for baseline updates (prevents auto-accepting bugs)

**Best Practice**:

Use visual regression for **layout and appearance**, unit tests for **behavior and logic**.

#### **C. Contract Testing for Component Props**

**Why**: Ensure component APIs remain stable and use design system tokens consistently.

**Pattern**: Use TypeScript + Vitest to validate prop types against design system tokens:

```typescript
// tests/unit/components/contracts/DesignSystemTokens.contract.test.ts
import { describe, it, expectTypeOf } from 'vitest';
import type { Variant, Tone, Size, Radius } from '@/components/vue/core/design-system/tokens';

// Import all components that should use design system tokens
import type Button from '@/components/vue/core/basic/Button.vue';
import type Badge from '@/components/vue/core/basic/Badge.vue';
import type Card from '@/components/vue/core/basic/Card.vue';
import type Modal from '@/components/vue/core/basic/Modal.vue';

describe('Design System Token Contracts', () => {
  describe('Variant prop types', () => {
    it('Button uses Variant type', () => {
      type ButtonProps = InstanceType<typeof Button>['$props'];
      expectTypeOf<ButtonProps['variant']>().toEqualTypeOf<Variant | undefined>();
    });

    it('Badge uses Variant type', () => {
      type BadgeProps = InstanceType<typeof Badge>['$props'];
      expectTypeOf<BadgeProps['variant']>().toEqualTypeOf<Variant | undefined>();
    });

    it('Card uses Variant type', () => {
      type CardProps = InstanceType<typeof Card>['$props'];
      expectTypeOf<CardProps['variant']>().toEqualTypeOf<Variant | undefined>();
    });
  });

  describe('Tone prop types', () => {
    it('Button uses Tone type', () => {
      type ButtonProps = InstanceType<typeof Button>['$props'];
      expectTypeOf<ButtonProps['tone']>().toEqualTypeOf<Tone | undefined>();
    });

    it('Badge uses Tone type', () => {
      type BadgeProps = InstanceType<typeof Badge>['$props'];
      expectTypeOf<BadgeProps['tone']>().toEqualTypeOf<Tone | undefined>();
    });

    it('Modal uses Tone type', () => {
      type ModalProps = InstanceType<typeof Modal>['$props'];
      expectTypeOf<ModalProps['tone']>().toEqualTypeOf<Tone | undefined>();
    });
  });

  describe('Size prop types', () => {
    it('Button uses Size type', () => {
      type ButtonProps = InstanceType<typeof Button>['$props'];
      expectTypeOf<ButtonProps['size']>().toEqualTypeOf<Size | undefined>();
    });

    it('Badge uses Size type', () => {
      type BadgeProps = InstanceType<typeof Badge>['$props'];
      expectTypeOf<BadgeProps['size']>().toEqualTypeOf<Size | undefined>();
    });
  });

  describe('Radius prop types', () => {
    it('Button uses Radius type', () => {
      type ButtonProps = InstanceType<typeof Button>['$props'];
      expectTypeOf<ButtonProps['radius']>().toEqualTypeOf<Radius | undefined>();
    });

    it('Card uses Radius type', () => {
      type CardProps = InstanceType<typeof Card>['$props'];
      expectTypeOf<CardProps['radius']>().toEqualTypeOf<Radius | undefined>();
    });
  });
});
```

**Benefits**:

- **Centralized validation**: One test suite ensures all components use correct token types
- **Prevents drift**: Components can't use custom variants like `'primary' | 'secondary'` instead of the design system `Variant` type
- **AI-friendly**: When adding a new component, AI knows to add it to these tests
- **Compile-time safety**: TypeScript enforces these constraints during development

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

**Copilot Prompt for Implementing This Change**:

```
@workspace Update the Modal component in /docs/src/components/vue/core/basic/Modal.vue to use
the transition components. Follow these requirements:

1. Import UiTransitionFade and UiTransitionFadeScale from '../transitions/'
2. Wrap the backdrop (fixed inset-0 bg-black/80 div) with UiTransitionFade
3. Wrap the DialogPanel with UiTransitionFadeScale using strength="sm"
4. Ensure TransitionRoot wraps both transitions with :show="open" and as="template"
5. Follow the exact pattern shown in /docs/src/components/vue/core/transitions/AGENTS.md
6. Do not remove any existing functionality - only add the transitions
7. Test that the modal opens and closes smoothly with the new transitions

Reference the transition presets in /docs/src/components/vue/core/transitions/presets.ts
for the correct transition classes. The transitions should support motion-reduce preferences.
```

**For Batch Updates Across Multiple Components**:

```
@workspace Audit all interactive components in /docs/src/components/vue/core and add
appropriate transitions where missing. For each component:

1. Modal, Dialog: Use UiTransitionFade for backdrop + UiTransitionFadeScale for panel
2. Dropdown, Menu, Popover: Use UiTransitionSlide with direction='down'
3. Slide-over panels: Use UiTransitionSlide with direction='left' or 'right'
4. Toast notifications: Use UiTransitionSlide with direction='up'
5. Accordion: Optional - only if smooth collapse is needed

Follow the transition guidelines in /docs/src/components/vue/core/transitions/AGENTS.md.
Ensure all transitions include motion-reduce support. Update COMPONENTS.md for any
components that now have transitions.
```

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

**Making GitHub Copilot Agent Run Pre-commit Hooks**:

GitHub Copilot Workspace agents **do** run pre-commit hooks automatically when you use the `report_progress` tool, which internally runs `git commit`. Here's how it works:

1. **Automatic Execution**: When `report_progress` commits changes, husky hooks run automatically
2. **Hook Failures**: If lint-staged fails, the commit is rejected and Copilot sees the error
3. **Auto-fix Loop**: Copilot can read the error, run `npm run lint:fix`, and retry the commit

**How Copilot Agents Handle Pre-commit Hooks**:

```typescript
// This is what happens internally when agent uses report_progress:

1. Agent calls report_progress({ commitMessage: "...", prDescription: "..." })
2. Tool runs: git add . && git commit -m "..."
3. Husky intercepts: Runs .husky/pre-commit script
4. lint-staged runs: Lints and formats staged files
5. If linting fails: Commit aborts, error returned to agent
6. Agent sees error: Can run lint:fix and call report_progress again
7. If linting passes: Commit succeeds, code is pushed
```

**Agent-Friendly Hook Configuration**:

For best results with AI agents, configure hooks to:

- **Auto-fix when possible**: Use `--fix` flags in lint-staged
- **Fail clearly**: Return specific error messages
- **Be idempotent**: Running twice should produce the same result

**Example of Copilot Using Hooks**:

```markdown
Agent: "I'll fix the linting issues and commit the changes"
Agent: report_progress(commitMessage="Fix button component")
Hook: ❌ ESLint found 3 errors in Button.vue
Agent: "The pre-commit hook failed. Let me fix the linting errors."
Agent: bash("npm run lint:fix")
Agent: report_progress(commitMessage="Fix button component")
Hook: ✅ All checks passed
Result: Commit successful, changes pushed
```

**Limitations**:

- Agents cannot bypass hooks (this is a security feature)
- Agents must fix issues to proceed with commits
- Hooks run in the sandboxed environment with limited network access

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
- **vue-component-meta**: Extract component prop types at runtime
- **zod**: Runtime schema validation for test data

#### Setting Up vue-component-meta

**Purpose**: Automatically extract and validate component prop types, slots, and events at build time.

**Installation**:

```bash
npm install -D vue-component-meta typescript
```

**Basic Usage**:

```typescript
// scripts/extract-component-metadata.ts
import { createComponentMetaChecker } from 'vue-component-meta';
import * as path from 'path';

const tsconfigPath = path.resolve(__dirname, '../tsconfig.json');
const checker = createComponentMetaChecker(tsconfigPath, {
  forceUseTs: true,
  schema: { ignore: ['MyIgnoredNestedProps'] },
  printer: { newLine: 1 },
});

// Extract metadata for a component
const meta = checker.getComponentMeta(
  path.resolve(__dirname, '../src/components/vue/core/basic/Button.vue')
);

console.log('Props:', meta.props);
console.log('Events:', meta.events);
console.log('Slots:', meta.slots);
console.log('Exposed:', meta.exposed);

// Output example:
// Props: [
//   { name: 'variant', type: 'Variant', required: false, default: 'surface' },
//   { name: 'tone', type: 'Tone', required: false, default: 'primary' },
//   { name: 'size', type: 'Size', required: false, default: 'md' }
// ]
```

**Advanced: Generate Test Fixtures**:

```typescript
// scripts/generate-component-tests.ts
import { createComponentMetaChecker } from 'vue-component-meta';
import * as fs from 'fs';
import * as path from 'path';

const checker = createComponentMetaChecker('./tsconfig.json');

function generateTestForComponent(componentPath: string) {
  const meta = checker.getComponentMeta(componentPath);
  const componentName = path.basename(componentPath, '.vue');

  const testTemplate = `
import { describe, it, expect } from 'vitest';
import { mount } from '@vue/test-utils';
import ${componentName} from '${componentPath}';

describe('${componentName}', () => {
  it('renders with default props', () => {
    const wrapper = mount(${componentName});
    expect(wrapper.exists()).toBe(true);
  });

  ${meta.props
    .filter((p) => p.required)
    .map(
      (prop) => `
  it('requires ${prop.name} prop', () => {
    // TypeScript should enforce this at compile time
    // This test documents the requirement
  });`
    )
    .join('\n')}

  ${meta.events
    .map(
      (event) => `
  it('emits ${event.name} event', async () => {
    const wrapper = mount(${componentName});
    // Trigger the action that emits ${event.name}
    // expect(wrapper.emitted('${event.name}')).toBeTruthy();
  });`
    )
    .join('\n')}
});
`;

  const testPath = componentPath.replace('/src/', '/tests/unit/').replace('.vue', '.test.ts');
  fs.mkdirSync(path.dirname(testPath), { recursive: true });
  fs.writeFileSync(testPath, testTemplate);
}

// Generate tests for all core components
const components = [
  './src/components/vue/core/basic/Button.vue',
  './src/components/vue/core/basic/Modal.vue',
  './src/components/vue/core/basic/Card.vue',
];

components.forEach(generateTestForComponent);
```

**AI Agent Use Case**:

When AI needs to update a component, it can:

1. Run `vue-component-meta` to extract current props
2. Compare with desired changes
3. Generate updated tests automatically
4. Validate that tests still pass

**Integration with Storybook**:

```typescript
// .storybook/main.ts
export default {
  async viteFinal(config) {
    const { mergeConfig } = await import('vite');
    const { vueComponentMeta } = await import('vite-plugin-vue-component-meta');

    return mergeConfig(config, {
      plugins: [
        vueComponentMeta({
          // Automatically generate prop tables in Storybook
          exclude: ['**/node_modules/**'],
        }),
      ],
    });
  },
};
```

**Benefits for AI Agents**:

- **Automatic test generation**: AI can scaffold tests based on component metadata
- **Type safety**: Validates component APIs match TypeScript definitions
- **Documentation sync**: Ensures COMPONENTS.md stays accurate
- **Refactoring support**: Detects when prop changes break tests

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
