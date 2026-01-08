import Badge from '../src/components/vue/core/basic/Badge.vue'
import type {Meta, StoryObj} from '@storybook/vue3'

const meta: Meta<typeof Badge> = {
    title: 'Core/Badge',
    component: Badge,
    argTypes: {
        type: {control: {type: 'select'}, options: ['primary', 'secondary', 'success', 'warning', 'danger']},
        default: {
            control: 'text',
            description: 'Badge text content (slot)'
        }
    },
    parameters: {
        docs: {
            description: {
                component: 'Badge component for displaying status, labels, or categories with different color variants.'
            }
        }
    }
}
export default meta

type Story = StoryObj<typeof meta>

export const Primary: Story = {
    render: (args) => ({
        components: {Badge},
        setup() {
            return {args}
        },
        template: '<Badge v-bind="args">Primary</Badge>'
    }),
    args: {type: 'primary'}
}

export const Secondary: Story = {
    render: (args) => ({
        components: {Badge},
        setup() {
            return {args}
        },
        template: '<Badge v-bind="args">Secondary</Badge>'
    }),
    args: {type: 'secondary'}
}

export const Success: Story = {
    render: (args) => ({
        components: {Badge},
        setup() {
            return {args}
        },
        template: '<Badge v-bind="args">Success</Badge>'
    }),
    args: {type: 'success'}
}

export const Warning: Story = {
    render: (args) => ({
        components: {Badge},
        setup() {
            return {args}
        },
        template: '<Badge v-bind="args">Warning</Badge>'
    }),
    args: {type: 'warning'}
}

export const Danger: Story = {
    render: (args) => ({
        components: {Badge},
        setup() {
            return {args}
        },
        template: '<Badge v-bind="args">Danger</Badge>'
    }),
    args: {type: 'danger'}
}

export const AllVariants: Story = {
    render: () => ({
        components: {Badge},
        template: `
            <div class="flex flex-wrap gap-3 items-center p-4">
                <Badge type="primary">Primary</Badge>
                <Badge type="secondary">Secondary</Badge>
                <Badge type="success">Success</Badge>
                <Badge type="warning">Warning</Badge>
                <Badge type="danger">Danger</Badge>
            </div>
        `
    })
}

export const UseCases: Story = {
    render: () => ({
        components: {Badge},
        template: `
            <div class="space-y-4 p-4">
                <div class="flex items-center gap-2">
                    <span class="text-sm">Status:</span>
                    <Badge type="success">Active</Badge>
                </div>
                <div class="flex items-center gap-2">
                    <span class="text-sm">Priority:</span>
                    <Badge type="danger">High</Badge>
                </div>
                <div class="flex items-center gap-2">
                    <span class="text-sm">Category:</span>
                    <Badge type="primary">AI/ML</Badge>
                </div>
                <div class="flex items-center gap-2">
                    <span class="text-sm">Version:</span>
                    <Badge type="secondary">v2.1.0</Badge>
                </div>
            </div>
        `
    })
}
