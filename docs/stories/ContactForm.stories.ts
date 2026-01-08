import ContactForm from '../src/components/vue/forms/ContactForm.vue'
import type {Meta, StoryObj} from '@storybook/vue3'
import {i18n} from './i18nSetup'

const meta: Meta<typeof ContactForm> = {
    title: 'Forms/ContactForm',
    component: ContactForm,
    parameters: {
        docs: {
            description: {
                component: 'Contact form with email and message fields, integrated with Formspree for submissions.'
            }
        }
    }
}
export default meta

type Story = StoryObj<typeof meta>

export const Default: Story = {
    render: (args, {app}) => ({
        components: {ContactForm},
        setup() {
            app.use(i18n)
            return {args}
        },
        template: '<div class="max-w-2xl"><ContactForm v-bind="args" /></div>'
    })
}

export const DarkMode: Story = {
    render: (args, {app}) => ({
        components: {ContactForm},
        setup() {
            app.use(i18n)
            return {args}
        },
        template: '<div class="max-w-2xl bg-gray-950 p-8 rounded"><ContactForm v-bind="args" /></div>'
    }),
    parameters: {
        backgrounds: { default: 'dark' }
    }
}
