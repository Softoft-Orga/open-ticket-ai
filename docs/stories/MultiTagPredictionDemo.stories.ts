import MultiTagPredictionDemo from '../src/components/vue/multiTagDemo/MultiTagPredictionDemo.vue'
import type {Meta, StoryObj} from '@storybook/vue3'

const meta: Meta<typeof MultiTagPredictionDemo> = {
    title: 'MultiTagDemo/MultiTagPredictionDemo',
    component: MultiTagPredictionDemo,
    parameters: {
        docs: {
            description: {
                component: 'Interactive demo showing multi-tag hierarchical classification predictions. Includes multiple example tickets with tag tree and mindmap visualizations.'
            }
        },
        layout: 'fullscreen'
    }
}
export default meta

type Story = StoryObj<typeof meta>

export const Default: Story = {
    render: (args) => ({
        components: {MultiTagPredictionDemo},
        setup() {
            return {args}
        },
        template: '<div class="p-8"><MultiTagPredictionDemo v-bind="args" /></div>'
    })
}

export const DarkMode: Story = {
    render: (args) => ({
        components: {MultiTagPredictionDemo},
        setup() {
            return {args}
        },
        template: '<div class="bg-slate-950 p-8 min-h-screen"><MultiTagPredictionDemo v-bind="args" /></div>'
    }),
    parameters: {
        backgrounds: { default: 'dark' }
    }
}
