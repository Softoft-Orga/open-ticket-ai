import PredictionCard from '../src/components/vue/predictionDemo/PredictionCard.vue'
import type {Meta, StoryObj} from '@storybook/vue3'

const meta: Meta<typeof PredictionCard> = {
    title: 'PredictionDemo/PredictionCard',
    component: PredictionCard,
    argTypes: {
        heading: {
            control: 'text',
            description: 'The heading text for the card'
        },
        confidence: {
            control: { type: 'range', min: 0, max: 1, step: 0.01 },
            description: 'Confidence level (0-1)'
        }
    },
    parameters: {
        docs: {
            description: {
                component: 'Card displaying prediction results with a confidence badge. Badge color changes based on confidence level.'
            }
        }
    }
}
export default meta

type Story = StoryObj<typeof meta>

export const HighConfidence: Story = {
    render: (args) => ({
        components: {PredictionCard},
        setup() {
            return {args}
        },
        template: `
            <div class="max-w-md">
                <PredictionCard v-bind="args">
                    <p>This ticket is about billing issues with payment processing.</p>
                </PredictionCard>
            </div>
        `
    }),
    args: {
        heading: 'Billing',
        confidence: 0.95
    }
}

export const MediumConfidence: Story = {
    render: (args) => ({
        components: {PredictionCard},
        setup() {
            return {args}
        },
        template: `
            <div class="max-w-md">
                <PredictionCard v-bind="args">
                    <p>The ticket might be related to technical support or product inquiries.</p>
                </PredictionCard>
            </div>
        `
    }),
    args: {
        heading: 'Technical Support',
        confidence: 0.65
    }
}

export const LowConfidence: Story = {
    render: (args) => ({
        components: {PredictionCard},
        setup() {
            return {args}
        },
        template: `
            <div class="max-w-md">
                <PredictionCard v-bind="args">
                    <p>Uncertain classification - may need manual review.</p>
                </PredictionCard>
            </div>
        `
    }),
    args: {
        heading: 'General Inquiry',
        confidence: 0.42
    }
}

export const VeryLowConfidence: Story = {
    render: (args) => ({
        components: {PredictionCard},
        setup() {
            return {args}
        },
        template: `
            <div class="max-w-md">
                <PredictionCard v-bind="args">
                    <p>Very uncertain - manual classification recommended.</p>
                </PredictionCard>
            </div>
        `
    }),
    args: {
        heading: 'Other',
        confidence: 0.15
    }
}

export const Interactive: Story = {
    render: (args) => ({
        components: {PredictionCard},
        setup() {
            return {args}
        },
        template: `
            <div class="space-y-4 max-w-md">
                <p class="text-sm text-text-dim">Adjust the confidence slider in Controls to see badge color changes</p>
                <PredictionCard v-bind="args">
                    <p>Sample prediction content</p>
                </PredictionCard>
            </div>
        `
    }),
    args: {
        heading: 'Sample Category',
        confidence: 0.75
    }
}
