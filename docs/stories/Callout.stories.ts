import Callout from '../src/components/vue/core/basic/Callout.vue'
import type {Meta, StoryObj} from '@storybook/vue3'

const meta: Meta<typeof Callout> = {
    title: 'Core/Callout',
    component: Callout,
    argTypes: {
        type: {
            control: {type: 'select'},
            options: ['info', 'success', 'warning', 'danger'],
            description: 'Callout variant type'
        },
        variant: {
            control: {type: 'select'},
            options: ['left-border', 'bordered', 'filled'],
            description: 'Border style variant'
        }
    },
    parameters: {
        docs: {
            description: {
                component: 'Callout component for displaying important messages with different severity levels. Includes automatic icons based on type and customizable border styles.'
            }
        }
    }
}
export default meta

type Story = StoryObj<typeof meta>

export const Info: Story = {
    render: (args) => ({
        components: {Callout},
        setup() {
            return {args}
        },
        template: '<Callout v-bind="args">This is an informational message to provide helpful context or additional details.</Callout>'
    }),
    args: {type: 'info'}
}

export const Success: Story = {
    render: (args) => ({
        components: {Callout},
        setup() {
            return {args}
        },
        template: '<Callout v-bind="args">Operation completed successfully! Your changes have been saved.</Callout>'
    }),
    args: {type: 'success'}
}

export const Warning: Story = {
    render: (args) => ({
        components: {Callout},
        setup() {
            return {args}
        },
        template: '<Callout v-bind="args">Please review your settings carefully before proceeding. This action may have side effects.</Callout>'
    }),
    args: {type: 'warning'}
}

export const Danger: Story = {
    render: (args) => ({
        components: {Callout},
        setup() {
            return {args}
        },
        template: '<Callout v-bind="args">Critical error: Unable to process your request. Please contact support if the problem persists.</Callout>'
    }),
    args: {type: 'danger'}
}

export const AllVariants: Story = {
    render: () => ({
        components: {Callout},
        template: `
            <div class="space-y-4 max-w-2xl">
                <Callout type="info">Info: This is helpful information for the user.</Callout>
                <Callout type="success">Success: The operation was completed successfully.</Callout>
                <Callout type="warning">Warning: Please review before continuing.</Callout>
                <Callout type="danger">Danger: A critical error has occurred.</Callout>
            </div>
        `
    })
}

export const BorderVariants: Story = {
    render: () => ({
        components: {Callout},
        template: `
            <div class="space-y-4 max-w-2xl">
                <h3 class="text-lg font-semibold mb-4 text-white">Left Border (Default)</h3>
                <Callout type="info" variant="left-border">Info with left border accent.</Callout>
                <Callout type="success" variant="left-border">Success with left border accent.</Callout>
                
                <h3 class="text-lg font-semibold mb-4 mt-8 text-white">Full Border</h3>
                <Callout type="warning" variant="bordered">Warning with full border.</Callout>
                <Callout type="danger" variant="bordered">Danger with full border.</Callout>
                
                <h3 class="text-lg font-semibold mb-4 mt-8 text-white">Filled (No Border)</h3>
                <Callout type="info" variant="filled">Info without border.</Callout>
                <Callout type="success" variant="filled">Success without border.</Callout>
            </div>
        `
    })
}

export const WithRichContent: Story = {
    render: (args) => ({
        components: {Callout},
        setup() {
            return {args}
        },
        template: `
            <Callout v-bind="args">
                <h4 class="font-bold mb-2">Important Update</h4>
                <p class="mb-2">We've released a new version of the AI classifier with improved accuracy:</p>
                <ul class="list-disc list-inside space-y-1">
                    <li>95% accuracy on standard tickets</li>
                    <li>Support for 50+ languages</li>
                    <li>Faster response times</li>
                </ul>
            </Callout>
        `
    }),
    args: {type: 'info'}
}
