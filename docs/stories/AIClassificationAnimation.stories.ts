import AIClassificationAnimation from '../src/components/vue/animation/AIClassificationAnimation.vue'
import type {Meta, StoryObj} from '@storybook/vue3'
import {i18n} from './i18nSetup'

const meta: Meta<typeof AIClassificationAnimation> = {
    title: 'Animation/AIClassificationAnimation',
    component: AIClassificationAnimation,
    parameters: {
        docs: {
            description: {
                component: 'Interactive SVG animation showing ticket classification flow. Click to start the animation and see tickets being routed to different categories.'
            }
        }
    }
}
export default meta

type Story = StoryObj<typeof meta>

export const Default: Story = {
    render: (args, {app}) => ({
        components: {AIClassificationAnimation},
        setup() {
            app.use(i18n)
            return {args}
        },
        template: '<div class="w-full max-w-4xl mx-auto"><AIClassificationAnimation v-bind="args" /></div>'
    })
}

export const DarkBackground: Story = {
    render: (args, {app}) => ({
        components: {AIClassificationAnimation},
        setup() {
            app.use(i18n)
            return {args}
        },
        template: '<div class="w-full max-w-4xl mx-auto bg-slate-950 p-8 rounded"><AIClassificationAnimation v-bind="args" /></div>'
    }),
    parameters: {
        backgrounds: { default: 'dark' }
    }
}
