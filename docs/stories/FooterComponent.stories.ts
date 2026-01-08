import FooterComponent from '../src/components/vue/navigation/FooterComponent.vue'
import type {Meta, StoryObj} from '@storybook/vue3'
import {i18n} from './i18nSetup'

const meta: Meta<typeof FooterComponent> = {
    title: 'Navigation/FooterComponent',
    component: FooterComponent,
    parameters: {
        layout: 'fullscreen',
    },
}
export default meta

type Story = StoryObj<typeof meta>

export const Default: Story = {
    render: (args, {app}) => ({
        components: {FooterComponent},
        setup() {
            app.use(i18n)
            return {args}
        },
        template: '<FooterComponent v-bind="args" />'
    })
}
