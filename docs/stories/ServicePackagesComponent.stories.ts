import ServicePackages from '../.vitepress/components/ServicePackagesComponent.vue'
import type {Meta, StoryObj} from '@storybook/vue3'
import {i18n} from './i18nSetup'

const meta: Meta<typeof ServicePackages> = {
    title: 'Components/ServicePackagesComponent',
    component: ServicePackages,
}
export default meta

type Story = StoryObj<typeof meta>

export const Default: Story = {
    render: (args, {app}) => ({
        components: {ServicePackagesComponent: ServicePackages},
        setup() {
            app.use(i18n)
            return {args}
        },
        template: '<ServicePackagesComponent />'
    })
}
