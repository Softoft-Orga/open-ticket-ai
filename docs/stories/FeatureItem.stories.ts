import type { Meta, StoryObj } from '@storybook/vue3'
import FeatureItem from '../src/components/vue/product/FeatureItem.vue'
import { VARIANTS } from '../src/components/vue/core/design-system/tokens'

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
    variant: {
      control: 'select',
      options: VARIANTS,
      description: 'Visual variant from design system tokens (primary, secondary, outline, ghost)',
    },
  },
  args: {
    variant: 'secondary',
  },
}

export default meta
type Story = StoryObj<typeof FeatureItem>

export const ReasoningChain: Story = {
  args: {
    icon: '🧠',
    title: 'Reasoning Chain',
    desc: 'LLM provides the logic behind each tag, allowing for human audit and trust-building across teams.',
    variant: 'secondary',
  },
}

export const CustomAdapters: Story = {
  args: {
    icon: '🎛️',
    title: 'Custom Adapters',
    desc: 'Inject your specific industry jargon via LoRA adapters without re-training the entire model from scratch.',
    variant: 'secondary',
  },
}

export const BatchProcessing: Story = {
  args: {
    icon: '📦',
    title: 'Batch Processing',
    desc: 'Optimized for massive ticket migrations (backlog tagging) at 100+ tps with zero external dependency on cloud.',
    variant: 'secondary',
  },
}

export const HardwareAirGap: Story = {
  args: {
    icon: '🛡️',
    title: 'Hardware Air-Gap',
    desc: 'Validated for high-security environments with zero external dependency telemetry, runs fully offline.',
    variant: 'secondary',
  },
}

// Variant demonstrations
export const VariantPrimary: Story = {
  args: {
    icon: '⭐',
    title: 'Primary Variant',
    desc: 'Features a primary color background with matching border for emphasis.',
    variant: 'primary',
  },
}

export const VariantSecondary: Story = {
  args: {
    icon: '📋',
    title: 'Secondary Variant',
    desc: 'Default subtle dark background with standard border styling.',
    variant: 'secondary',
  },
}

export const VariantOutline: Story = {
  args: {
    icon: '🔲',
    title: 'Outline Variant',
    desc: 'Transparent background with visible border for a minimal look.',
    variant: 'outline',
  },
}

export const VariantGhost: Story = {
  args: {
    icon: '👻',
    title: 'Ghost Variant',
    desc: 'Completely transparent with no border for seamless integration.',
    variant: 'ghost',
  },
}

// Showcase all variants
export const AllVariants: Story = {
  render: () => ({
    components: { FeatureItem },
    template: `
      <div class="grid grid-cols-1 md:grid-cols-2 gap-6 p-6 bg-background-dark">
        <FeatureItem 
          icon="⭐" 
          title="Primary Variant" 
          desc="Features a primary color background with matching border for emphasis."
          variant="primary"
        />
        <FeatureItem 
          icon="📋" 
          title="Secondary Variant" 
          desc="Default subtle dark background with standard border styling."
          variant="secondary"
        />
        <FeatureItem 
          icon="🔲" 
          title="Outline Variant" 
          desc="Transparent background with visible border for a minimal look."
          variant="outline"
        />
        <FeatureItem 
          icon="👻" 
          title="Ghost Variant" 
          desc="Completely transparent with no border for seamless integration."
          variant="ghost"
        />
      </div>
    `
  }),
}
