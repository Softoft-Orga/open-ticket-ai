import TableOfContents from '../src/components/vue/docs/TableOfContents.vue'
import type { Meta, StoryObj } from '@storybook/vue3'

const meta: Meta<typeof TableOfContents> = {
  title: 'Docs/TableOfContents',
  component: TableOfContents,
  tags: ['autodocs'],
  parameters: {
    docs: {
      description: {
        component: 'Table of contents component for documentation pages with automatic scroll tracking and smooth navigation.'
      }
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

export const Default: Story = {
  render: (args) => ({
    components: { TableOfContents },
    setup() {
      return { args }
    },
    template: '<TableOfContents v-bind="args" />'
  }),
  args: {
    headings: sampleHeadings
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
    ]
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
    headings: [
      { id: 'introduction', text: 'Introduction', level: 2 },
      { id: 'core-concepts', text: 'Core Concepts', level: 2 },
      { id: 'tickets', text: 'Tickets', level: 3 },
      { id: 'ticket-types', text: 'Ticket Types', level: 4 },
      { id: 'ticket-status', text: 'Ticket Status', level: 4 },
      { id: 'automation', text: 'Automation', level: 3 },
      { id: 'rules', text: 'Rules', level: 4 },
      { id: 'workflows', text: 'Workflows', level: 4 },
    ]
  }
}
