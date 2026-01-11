# Vue Components Inventory

Below is an inventory of Vue components in `docs/src/components/vue`, organized by folder. Each entry lists name, brief description, props, and slots. Descriptions are concise; adjust as implementations evolve.

**For detailed component documentation**, including usage examples, prop types, and interactive demos, see the corresponding Storybook stories in `docs/stories/**/*.stories.ts`. View Storybook locally with `npm run storybook` or visit [https://open-ticket-ai-storybook.netlify.app/](https://open-ticket-ai-storybook.netlify.app/).

## (root)

## blog
- **ArticleCard.vue** — Blog article card with title, meta, and excerpt. Props: `title`, `description`, `readingTime`, `publishedAt`, `author`, `tags`, `slug`. Slots: _none_.
- **AuthorBio.vue** — Author bio block with avatar and socials. Props: `author`, `avatar`, `role`, `website`, `twitter`, `linkedin`, `github`, `dribbble`. Slots: default (bio content).
- **ReadingTime.vue** — Displays estimated reading time. Props: `minutes`. Slots: _none_.
- **RelatedPosts.vue** — Grid of related posts. Props: `posts`. Slots: _none_.
- **ShareButtons.vue** — Social share buttons. Props: `url`, `title`. Slots: _none_.
- **TagFilter.vue** — Filter pill list for tags. Props: `tags`, `activeTags`, `title`. Slots: _none_.
- **TopicLink.vue** — Link styled for topics. Props: `label`, `href`. Slots: _none_.

## configExamples
- **ExampleCard.vue** — Card wrapper for a config example. Props: `example` (ExampleMeta), `linkBase`. Slots: _none_.
- **ExampleGrid.vue** — Grid layout for example cards. Props: `examples` (ExampleMeta[]). Slots: _none_.
- **ExamplePage.vue** — Renders a full example page. Props: `example` (ExampleMeta), `renderTOC` (bool). Slots: default (example content).
- **ExamplesGallery.vue** — Gallery view of examples. Props: `examples` (ExampleMeta[]), `linkBase`. Slots: _none_.
- **ExampleViewer.vue** — Viewer for selected example content. Props: `example` (ExampleMeta). Slots: default (content).
- **InlineExample.vue** — Renders inline example from registry. Props: `name`. Slots: _none_.
- **MarkdownFromString.vue** — Renders markdown string. Props: `source`. Slots: _none_.
- **SearchBox.vue** — Search input for examples. Props: `placeholder`. Slots: _none_.
- **TagBadges.vue** — Badge list for tags. Props: `tags`. Slots: _none_.
- **TagFilter.vue** — Tag filter control. Props: `tags`, `activeTags`. Slots: _none_.

## core
- **Alert.vue** — Alert banner with tone. Props: `title`, `tone` (`info` | `success` | `warning` | `danger`), `icon`. Slots: default (body).
- **DocCard.vue** — Card for documentation links. Props: `title`, `description`, `href`, `icon`. Slots: _none_.
- **HeadlessUiTailwindDemo.vue** — Demonstrates Headless UI ui-open/ui-closed classes. Props: _none_. Slots: _none_.
- **LoadingComponent.vue** — Loading spinner/placeholder. Props: `label`. Slots: _none_.
- **QuickLink.vue** — Inline link pill. Props: `label`, `href`, `icon`. Slots: _none_.

### core/accordion
- **Accordion.vue** — Accordion container. Props: `items` (array), `multiple` (bool). Slots: default (custom items).
- **AccordionItem.vue** — Single accordion item. Props: `item`, `isOpen`, `disabled`. Slots: `title`, default (body).

### core/basic
- **Badge.vue** — Pill badge. Props: `label`, `tone`, `size`, `icon`. Slots: default (custom content).
- **Button.vue** — Styled button. Props: `label`, `variant`, `size`, `to`, `href`, `icon`, `block`, `loading`, `disabled`. Slots: default (button content).
- **Card.vue** — Card container. Props: `title`, `description`, `icon`, `link`. Slots: default (content), `footer`.
- **Link.vue** — Simple link component. Props: `to`. Slots: default (link text).
- **Tabs.vue** — Basic tabs. Props: `tabs` (array), `initial`. Slots: default (tab panels via slot scope).

### core/forms
- **RadioGroup.vue** — Grouped radio options. Props: `modelValue`, `options`, `disabled`. Slots: default (option rendering via slot scope).
- **RadioGroupOption.vue** — Single radio option. Props: `option`, `modelValue`, `disabled`. Slots: default (option label/body).
- **SelectComponent.vue** — Styled select. Props: `modelValue`, `options`, `label`, `placeholder`, `error`. Slots: _none_.

### core/navigation
- **FooterComponent.vue** — Footer navigation sections. Props: `sections`, `locale`. Slots: _none_.
- **NavBar.vue** — Top navigation bar. Props: `links`, `cta`, `mobileOnlyLinks`. Slots: default (extra actions).

### core/table
- **C.vue** — Table cell wrapper. Props: `as` (tag), `align`, `width`. Slots: default (cell content).
- **Row.vue** — Table row wrapper. Props: `as` (tag), `hoverable`. Slots: default (row content).
- **Table.vue** — Table container. Props: `columns` (array), `striped`, `bordered`. Slots: default (rows), `header`.

### core/transitions
- **UiTransitionFade.vue** — Fade transition wrapper. Props: `as`, `appear`, `duration`. Slots: default (content).
- **UiTransitionFadeScale.vue** — Fade + scale transition wrapper. Props: `as`, `appear`, `strength`. Slots: default (content).
- **UiTransitionSlide.vue** — Slide transition wrapper. Props: `as`, `appear`, `direction`. Slots: default (content).

## forms
- **ServiceInquiryModal.vue** — Modal for service inquiries. Props: `open`, `onClose`. Slots: default (form body).

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
