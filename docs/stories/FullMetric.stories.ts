import type { Meta, StoryObj } from '@storybook/vue3'
import FullMetric from '../src/components/vue/product/FullMetric.vue'

const meta: Meta<typeof FullMetric> = {
  title: 'Product/FullMetric',
  component: FullMetric,
  tags: ['autodocs'],
  argTypes: {
    label: {
      control: 'text',
      description: 'Uppercase label for the metric',
    },
    value: {
      control: 'text',
      description: 'Main value display',
    },
    sub: {
      control: 'text',
      description: 'Subtitle or description',
    },
  },
}

export default meta
type Story = StoryObj<typeof FullMetric>

export const ModelArchitecture: Story = {
  args: {
    label: 'MODEL ARCHITECTURE',
    value: '8.0B Dense Transformer',
    sub: 'Fine-tuned for helpdesk semantics',
  },
}

export const VramOptimized: Story = {
  args: {
    label: 'VRAM OPTIMIZED',
    value: '16GB - 24GB',
    sub: 'Supports 4-bit and 8-bit quantization',
  },
}

export const TaxonomyDepth: Story = {
  args: {
    label: 'TAXONOMY DEPTH',
    value: '250+ Tags (4 Levels)',
    sub: 'Unmatched granularity for reporting',
  },
}

export const AccuracyBaseline: Story = {
  args: {
    label: 'ACCURACY BASELINE',
    value: '92.4%+',
    sub: 'State-of-the-art benchmarks',
  },
}
