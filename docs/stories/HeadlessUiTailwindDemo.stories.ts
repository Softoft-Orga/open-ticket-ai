import type { Meta, StoryObj } from '@storybook/vue3'
import HeadlessUiTailwindDemo from '../src/components/vue/core/HeadlessUiTailwindDemo.vue'

const meta = {
  title: 'Core/Headless UI Tailwind Demo',
  component: HeadlessUiTailwindDemo,
  parameters: {
    layout: 'centered',
  },
} satisfies Meta<typeof HeadlessUiTailwindDemo>

export default meta

export const Default: StoryObj<typeof meta> = {}

