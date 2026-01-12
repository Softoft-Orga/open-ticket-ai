import Badge from '../src/components/vue/core/basic/Badge.vue'
import type {Meta, StoryObj} from '@storybook/vue3'
import { TONES, SIZES, VARIANTS } from '../src/design-system/tokens'

const meta: Meta<typeof Badge> = {
    title: 'Core/Badge',
    component: Badge,
    argTypes: {
        variant: {control: {type: 'select'}, options: VARIANTS},
        tone: {control: {type: 'select'}, options: TONES},
        size: {control: {type: 'select'}, options: SIZES},
        default: {
            control: 'text',
            description: 'Badge text content (slot)'
        }
    },
    args: {
        variant: 'surface',
        tone: 'primary',
        size: 'md'
    },
    parameters: {
        layout: 'centered',
        docs: {
            description: {
                component: 'Badge component for displaying status, labels, or categories with different variants, tones, and sizes.'
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
    args: {variant: 'surface', tone: 'primary'}
}

export const Info: Story = {
    render: (args) => ({
        components: {Badge},
        setup() {
            return {args}
        },
        template: '<Badge v-bind="args">Info</Badge>'
    }),
    args: {variant: 'solid', tone: 'info'}
}

export const Success: Story = {
    render: (args) => ({
        components: {Badge},
        setup() {
            return {args}
        },
        template: '<Badge v-bind="args">Success</Badge>'
    }),
    args: {variant: 'solid', tone: 'success'}
}

export const Warning: Story = {
    render: (args) => ({
        components: {Badge},
        setup() {
            return {args}
        },
        template: '<Badge v-bind="args">Warning</Badge>'
    }),
    args: {variant: 'solid', tone: 'warning'}
}

export const Danger: Story = {
    render: (args) => ({
        components: {Badge},
        setup() {
            return {args}
        },
        template: '<Badge v-bind="args">Danger</Badge>'
    }),
    args: {variant: 'solid', tone: 'danger'}
}

export const AllTones: Story = {
    render: () => ({
        components: {Badge},
        template: `
            <div class="flex flex-wrap items-center gap-3 rounded-xl bg-surface-dark p-4">
                <Badge tone="neutral">Neutral</Badge>
                <Badge tone="primary">Primary</Badge>
                <Badge tone="info">Info</Badge>
                <Badge tone="success">Success</Badge>
                <Badge tone="warning">Warning</Badge>
                <Badge tone="danger">Danger</Badge>
            </div>
        `
    })
}

export const AllVariants: Story = {
    render: () => ({
        components: {Badge},
        template: `
            <div class="flex flex-wrap items-center gap-3 rounded-xl bg-surface-dark p-4">
                <Badge variant="surface" tone="primary">Surface</Badge>
                <Badge variant="subtle" tone="primary">Subtle</Badge>
                <Badge variant="outline" tone="primary">Outline</Badge>
            </div>
        `
    })
}

export const UseCases: Story = {
    render: () => ({
        components: {Badge},
        template: `
            <div class="space-y-4 rounded-xl bg-surface-dark p-4">
                <div class="flex items-center gap-2">
                    <span class="text-sm text-text-dim">Status:</span>
                    <Badge tone="success">Active</Badge>
                </div>
                <div class="flex items-center gap-2">
                    <span class="text-sm text-text-dim">Priority:</span>
                    <Badge tone="danger">High</Badge>
                </div>
                <div class="flex items-center gap-2">
                    <span class="text-sm text-text-dim">Category:</span>
                    <Badge tone="primary">AI/ML</Badge>
                </div>
                <div class="flex items-center gap-2">
                    <span class="text-sm text-text-dim">Version:</span>
                    <Badge tone="neutral">v2.1.0</Badge>
                </div>
            </div>
        `
    })
}

export const Sizes: Story = {
    render: () => ({
        components: {Badge},
        template: `
            <div class="flex flex-wrap items-center gap-3 rounded-xl bg-surface-dark p-4">
                <Badge tone="primary" size="sm">Small</Badge>
                <Badge tone="primary" size="md">Medium</Badge>
            </div>
        `
    })
}

export const SubtleVariant: Story = {
    render: () => ({
        components: {Badge},
        template: `
            <div class="flex flex-wrap items-center gap-3 rounded-xl bg-surface-dark p-4">
                <Badge variant="subtle" tone="neutral">Neutral</Badge>
                <Badge variant="subtle" tone="primary">Primary</Badge>
                <Badge variant="subtle" tone="info">Info</Badge>
                <Badge variant="subtle" tone="success">Success</Badge>
                <Badge variant="subtle" tone="warning">Warning</Badge>
                <Badge variant="subtle" tone="danger">Danger</Badge>
            </div>
        `
    })
}

export const OutlineVariant: Story = {
    render: () => ({
        components: {Badge},
        template: `
            <div class="flex flex-wrap items-center gap-3 rounded-xl bg-surface-dark p-4">
                <Badge variant="outline" tone="neutral">Neutral</Badge>
                <Badge variant="outline" tone="primary">Primary</Badge>
                <Badge variant="outline" tone="info">Info</Badge>
                <Badge variant="outline" tone="success">Success</Badge>
                <Badge variant="outline" tone="warning">Warning</Badge>
                <Badge variant="outline" tone="danger">Danger</Badge>
            </div>
        `
    })
}
