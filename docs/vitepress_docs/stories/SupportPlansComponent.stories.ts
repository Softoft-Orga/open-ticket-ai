import SupportPlans from '../.vitepress/components/SupportPlansComponent.vue'
import type {Meta, StoryObj} from '@storybook/vue3'
import {i18n} from './i18nSetup'

const meta: Meta<typeof SupportPlans> = {
    title: 'Components/SupportPlansComponent',
    component: SupportPlans,
}
export default meta

type Story = StoryObj<typeof meta>

export const Default: Story = {
    render: (args, {app}) => ({
        components: {SupportPlansComponent: SupportPlans},
        setup() {
            app.use(i18n)
            return {args}
        },
        template: '<SupportPlansComponent />'
    })
}
