import ResultTable from '../src/components/vue/predictionDemo/ResultTable.vue'
import type {Meta, StoryObj} from '@storybook/vue3'
import {i18n} from './i18nSetup'

const meta: Meta<typeof ResultTable> = {
    title: 'PredictionDemo/ResultTable',
    component: ResultTable,
    argTypes: {
        queueResult: {
            control: 'object',
            description: 'Queue prediction results array'
        },
        prioResult: {
            control: 'object',
            description: 'Priority prediction results array'
        }
    },
    parameters: {
        docs: {
            description: {
                component: 'Displays prediction results in a two-column grid showing queue and priority classifications with confidence scores.'
            }
        }
    }
}
export default meta

type Story = StoryObj<typeof meta>

const highConfidenceResults = {
    queueResult: [
        { label: 'Technical Support/Software', score: 0.94 }
    ],
    prioResult: [
        { label: 'High', score: 0.88 }
    ]
}

const mediumConfidenceResults = {
    queueResult: [
        { label: 'Billing/Payment Issues', score: 0.72 }
    ],
    prioResult: [
        { label: 'Medium', score: 0.65 }
    ]
}

const lowConfidenceResults = {
    queueResult: [
        { label: 'General Inquiry/Other', score: 0.45 }
    ],
    prioResult: [
        { label: 'Low', score: 0.42 }
    ]
}

export const HighConfidence: Story = {
    render: (args, {app}) => ({
        components: {ResultTable},
        setup() {
            app.use(i18n)
            return {args}
        },
        template: '<div class="max-w-4xl"><ResultTable v-bind="args" /></div>'
    }),
    args: highConfidenceResults
}

export const MediumConfidence: Story = {
    render: (args, {app}) => ({
        components: {ResultTable},
        setup() {
            app.use(i18n)
            return {args}
        },
        template: '<div class="max-w-4xl"><ResultTable v-bind="args" /></div>'
    }),
    args: mediumConfidenceResults
}

export const LowConfidence: Story = {
    render: (args, {app}) => ({
        components: {ResultTable},
        setup() {
            app.use(i18n)
            return {args}
        },
        template: '<div class="max-w-4xl"><ResultTable v-bind="args" /></div>'
    }),
    args: lowConfidenceResults
}

export const DarkMode: Story = {
    render: (args, {app}) => ({
        components: {ResultTable},
        setup() {
            app.use(i18n)
            return {args}
        },
        template: '<div class="max-w-4xl bg-slate-950 p-8 rounded"><ResultTable v-bind="args" /></div>'
    }),
    args: highConfidenceResults,
    parameters: {
        backgrounds: { default: 'dark' }
    }
}
