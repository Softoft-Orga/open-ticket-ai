import Tabs from '../src/components/vue/core/basic/Tabs.vue'
import {ref} from 'vue'
import type {Meta, StoryObj} from '@storybook/vue3'
import {ref} from 'vue'

const meta: Meta<typeof Tabs> = {
    title: 'Core/Tabs',
    component: Tabs,
}
export default meta

type Story = StoryObj<typeof meta>

export const Default: Story = {
    render: (args) => ({
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
    }),
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
      <p class="mb-4 text-sm text-gray-400">Active tab index: {{ activeTab }}</p>
      <Tabs v-bind="args" v-model="activeTab">
        <template #tab-0>Content for tab A</template>
        <template #tab-1>Content for tab B (initially active)</template>
        <template #tab-2>Content for tab C</template>
      </Tabs>
    </div>`
    }),
    args: {tabs: ['Tab A', 'Tab B', 'Tab C']}
}
