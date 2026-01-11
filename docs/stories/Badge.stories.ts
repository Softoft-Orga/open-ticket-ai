import Badge from '../src/components/vue/core/basic/Badge.vue'
import type {Meta, StoryObj} from '@storybook/vue3'
import { TONES, SIZES, RADII, ELEVATIONS } from '../src/design-system/tokens'

// Badge supports brand colors (primary, secondary) plus semantic tones
const BADGE_TYPES = ['primary', 'secondary', ...TONES] as const

const meta: Meta<typeof Badge> = {
    title: 'Core/Badge',
    component: Badge,
    argTypes: {
        type: {control: {type: 'select'}, options: BADGE_TYPES},
        size: {control: {type: 'select'}, options: SIZES},
        radius: {control: {type: 'select'}, options: RADII},
        elevation: {control: {type: 'select'}, options: ELEVATIONS},
        default: {
            control: 'text',
            description: 'Badge text content (slot)'
        }
    },
    args: {
        type: 'secondary',
        size: 'md',
        radius: 'xl',
        elevation: 'sm'
    },
    parameters: {
        layout: 'centered',
        docs: {
            description: {
                component: 'Badge component for displaying status, labels, or categories with different color variants, sizes, border radius, and elevation levels.'
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

export const Info: Story = {
    render: (args) => ({
        components: {Badge},
        setup() {
            return {args}
        },
        template: '<Badge v-bind="args">Info</Badge>'
    }),
    args: {type: 'info'}
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
            <div class="flex flex-wrap items-center gap-3 rounded-xl bg-surface-dark p-4">
                <Badge type="primary">Primary</Badge>
                <Badge type="secondary">Secondary</Badge>
                <Badge type="info">Info</Badge>
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
            <div class="space-y-4 rounded-xl bg-surface-dark p-4">
                <div class="flex items-center gap-2">
                    <span class="text-sm text-text-dim">Status:</span>
                    <Badge type="success">Active</Badge>
                </div>
                <div class="flex items-center gap-2">
                    <span class="text-sm text-text-dim">Priority:</span>
                    <Badge type="danger">High</Badge>
                </div>
                <div class="flex items-center gap-2">
                    <span class="text-sm text-text-dim">Category:</span>
                    <Badge type="primary">AI/ML</Badge>
                </div>
                <div class="flex items-center gap-2">
                    <span class="text-sm text-text-dim">Version:</span>
                    <Badge type="secondary">v2.1.0</Badge>
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
                <Badge type="primary" size="sm">Small</Badge>
                <Badge type="primary" size="md">Medium</Badge>
                <Badge type="primary" size="lg">Large</Badge>
            </div>
        `
    })
}

export const BorderRadius: Story = {
    render: () => ({
        components: {Badge},
        template: `
            <div class="flex flex-wrap items-center gap-3 rounded-xl bg-surface-dark p-4">
                <Badge type="success" radius="md">Medium Radius</Badge>
                <Badge type="success" radius="lg">Large Radius</Badge>
                <Badge type="success" radius="xl">XL Radius</Badge>
                <Badge type="success" radius="2xl">2XL Radius</Badge>
            </div>
        `
    })
}

export const Elevations: Story = {
    render: () => ({
        components: {Badge},
        template: `
            <div class="flex flex-wrap items-center gap-3 rounded-xl bg-surface-dark p-4">
                <Badge type="warning" elevation="none">No Shadow</Badge>
                <Badge type="warning" elevation="sm">Small Shadow</Badge>
                <Badge type="warning" elevation="md">Medium Shadow</Badge>
                <Badge type="warning" elevation="lg">Large Shadow</Badge>
            </div>
        `
    })
}

export const HoverEffects: Story = {
    render: () => ({
        components: {Badge},
        template: `
            <div class="flex flex-wrap items-center gap-3 rounded-xl bg-surface-dark p-4">
                <p class="w-full text-sm text-text-dim mb-2">Hover over badges to see the subtle effect:</p>
                <Badge type="primary">Primary Hover</Badge>
                <Badge type="secondary">Secondary Hover</Badge>
                <Badge type="info">Info Hover</Badge>
                <Badge type="success">Success Hover</Badge>
                <Badge type="warning">Warning Hover</Badge>
                <Badge type="danger">Danger Hover</Badge>
            </div>
        `
    })
}
