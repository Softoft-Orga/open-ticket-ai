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
        component: `Interactive ROI and pricing calculator with scenario presets and customizable inputs. 

**Features:**
- Three preset scenarios (Conservative, Realistic, Critical) with visual selection indicators
- Enhanced hover effects on preset cards and stat cards with scale and glow
- Smooth fade/scale transitions using classes inspired by the design system presets
- Chart.js visualizations for TCO projection and cost breakdown
- Shared components (Card, Badge) with Tailwind tokens only
- Real-time calculations with Chart updates
- Accessibility support with motion-reduce

**Visual Enhancements:**
- Selected preset: Stronger border (2px), gradient background, purple glow shadow, ring effect, check icon
- Hover states: Scale effects, border color transitions, shadow glows (purple/cyan)
- Entry animations: Fade and scale for stat cards and savings panel

**Interactions:**
- Click preset scenarios to apply predefined values
- Selected preset displays with enhanced visual feedback (gradient, glow, ring, check)
- Hover over cards for smooth scale and glow effects
- Modify inputs to see live TCO updates`
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
        story: 'Default calculator view with realistic scenario preset. Demonstrates enhanced visual feedback for selected preset with stronger border, gradient, glow, and check icon. Hover interactions show scale and shadow effects.'
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
        story: 'Calculator displayed on dark background to match site theme. Showcases the cyber-glow aesthetic with purple/cyan highlights and enhanced transitions.'
      }
    }
  }
}
