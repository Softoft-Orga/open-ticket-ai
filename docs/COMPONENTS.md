# Vue Components Inventory

Below is an inventory of Vue components in `docs/src/components/vue`, organized by folder. Each entry lists name, brief description, props, and slots. Descriptions are concise; adjust as implementations evolve.

**For detailed component documentation**, including usage examples, prop types, and interactive demos, see the corresponding Storybook stories in `docs/stories/**/*.stories.ts`. View Storybook locally with `npm run storybook` or visit [https://open-ticket-ai-storybook.netlify.app/](https://open-ticket-ai-storybook.netlify.app/).

## (root)

## configExamples
- **ExamplePage.vue** — Renders a full example page. Props: `example` (ExampleMeta), `renderTOC` (bool). Slots: default (example content).
- **ExamplesGallery.vue** — Gallery view of examples. Props: `examples` (ExampleMeta[]), `linkBase`. Slots: _none_.
- **ExampleViewer.vue** — Viewer for selected example content. Props: `example` (ExampleMeta). Slots: default (content).
- **InlineExample.vue** — Renders inline example from registry. Props: `name`. Slots: _none_.
- **MarkdownFromString.vue** — Renders markdown string. Props: `source`. Slots: _none_.

## core
- **Alert.vue** — Alert/notification component using design-system alert() recipe. Props: `type` ('info' | 'success' | 'warning' | 'danger' | 'tip'), `variant` ('soft' | 'solid' | 'outline'), `title`, `hideIcon`. Slots: default (body), `footer`.

- **HeadlessUiTailwindDemo.vue** — Demonstrates Headless UI ui-open/ui-closed classes. Props: _none_. Slots: _none_.
- **LoadingComponent.vue** — Loading spinner/placeholder. Props: `label`. Slots: _none_.

### core/accordion
- **Accordion.vue** — Accordion container. Props: `items` (Item[] | optional), `variant` ('default' | 'ghost' | 'bordered' | 'gradient'), `multiple` (boolean, default false), `modelValue` (string[] | string | optional for controlled state). Emits: `update:modelValue`. Slots: `title` (custom title rendering for items mode, receives { item, index, open }), default (custom content rendering, receives { item, index, open }). Supports both items-based rendering and manual composition with AccordionItem children.
- **AccordionItem.vue** — Single accordion item. Props: `id` (string, required), `title` (string, optional), `defaultOpen` (boolean), `variant` ('default' | 'ghost' | 'bordered' | 'gradient'), `disabled` (boolean). Slots: `title` (receives { open }), default (body, receives { open }).

### core/basic
- **Badge.vue** — Badge/label component using design-system badge() recipe. Props: `variant` ('solid' | 'soft' | 'outline'), `tone` (Tone), `size` (Size). Slots: default (badge content).
- **Button.vue** — Button component using design-system button() recipe. Props: `variant` ('solid' | 'outline' | 'ghost'), `tone` (Tone), `size` (Size), `radius` (Radius), `disabled`, `loading`, `block`, `to`, `href`. Slots: default (button content).
- **Card.vue** — Card container using design-system card() recipe. Props: `variant` ('surface' | 'outline' | 'subtle'), `tone` (Tone), `size` (Size), `radius` (Radius), `elevation` (Elevation), `hoverable`. Slots: `image`, `header`, `title`, default (content), `actions`, `footer`.
- **Link.vue** — Simple link component. Props: `to`. Slots: default (link text).
- **Modal.vue** — Accessible modal dialog. Props: `open` (boolean), `title` (string), `tone` (`neutral` | `primary` | `success` | `warning` | `danger` | `info`), `size` (`sm` | `md` | `lg`), `closeOnOverlay` (boolean, default: true). Emits: `close`. Slots: default (body), `title` (custom header), `footer` (actions).
- **Tabs.vue** — Basic tabs. Props: `tabs` (array), `initial`. Slots: default (tab panels via slot scope).

### core/forms
- **RadioGroup.vue** — Grouped radio options. Props: `modelValue`, `options`, `disabled`. Slots: default (option rendering via slot scope).
- **RadioGroupOption.vue** — Single radio option. Props: `option`, `modelValue`, `disabled`. Slots: default (option label/body).
- **SelectComponent.vue** — Styled select. Props: `modelValue`, `options`, `label`, `placeholder`, `error`. Slots: _none_.

### core/navigation
- **FooterComponent.vue** — Footer navigation sections. Props: `sections`, `locale`. Slots: _none_.
- **NavBar.vue** — Simplified top navigation bar with logo, links, and primary CTA. Props: `navItems` (array of {href, label}), `currentPath` (string), `ctaLabel` (string). Slots: _none_. Uses Headless UI Dialog for mobile menu.

### core/table
- **C.vue** — Table cell wrapper. Props: `as` (tag), `align`, `width`. Slots: default (cell content).
- **Row.vue** — Table row wrapper. Props: `as` (tag), `hoverable`. Slots: default (row content).
- **Table.vue** — Table container. Props: `columns` (array), `striped`, `bordered`. Slots: default (rows), `header`.

### core/transitions
- **UiTransitionFade.vue** — Fade transition wrapper. Props: `as`, `appear`, `duration`. Slots: default (content).
- **UiTransitionFadeScale.vue** — Fade + scale transition wrapper. Props: `as`, `appear`, `strength`. Slots: default (content).
- **UiTransitionSlide.vue** — Slide transition wrapper. Props: `as`, `appear`, `direction`. Slots: default (content).

## homepage
- **ServiceCard.vue** — Service offering card. Props: `title`, `description`, `cta`, `icon`. Slots: `footer`.

## marketplace
- **MarketplacePagination.vue** — Pagination control. Props: `page`, `pageSize`, `total`, `onPageChange`. Slots: _none_.
- **MarketplaceSearchForm.vue** — Search form for marketplace. Props: `query`, `filters`. Slots: _none_.
- **MarketplaceSkeletonCard.vue** — Skeleton loader for marketplace cards. Props: _none_. Slots: _none_.
- **PluginCard.vue** — Plugin marketplace card. Props: `plugin` (data), `href`. Slots: _none_.
- **PluginsMarketplace.vue** — Marketplace layout with filters/list. Props: `plugins`, `isLoading`, `error`. Slots: _none_.

## multiTagDemo
- **MultiTagPredictionDemo.vue** — Multi-tag prediction demo UI. Props: _none_. Slots: _none_.
- **TagMindmap.vue** — Visual mindmap of tags. Props: `tagYaml`. Slots: _none_.
- **TagNode.vue** — Node renderer for tag tree. Props: `node`. Slots: default (node label/body).
- **TagTree.vue** — Tree view of tags. Props: `tagYaml`. Slots: _none_.
- **YamlTree.vue** — YAML tree renderer. Props: `source`. Slots: _none_.

## pipe
- **PipeSidecar.vue** — Renders sidecar data listing. Props: `sidecars`, `selected`, `onSelect`. Slots: _none_.

## predictionDemo
- **OTAIPredictionDemo.vue** — Prediction demo experience. Props: `initialMessage`, `demoConfig`. Slots: _none_.
