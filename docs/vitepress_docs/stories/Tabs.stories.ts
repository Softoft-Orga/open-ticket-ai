import Tabs from '../.vitepress/components/core/basic/Tabs.vue'
import type { Meta, StoryObj } from '@storybook/vue3'

const meta: Meta<typeof Tabs> = {
  title: 'Core/Tabs',
  component: Tabs,
}
export default meta

type Story = StoryObj<typeof meta>

const Template = (args:any) => ({
  components: { Tabs },
  setup() { return { args } },
  template: `
    <Tabs v-bind="args">
      <template #tab-0>Content for first tab</template>
      <template #tab-1>Content for second tab</template>
    </Tabs>`
})

export const Default: Story = {
  render: Template,
  args: { tabs: ['First', 'Second'] }
}
