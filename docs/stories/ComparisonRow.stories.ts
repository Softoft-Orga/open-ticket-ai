import type { Meta, StoryObj } from '@storybook/vue3'
import ComparisonRow from '../src/components/vue/product/ComparisonRow.vue'

const meta: Meta<typeof ComparisonRow> = {
  title: 'Product/ComparisonRow',
  component: ComparisonRow,
  tags: ['autodocs'],
  argTypes: {
    label: {
      control: 'text',
      description: 'Row label/metric name',
    },
    v1: {
      control: 'text',
      description: 'Value for version 1 (Lite Pro)',
    },
    v2: {
      control: 'text',
      description: 'Value for version 2 (Full Pro)',
    },
  },
}

export default meta
type Story = StoryObj<typeof ComparisonRow>

export const ModelSize: Story = {
  args: {
    label: 'Model Size',
    v1: '4B Params',
    v2: '8B Params',
  },
}

export const Tags: Story = {
  args: {
    label: 'Tags',
    v1: '150+',
    v2: '250+',
  },
}

export const Accuracy: Story = {
  args: {
    label: 'Accuracy',
    v1: '~90%',
    v2: '~92.4%',
  },
}

export const Reasoning: Story = {
  args: {
    label: 'Reasoning',
    v1: '—',
    v2: '✓',
  },
}

export const LoRASupport: Story = {
  args: {
    label: 'LoRA Support',
    v1: '—',
    v2: '✓',
  },
}
