import FooterComponent from '../src/components/vue/core/navigation/FooterComponent.vue'
import type {Meta, StoryObj} from '@storybook/vue3'

const meta: Meta<typeof FooterComponent> = {
    title: 'Navigation/FooterComponent',
    component: FooterComponent,
    parameters: {
        layout: 'fullscreen',
        backgrounds: {
            default: 'dark',
            values: [
                { name: 'dark', value: '#0f0814' },
            ],
        },
    },
}
export default meta

type Story = StoryObj<typeof meta>

export const Default: Story = {
    render: (args) => ({
        components: {FooterComponent},
        setup() {
            return {args}
        },
        template: '<FooterComponent v-bind="args" />'
    })
}
