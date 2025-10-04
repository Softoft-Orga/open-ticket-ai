import OTAIPredictionDemo from '../.vitepress/components/predictionDemo/OTAIPredictionDemo.vue'
import type {Meta, StoryObj} from '@storybook/vue3'
import {i18n} from './i18nSetup'

const meta: Meta<typeof OTAIPredictionDemo> = {
    title: 'Components/OTAIPredictionDemo',
    component: OTAIPredictionDemo,
}
export default meta

type Story = StoryObj<typeof meta>

export const Default: Story = {
    render: (args, {app}) => ({
        components: {OTAIPredictionDemo},
        setup() {
            app.use(i18n)
            return {args}
        },
        template: '<OTAIPredictionDemo />'
    })
}
