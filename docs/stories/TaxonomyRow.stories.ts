import type { Meta, StoryObj } from '@storybook/vue3'
import TaxonomyRow from '../src/components/vue/product/TaxonomyRow.vue'

const meta: Meta<typeof TaxonomyRow> = {
  title: 'Product/TaxonomyRow',
  component: TaxonomyRow,
  tags: ['autodocs'],
  argTypes: {
    level: {
      control: { type: 'number', min: 1, max: 4 },
      description: 'Taxonomy hierarchy level (1-4)',
    },
    label: {
      control: 'text',
      description: 'Taxonomy path label',
    },
    tags: {
      control: 'object',
      description: 'Array of tag strings',
    },
    active: {
      control: 'boolean',
      description: 'Whether this row is active/highlighted',
    },
  },
}

export default meta
type Story = StoryObj<typeof TaxonomyRow>

export const Level1Active: Story = {
  args: {
    level: 1,
    label: 'intent/',
    tags: ['service_request', 'incident', 'change'],
    active: true,
  },
}

export const Level2: Story = {
  args: {
    level: 2,
    label: 'intent/incident/',
    tags: ['security', 'downtime', 'performance'],
    active: false,
  },
}

export const Level3: Story = {
  args: {
    level: 3,
    label: 'intent/incident/security/',
    tags: ['breach', 'phishing', 'malware'],
    active: false,
  },
}

export const Level4: Story = {
  args: {
    level: 4,
    label: 'intent/incident/security/phishing/',
    tags: ['email', 'sms', 'voice'],
    active: false,
  },
}
