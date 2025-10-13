# PipeSidecar Component

## Overview
The PipeSidecar component displays comprehensive information about pipeline pipe configurations from sidecar YAML specifications.

## Usage

### Basic Usage
```vue
<PipeSidecar :sidecar="pipeSidecarData" />
```

### With Action Buttons
```vue
<PipeSidecar :sidecar="pipeSidecarData">
  <template #actions>
    <button @click="runPipe">Run Pipe</button>
    <button @click="viewDocs">View Docs</button>
  </template>
</PipeSidecar>
```

## Props

| Prop | Type | Required | Description |
|------|------|----------|-------------|
| sidecar | PipeSidecar | Yes | The pipe sidecar configuration object |

## Slots

| Slot | Description |
|------|-------------|
| actions | Optional slot for custom action buttons (e.g., "Run Pipe", "View Docs") |

## Features

- **Metadata Display**: Shows pipe class, inheritance, title, summary, category, and version
- **Input Configuration**: Displays input parameters with descriptions, placement, and alongside fields
- **Default Values**: Lists all default parameter values
- **Output States**: Shows possible output states (ok, skipped, failed) with color-coded badges
- **Error Handling**: Categorizes errors into fail, break, and continue with visual distinction
- **Engine Support**: Displays engine capability flags
- **Usage Examples**: Collapsible accordion sections for minimal, full, and large configuration examples
- **Responsive Design**: Uses Tailwind CSS for responsive layouts
- **Dark Mode Support**: Compatible with VitePress dark/light theme switching

## Accessibility

The component follows accessibility best practices:
- Semantic HTML structure with proper heading hierarchy (h2, h3, h4)
- Uses `<section>` elements for logical content grouping
- Proper `<dl>`, `<dt>`, `<dd>` tags for definition lists
- AccordionItem uses Headless UI with built-in ARIA attributes
- Color-coded states include text labels (not color-only information)
- Keyboard navigation support through Headless UI Disclosure component

## Type Definitions

See `pipeSidecar.types.ts` for complete TypeScript type definitions.

## Storybook

The component includes three Storybook stories:
- **Add Note Pipe**: Demonstrates the component with AddNotePipe sidecar data
- **Update Ticket Pipe**: Shows UpdateTicketPipe configuration
- **With Actions**: Example with custom action buttons in the header

Run Storybook to view and interact with the component:
```bash
npm run storybook
```
