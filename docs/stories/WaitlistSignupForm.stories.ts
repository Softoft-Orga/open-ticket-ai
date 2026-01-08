import WaitlistSignupForm from '../src/components/vue/forms/WaitlistSignupForm.vue'
import type {Meta, StoryObj} from '@storybook/vue3'
import {i18n} from './i18nSetup'

const meta: Meta<typeof WaitlistSignupForm> = {
    title: 'Forms/WaitlistSignupForm',
    component: WaitlistSignupForm,
    parameters: {
        docs: {
            description: {
                component: 'Waitlist signup form for Synthetic Data Generator, integrated with Formspree for email collection.'
            }
        }
    }
}
export default meta

type Story = StoryObj<typeof meta>

export const Default: Story = {
    render: (args, {app}) => ({
        components: {WaitlistSignupForm},
        setup() {
            app.use(i18n)
            return {args}
        },
        template: '<div class="max-w-2xl"><WaitlistSignupForm v-bind="args" /></div>'
    })
}

export const DarkMode: Story = {
    render: (args, {app}) => ({
        components: {WaitlistSignupForm},
        setup() {
            app.use(i18n)
            return {args}
        },
        template: '<div class="max-w-2xl bg-gray-950 p-8 rounded"><WaitlistSignupForm v-bind="args" /></div>'
    }),
    parameters: {
        backgrounds: { default: 'dark' }
    }
}
