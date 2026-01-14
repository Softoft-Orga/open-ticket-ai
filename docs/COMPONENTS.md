# Vue Components Inventory

Below is an inventory of Vue components in `docs/src/components/vue`, organized by folder. Each
entry lists name, brief description, props, and slots. Descriptions are concise; adjust as
implementations evolve.

**For detailed component documentation**, including usage examples, prop types, and interactive
demos, see the corresponding Storybook stories in `docs/stories/**/*.stories.ts`. View Storybook
locally with `npm run storybook` or
visit [https://open-ticket-ai-storybook.netlify.app/](https://open-ticket-ai-storybook.netlify.app/).

## core

- **Alert.vue** — Alert/notification component using design-system alert() recipe. Props: `type` ('
  info' | 'success' | 'warning' | 'danger' | 'tip'), `variant` ('soft' | 'solid' | 'outline'),
  `title`, `hideIcon`. Slots: default (body), `footer`. Story: `stories/Alert.stories.ts`.

- **HeadlessUiTailwindDemo.vue** — Demonstrates Headless UI ui-open/ui-closed classes. Props:
  _none_. Slots: _none_. Story: `stories/HeadlessUiTailwindDemo.stories.ts`.
- **LoadingComponent.vue** — Loading spinner/placeholder. Props: `label`. Slots: _none_. Story:
  `stories/LoadingComponent.stories.ts`.

### core/accordion

- **Accordion.vue** — Accordion container. Props: `items` (Item[] | optional), `variant` ('
  default' | 'ghost' | 'bordered' | 'gradient'), `multiple` (boolean, default false), `modelValue` (
  string[] | string | optional for controlled state). Emits: `update:modelValue`. Slots: `title` (
  custom title rendering for items mode, receives { item, index, open }), default (custom content
  rendering, receives { item, index, open }). Supports both items-based rendering and manual
  composition with AccordionItem children. Story: `stories/Accordion.stories.ts`.
- **AccordionItem.vue** — Single accordion item. Props: `id` (string, required), `title` (string,
  optional), `defaultOpen` (boolean), `variant` ('default' | 'ghost' | 'bordered' | 'gradient'),
  `disabled` (boolean). Slots: `title` (receives { open }), default (body, receives { open }). Story:
  `stories/Accordion.stories.ts`.

### core/basic

- **Badge.vue** — Badge/label component using design-system badge() recipe. Props: `variant` ('
  solid' | 'soft' | 'outline'), `tone` (Tone), `size` (Size). Slots: default (badge content). Story:
  `stories/Badge.stories.ts`.
- **Button.vue** — Button component using design-system button() recipe. Props: `variant` ('
  solid' | 'outline' | 'ghost'), `tone` (Tone), `size` (Size), `radius` (Radius), `disabled`,
  `loading`, `block`, `to`, `href`. Slots: default (button content). Story: `stories/Button.stories.ts`.
- **Card.vue** — Card container using design-system card() recipe. Props: `variant` ('surface' | '
  outline' | 'subtle'), `tone` (Tone), `size` (Size), `radius` (Radius), `elevation` (Elevation),
  `hoverable`. Slots: `image`, `header`, `title`, default (content), `actions`, `footer`. Story:
  `stories/Card.stories.ts`.
- **Link.vue** — Simple link component. Props: `to`. Slots: default (link text). Story:
  `stories/Link.stories.ts`.
- **Modal.vue** — Accessible modal dialog. Props: `open` (boolean), `title` (string), `tone` (
  `neutral` | `primary` | `success` | `warning` | `danger` | `info`), `size` (`sm` | `md` | `lg`),
  `closeOnOverlay` (boolean, default: true). Emits: `close`. Slots: default (body), `title` (custom
  header), `footer` (actions). Story: `stories/Modal.stories.ts`.
- **ModalTrigger.vue** — Modal with internal state management. Manages its own `isOpen` state
  internally—no modal state leaks to parent. Props: `title` (string), `tone` (Tone), `size` (Size),
  `closeOnOverlay` (boolean, default: true). Slots: `trigger` (required, receives `{ open }`
  function), `title` (custom header), default (body), `footer` (actions). Story:
  `stories/ModalTrigger.stories.ts`.
- **Tabs.vue** — Basic tabs. Props: `tabs` (array), `initial`. Slots: default (tab panels via slot
  scope). Story: `stories/Tabs.stories.ts`.

### core/forms

- **RadioGroup.vue** — Grouped radio options. Props: `modelValue`, `label`, `disabled`. Slots:
  `description`, default (RadioGroupOption children). Story: `stories/RadioGroup.stories.ts`.
- **RadioGroupOption.vue** — Single radio option with recipe-based styling. Props: `value`, `label`,
  `description`, `variant` (Variant), `tone` (Tone). Uses `card` and `focusRing` recipes for
  consistent styling. Slots: `label`, `description`. Story: `stories/RadioGroup.stories.ts`.

### core/navigation

- **FooterComponent.vue** — Footer navigation sections. Props: `sections`, `locale`. Slots: _none_.
  Story: `stories/FooterComponent.stories.ts`.
- **NavBar.vue** — Simplified top navigation bar with logo, links, and primary CTA. Props:
  `navItems` (array of {href, label}), `currentPath` (string), `ctaLabel` (string). Slots: _none_.
  Uses Headless UI Dialog for mobile menu. Story: `stories/NavBar.stories.ts`.

### core/table

- **C.vue** — Table cell wrapper with minimal semantic classes. Props: `header` (bool), `align` ('
  left' | 'center' | 'right'). Uses Tailwind utilities for alignment and spacing. Slots: default (
  cell content). Story: `stories/Table.stories.ts`.
- **Row.vue** — Table row wrapper with recipe-based hover effects. Props: _none_. Uses Tailwind
  utilities for striped backgrounds and hover states. Slots: default (row content). Story:
  `stories/Table.stories.ts`.
- **Table.vue** — Table container using `card` recipe. Props: `variant` ('default' | 'bordered' | '
  borderless' | 'glassy' | 'compact'), `striped`, `dense`, `width` ('stretch' | 'auto' | 'full'),
  `hoverEffect`, `radius` (Radius), `elevation` (Elevation). Slots: default (rows). Story:
  `stories/Table.stories.ts`.

### core/transitions

- **UiTransitionFade.vue** — Fade transition wrapper using HeadlessUI TransitionChild. Props: _none_.
  Provides smooth opacity transitions with motion-reduce support. Use for overlays, backdrops, and
  simple fade effects. Slots: default (content to transition). Duration: 300ms enter, 200ms leave.
- **UiTransitionSlide.vue** — Slide transition wrapper using HeadlessUI TransitionChild. Props:
  `direction` ('up' | 'down' | 'left' | 'right', default: 'down'). Provides slide + fade transitions
  with motion-reduce support. Use for menus, slide-over panels, and directional animations. Slots:
  default (content to transition). Duration: 300ms enter, 200ms leave.
