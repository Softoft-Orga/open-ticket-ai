import Badge from '../.vitepress/components/core/basic/Badge.vue'
import type { Meta, StoryObj } from '@storybook/vue3'

const meta: Meta<typeof Badge> = {
  title: 'Core/Badge',
  component: Badge,
  argTypes: {
    type: { control: { type: 'select' }, options: ['primary','secondary','success','warning','danger'] }
  },
}
export default meta

type Story = StoryObj<typeof meta>

export const Primary: Story = {
  render: (args) => ({
    components: { Badge },
    setup() { return { args } },
    template: '<Badge v-bind="args">Primary</Badge>'
  }),
  args: { type: 'primary' }
}

export const Success: Story = {
  render: (args) => ({
    components: { Badge },
    setup() { return { args } },
    template: '<Badge v-bind="args">Success</Badge>'
  }),
  args: { type: 'success' }
}
