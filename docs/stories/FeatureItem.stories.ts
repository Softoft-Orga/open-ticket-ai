import type { Meta, StoryObj } from '@storybook/vue3'
import FeatureItem from '../src/components/vue/product/FeatureItem.vue'

const meta: Meta<typeof FeatureItem> = {
  title: 'Product/FeatureItem',
  component: FeatureItem,
  tags: ['autodocs'],
  argTypes: {
    icon: {
      control: 'text',
      description: 'Icon emoji or character',
    },
    title: {
      control: 'text',
      description: 'Feature title',
    },
    desc: {
      control: 'text',
      description: 'Feature description',
    },
  },
}

export default meta
type Story = StoryObj<typeof FeatureItem>

export const ReasoningChain: Story = {
  args: {
    icon: '🧠',
    title: 'Reasoning Chain',
    desc: 'LLM provides the logic behind each tag, allowing for human audit and trust-building across teams.',
  },
}

export const CustomAdapters: Story = {
  args: {
    icon: '🎛️',
    title: 'Custom Adapters',
    desc: 'Inject your specific industry jargon via LoRA adapters without re-training the entire model from scratch.',
  },
}

export const BatchProcessing: Story = {
  args: {
    icon: '📦',
    title: 'Batch Processing',
    desc: 'Optimized for massive ticket migrations (backlog tagging) at 100+ tps with zero external dependency on cloud.',
  },
}

export const HardwareAirGap: Story = {
  args: {
    icon: '🛡️',
    title: 'Hardware Air-Gap',
    desc: 'Validated for high-security environments with zero external dependency telemetry, runs fully offline.',
  },
}
