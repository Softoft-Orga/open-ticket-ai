import Tabs from '../src/components/vue/core/basic/Tabs.vue'
import {ref} from 'vue'
import type {Meta, StoryObj} from '@storybook/vue3'

const meta: Meta<typeof Tabs> = {
    title: 'Core/Tabs',
    component: Tabs,
}
export default meta

type Story = StoryObj<typeof meta>

const Template = (args: any) => ({
    components: {Tabs},
    setup() {
        return {args}
    },
    template: `
    <Tabs v-bind="args">
      <template #tab-0>Content for first tab</template>
      <template #tab-1>Content for second tab</template>
      <template #tab-2>Content for third tab</template>
    </Tabs>`
})

export const Default: Story = {
    render: Template,
    args: {tabs: ['First', 'Second', 'Third']}
}

export const WithVModel: Story = {
    render: (args) => ({
        components: {Tabs},
        setup() {
            const activeTab = ref(1)
            return {args, activeTab}
        },
        template: `
      <div>
        <p class="mb-4 text-sm">Current active tab: {{ activeTab }}</p>
        <Tabs v-bind="args" v-model="activeTab">
          <template #tab-0>First tab content</template>
          <template #tab-1>Second tab content (initially active)</template>
          <template #tab-2>Third tab content</template>
        </Tabs>
      </div>
    `
    }),
    args: {tabs: ['First', 'Second', 'Third']}
}

export const KeyboardNavigation: Story = {
    render: Template,
    args: {tabs: ['Home', 'About', 'Contact', 'Services']},
    parameters: {
        docs: {
            description: {
                story: 'Use Arrow Left/Right keys to navigate between tabs. Home/End keys jump to first/last tab.'
            }
        }
    }
}
