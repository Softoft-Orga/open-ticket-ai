import Callout from '../.vitepress/components/core/basic/Callout.vue'
import type { Meta, StoryObj } from '@storybook/vue3'

const meta: Meta<typeof Callout> = {
  title: 'Core/Callout',
  component: Callout,
  argTypes: {
    type: { control: { type: 'select' }, options: ['info','success','warning','danger'] }
  }
}
export default meta

type Story = StoryObj<typeof meta>

export const Info: Story = {
  render: (args) => ({
    components: { Callout },
    setup() { return { args } },
    template: '<Callout v-bind="args">Informational message</Callout>'
  }),
  args: { type: 'info' }
}

export const Danger: Story = {
  render: (args) => ({
    components: { Callout },
    setup() { return { args } },
    template: '<Callout v-bind="args">Danger message</Callout>'
  }),
  args: { type: 'danger' }
}
