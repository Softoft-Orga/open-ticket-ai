import TableOfContents from '../src/components/vue/core/TableOfContents.vue'
import type { Meta, StoryObj } from '@storybook/vue3'

const meta: Meta<typeof TableOfContents> = {
  title: 'Docs/TableOfContents',
  component: TableOfContents,
  tags: ['autodocs'],
  parameters: {
    docs: {
      description: {
        component: 'Table of contents component for documentation pages with automatic scroll tracking, smooth navigation, nested headings support, and optional collapsing.'
      }
    }
  },
  argTypes: {
    showLine: {
      control: 'boolean',
      description: 'Show or hide the vertical accent line',
      defaultValue: true
    },
    collapsible: {
      control: 'boolean',
      description: 'Enable collapsible nested sections',
      defaultValue: false
    }
  }
}
export default meta

type Story = StoryObj<typeof meta>

const sampleHeadings = [
  { id: 'introduction', text: 'Introduction', level: 2 },
  { id: 'getting-started', text: 'Getting Started', level: 2 },
  { id: 'installation', text: 'Installation', level: 3 },
  { id: 'configuration', text: 'Configuration', level: 3 },
  { id: 'usage', text: 'Usage', level: 2 },
  { id: 'basic-usage', text: 'Basic Usage', level: 3 },
  { id: 'advanced-usage', text: 'Advanced Usage', level: 3 },
  { id: 'api-reference', text: 'API Reference', level: 2 },
]

const deeplyNestedHeadings = [
  { id: 'introduction', text: 'Introduction', level: 2 },
  { id: 'core-concepts', text: 'Core Concepts', level: 2 },
  { id: 'tickets', text: 'Tickets', level: 3 },
  { id: 'ticket-types', text: 'Ticket Types', level: 4 },
  { id: 'bug-tickets', text: 'Bug Tickets', level: 5 },
  { id: 'feature-tickets', text: 'Feature Tickets', level: 5 },
  { id: 'ticket-status', text: 'Ticket Status', level: 4 },
  { id: 'open-status', text: 'Open Status', level: 5 },
  { id: 'closed-status', text: 'Closed Status', level: 5 },
  { id: 'automation', text: 'Automation', level: 3 },
  { id: 'rules', text: 'Rules', level: 4 },
  { id: 'simple-rules', text: 'Simple Rules', level: 5 },
  { id: 'complex-rules', text: 'Complex Rules', level: 5 },
  { id: 'workflows', text: 'Workflows', level: 4 },
  { id: 'workflow-triggers', text: 'Workflow Triggers', level: 5 },
  { id: 'api-reference', text: 'API Reference', level: 2 },
  { id: 'endpoints', text: 'Endpoints', level: 3 },
  { id: 'authentication', text: 'Authentication', level: 4 },
]

export const Default: Story = {
  render: (args) => ({
    components: { TableOfContents },
    setup() {
      return { args }
    },
    template: '<TableOfContents v-bind="args" />'
  }),
  args: {
    headings: sampleHeadings,
    showLine: true,
    collapsible: false
  }
}

export const WithoutLine: Story = {
  render: (args) => ({
    components: { TableOfContents },
    setup() {
      return { args }
    },
    template: '<TableOfContents v-bind="args" />'
  }),
  args: {
    headings: sampleHeadings,
    showLine: false,
    collapsible: false
  },
  parameters: {
    docs: {
      description: {
        story: 'Table of contents without the vertical accent line for a cleaner look.'
      }
    }
  }
}

export const Collapsible: Story = {
  render: (args) => ({
    components: { TableOfContents },
    setup() {
      return { args }
    },
    template: '<TableOfContents v-bind="args" />'
  }),
  args: {
    headings: sampleHeadings,
    showLine: true,
    collapsible: true
  },
  parameters: {
    docs: {
      description: {
        story: 'Table of contents with collapsible nested sections. Click the arrow to expand/collapse sections.'
      }
    }
  }
}

export const CollapsibleWithoutLine: Story = {
  render: (args) => ({
    components: { TableOfContents },
    setup() {
      return { args }
    },
    template: '<TableOfContents v-bind="args" />'
  }),
  args: {
    headings: sampleHeadings,
    showLine: false,
    collapsible: true
  },
  parameters: {
    docs: {
      description: {
        story: 'Collapsible table of contents without the vertical line.'
      }
    }
  }
}

export const FewHeadings: Story = {
  render: (args) => ({
    components: { TableOfContents },
    setup() {
      return { args }
    },
    template: '<TableOfContents v-bind="args" />'
  }),
  args: {
    headings: [
      { id: 'overview', text: 'Overview', level: 2 },
      { id: 'features', text: 'Features', level: 2 },
      { id: 'examples', text: 'Examples', level: 2 },
    ],
    showLine: true,
    collapsible: false
  },
  parameters: {
    docs: {
      description: {
        story: 'Simple table of contents with just a few top-level headings.'
      }
    }
  }
}

export const DeepNesting: Story = {
  render: (args) => ({
    components: { TableOfContents },
    setup() {
      return { args }
    },
    template: '<TableOfContents v-bind="args" />'
  }),
  args: {
    headings: deeplyNestedHeadings,
    showLine: true,
    collapsible: false
  },
  parameters: {
    docs: {
      description: {
        story: 'Table of contents with deeply nested headings (up to level 5) showing the tree structure.'
      }
    }
  }
}

export const DeepNestingCollapsible: Story = {
  render: (args) => ({
    components: { TableOfContents },
    setup() {
      return { args }
    },
    template: '<TableOfContents v-bind="args" />'
  }),
  args: {
    headings: deeplyNestedHeadings,
    showLine: true,
    collapsible: true
  },
  parameters: {
    docs: {
      description: {
        story: 'Deeply nested table of contents with collapsible sections - ideal for large documentation pages.'
      }
    }
  }
}
