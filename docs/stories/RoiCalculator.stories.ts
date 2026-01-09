import type { Meta, StoryObj } from '@storybook/vue3'
import RoiCalculator from '../src/components/vue/product/RoiCalculator.vue'

const meta = {
  title: 'Product/RoiCalculator',
  component: RoiCalculator,
  tags: ['autodocs'],
  parameters: {
    layout: 'fullscreen',
    docs: {
      description: {
        component: 'Interactive ROI and pricing calculator with scenario presets and customizable inputs. Features Chart.js visualizations for TCO projection and cost breakdown.'
      }
    }
  }
} satisfies Meta<typeof RoiCalculator>

export default meta
type Story = StoryObj<typeof meta>

export const Default: Story = {
  args: {},
  parameters: {
    docs: {
      description: {
        story: 'Default calculator view with realistic scenario preset.'
      }
    }
  }
}

export const DarkBackground: Story = {
  args: {},
  parameters: {
    backgrounds: {
      default: 'dark'
    },
    docs: {
      description: {
        story: 'Calculator displayed on dark background to match site theme.'
      }
    }
  }
}
