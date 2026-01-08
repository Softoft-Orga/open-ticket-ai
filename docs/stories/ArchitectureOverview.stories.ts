import ArchitectureOverview from '../src/components/vue/ArchitectureOverview.vue'
import type {Meta, StoryObj} from '@storybook/vue3'

const meta: Meta<typeof ArchitectureOverview> = {
    title: 'Components/ArchitectureOverview',
    component: ArchitectureOverview,
    parameters: {
        docs: {
            description: {
                component: 'Visual architecture diagram component showing system design and component relationships.'
            }
        },
        layout: 'fullscreen'
    }
}
export default meta

type Story = StoryObj<typeof meta>

export const Default: Story = {
    render: (args) => ({
        components: {ArchitectureOverview},
        setup() {
            return {args}
        },
        template: '<div class="p-8"><ArchitectureOverview v-bind="args" /></div>'
    })
}

export const DarkMode: Story = {
    render: (args) => ({
        components: {ArchitectureOverview},
        setup() {
            return {args}
        },
        template: '<div class="bg-slate-950 p-8 min-h-screen"><ArchitectureOverview v-bind="args" /></div>'
    }),
    parameters: {
        backgrounds: { default: 'dark' }
    }
}
