# PipeSidecar Component

## Overview
The PipeSidecar component displays comprehensive information about pipeline pipe configurations from sidecar YAML specifications. The component is now refactored into smaller, focused sub-components for better maintainability.

## Architecture

The component has been refactored from a single 250-line file into a modular structure:

- **PipeSidecar.vue** (56 lines) - Main component that composes all sections
- **sections/MetadataSection.vue** - Displays class and inheritance information
- **sections/InputsSection.vue** - Shows input parameters and configuration
- **sections/DefaultsSection.vue** - Displays default values
- **sections/OutputSection.vue** - Shows output states and examples
- **sections/ErrorsSection.vue** - Displays error categories (fail/break/continue)
- **sections/EngineSupportSection.vue** - Shows engine capability flags
- **sections/ExamplesSection.vue** - Displays usage examples

## Composable: useSidecars

A new composable `useSidecars` provides centralized access to sidecar data:

```typescript
import { useSidecars } from '@/.vitepress/composables/useSidecars'

const { sidecars, isLoading, error, getSidecar, filterByType, filterByCategory } = useSidecars()

// Get a specific sidecar
const addNotePipe = getSidecar('pipe', 'add_note_pipe')

// Filter by type (pipe, service, trigger)
const allPipes = filterByType('pipe')

// Filter by category
const ticketSystemPipes = filterByCategory('ticket-system')
```

### Composable API

| Method | Description |
|--------|-------------|
| `getSidecar(type, name)` | Get a specific sidecar by type and name |
| `filterByType(type)` | Get all sidecars of a specific type ('pipe', 'service', 'trigger') |
| `filterByCategory(category)` | Get all sidecars in a specific category |
| `getAllSidecars()` | Get all available sidecars |

### Reactive State

| Property | Type | Description |
|----------|------|-------------|
| `sidecars` | `Map<string, SidecarEntry>` | Map of all loaded sidecars |
| `isLoading` | `boolean` | Loading state |
| `error` | `Error \| null` | Error state if loading fails |

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

### Using the Composable
```vue
<script setup>
import { useSidecars } from '@/.vitepress/composables/useSidecars'
import PipeSidecar from '@/.vitepress/components/pipe/PipeSidecar.vue'

const { getSidecar, filterByType, isLoading } = useSidecars()

const addNotePipe = getSidecar('pipe', 'add_note_pipe')
const allPipes = filterByType('pipe')
</script>

<template>
  <div v-if="isLoading">Loading...</div>
  <PipeSidecar v-else-if="addNotePipe" :sidecar="addNotePipe.data" />
</template>
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

- **Modular Structure**: Component split into focused sub-components (56 lines vs 250 lines)
- **Centralized Data**: `useSidecars` composable for loading and filtering sidecars
- **Type Support**: Works with Pipes, Services, and Triggers
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
