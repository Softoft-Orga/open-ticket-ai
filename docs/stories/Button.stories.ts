import Button from '../src/components/vue/core/basic/Button.vue'
import type {Meta, StoryObj} from '@storybook/vue3'

const meta: Meta<typeof Button> = {
    title: 'Core/Button',
    component: Button,
    argTypes: {
        variant: {control: {type: 'select'}, options: ['primary', 'secondary', 'outline', 'ghost']},
        size: {control: {type: 'select'}, options: ['sm', 'md', 'lg']},
        disabled: {control: 'boolean'}
    },
    parameters: {
        backgrounds: {
            default: 'dark',
            values: [
                { name: 'dark', value: '#0f0814' }
            ]
        }
    }
}
export default meta

type Story = StoryObj<typeof meta>

export const Primary: Story = {
    render: (args) => ({
        components: {Button},
        setup() {
            return {args}
        },
        template: '<Button v-bind="args">Get Demo</Button>'
    }),
    args: {variant: 'primary', size: 'md', disabled: false}
}

export const Secondary: Story = {
    render: (args) => ({
        components: {Button},
        setup() {
            return {args}
        },
        template: '<Button v-bind="args">Get Lite Free</Button>'
    }),
    args: {variant: 'secondary', size: 'md', disabled: false}
}

export const Outline: Story = {
    render: (args) => ({
        components: {Button},
        setup() {
            return {args}
        },
        template: '<Button v-bind="args">Contact Sales</Button>'
    }),
    args: {variant: 'outline', size: 'md', disabled: false}
}

export const Ghost: Story = {
    render: (args) => ({
        components: {Button},
        setup() {
            return {args}
        },
        template: '<Button v-bind="args">Learn More</Button>'
    }),
    args: {variant: 'ghost', size: 'md', disabled: false}
}

export const SmallSize: Story = {
    render: (args) => ({
        components: {Button},
        setup() {
            return {args}
        },
        template: '<Button v-bind="args">Small Button</Button>'
    }),
    args: {variant: 'primary', size: 'sm', disabled: false}
}

export const LargeSize: Story = {
    render: (args) => ({
        components: {Button},
        setup() {
            return {args}
        },
        template: '<Button v-bind="args">Large Button</Button>'
    }),
    args: {variant: 'primary', size: 'lg', disabled: false}
}

export const Disabled: Story = {
    render: (args) => ({
        components: {Button},
        setup() {
            return {args}
        },
        template: '<Button v-bind="args">Disabled Button</Button>'
    }),
    args: {variant: 'primary', size: 'md', disabled: true}
}

export const AllVariants: Story = {
    render: () => ({
        components: {Button},
        template: `
            <div style="display: flex; flex-direction: column; gap: 1rem; padding: 2rem;">
                <div style="display: flex; gap: 1rem; flex-wrap: wrap;">
                    <Button variant="primary">Primary</Button>
                    <Button variant="secondary">Secondary</Button>
                    <Button variant="outline">Outline</Button>
                    <Button variant="ghost">Ghost</Button>
                </div>
                <div style="display: flex; gap: 1rem; flex-wrap: wrap;">
                    <Button variant="primary" size="sm">Small</Button>
                    <Button variant="primary" size="md">Medium</Button>
                    <Button variant="primary" size="lg">Large</Button>
                </div>
                <div style="display: flex; gap: 1rem; flex-wrap: wrap;">
                    <Button variant="primary" disabled>Disabled</Button>
                    <Button variant="outline" disabled>Disabled Outline</Button>
                </div>
            </div>
        `
    })
}
