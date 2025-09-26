import Accordion from '../.vitepress/components/core/accordion/Accordion.vue'
import type { Meta, StoryObj } from '@storybook/vue3'

const meta: Meta<typeof Accordion> = {
  title: 'Core/Accordion',
  component: Accordion,
}
export default meta

type Story = StoryObj<typeof meta>

const sampleItems = [
  { title: 'Item 1', content: 'Content of item 1' },
  { title: 'Item 2', content: 'Content of item 2' },
]

export const Default: Story = {
  render: (args) => ({
    components: { Accordion },
    setup() { return { args } },
    template: '<Accordion v-bind="args" />',
  }),
  args: {
    items: sampleItems,
  },
}
