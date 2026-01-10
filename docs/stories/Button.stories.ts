import Button from '../src/components/vue/core/basic/Button.vue'
import type {Meta, StoryObj} from '@storybook/vue3'
import { VARIANTS, SIZES, TONES, RADII, ELEVATIONS } from '../src/components/vue/core/design-system/tokens'

const meta: Meta<typeof Button> = {
    title: 'Core/Button',
    component: Button,
    argTypes: {
        variant: {control: {type: 'select'}, options: VARIANTS},
        size: {control: {type: 'select'}, options: SIZES},
        tone: {control: {type: 'select'}, options: [undefined, ...TONES]},
        radius: {control: {type: 'select'}, options: RADII},
        elevation: {control: {type: 'select'}, options: ELEVATIONS},
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
    args: {variant: 'primary', size: 'md', radius: 'xl', elevation: 'none', disabled: false}
}

export const Secondary: Story = {
    render: (args) => ({
        components: {Button},
        setup() {
            return {args}
        },
        template: '<Button v-bind="args">Get Lite Free</Button>'
    }),
    args: {variant: 'secondary', size: 'md', radius: 'xl', elevation: 'none', disabled: false}
}

export const Outline: Story = {
    render: (args) => ({
        components: {Button},
        setup() {
            return {args}
        },
        template: '<Button v-bind="args">Contact Sales</Button>'
    }),
    args: {variant: 'outline', size: 'md', radius: 'xl', elevation: 'none', disabled: false}
}

export const Ghost: Story = {
    render: (args) => ({
        components: {Button},
        setup() {
            return {args}
        },
        template: '<Button v-bind="args">Learn More</Button>'
    }),
    args: {variant: 'ghost', size: 'md', radius: 'xl', elevation: 'none', disabled: false}
}

export const SmallSize: Story = {
    render: (args) => ({
        components: {Button},
        setup() {
            return {args}
        },
        template: '<Button v-bind="args">Small Button</Button>'
    }),
    args: {variant: 'primary', size: 'sm', radius: 'xl', elevation: 'none', disabled: false}
}

export const LargeSize: Story = {
    render: (args) => ({
        components: {Button},
        setup() {
            return {args}
        },
        template: '<Button v-bind="args">Large Button</Button>'
    }),
    args: {variant: 'primary', size: 'lg', radius: 'xl', elevation: 'none', disabled: false}
}

export const Disabled: Story = {
    render: (args) => ({
        components: {Button},
        setup() {
            return {args}
        },
        template: '<Button v-bind="args">Disabled Button</Button>'
    }),
    args: {variant: 'primary', size: 'md', radius: 'xl', elevation: 'none', disabled: true}
}

export const ToneInfo: Story = {
    render: (args) => ({
        components: {Button},
        setup() {
            return {args}
        },
        template: '<Button v-bind="args">Info Button</Button>'
    }),
    args: {tone: 'info', size: 'md', radius: 'xl', elevation: 'none', disabled: false}
}

export const ToneSuccess: Story = {
    render: (args) => ({
        components: {Button},
        setup() {
            return {args}
        },
        template: '<Button v-bind="args">Success Button</Button>'
    }),
    args: {tone: 'success', size: 'md', radius: 'xl', elevation: 'none', disabled: false}
}

export const ToneWarning: Story = {
    render: (args) => ({
        components: {Button},
        setup() {
            return {args}
        },
        template: '<Button v-bind="args">Warning Button</Button>'
    }),
    args: {tone: 'warning', size: 'md', radius: 'xl', elevation: 'none', disabled: false}
}

export const ToneDanger: Story = {
    render: (args) => ({
        components: {Button},
        setup() {
            return {args}
        },
        template: '<Button v-bind="args">Danger Button</Button>'
    }),
    args: {tone: 'danger', size: 'md', radius: 'xl', elevation: 'none', disabled: false}
}

export const WithElevation: Story = {
    render: (args) => ({
        components: {Button},
        setup() {
            return {args}
        },
        template: '<Button v-bind="args">Elevated Button</Button>'
    }),
    args: {variant: 'primary', size: 'md', radius: 'xl', elevation: 'lg', disabled: false}
}

export const CustomRadius: Story = {
    render: (args) => ({
        components: {Button},
        setup() {
            return {args}
        },
        template: '<Button v-bind="args">Rounded Button</Button>'
    }),
    args: {variant: 'primary', size: 'md', radius: '2xl', elevation: 'none', disabled: false}
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
                    <Button tone="info">Info</Button>
                    <Button tone="success">Success</Button>
                    <Button tone="warning">Warning</Button>
                    <Button tone="danger">Danger</Button>
                </div>
                <div style="display: flex; gap: 1rem; flex-wrap: wrap;">
                    <Button variant="primary" size="sm">Small</Button>
                    <Button variant="primary" size="md">Medium</Button>
                    <Button variant="primary" size="lg">Large</Button>
                </div>
                <div style="display: flex; gap: 1rem; flex-wrap: wrap;">
                    <Button variant="primary" radius="md">MD Radius</Button>
                    <Button variant="primary" radius="lg">LG Radius</Button>
                    <Button variant="primary" radius="xl">XL Radius</Button>
                    <Button variant="primary" radius="2xl">2XL Radius</Button>
                </div>
                <div style="display: flex; gap: 1rem; flex-wrap: wrap;">
                    <Button variant="primary" elevation="none">No Shadow</Button>
                    <Button variant="primary" elevation="sm">Small Shadow</Button>
                    <Button variant="primary" elevation="md">Medium Shadow</Button>
                    <Button variant="primary" elevation="lg">Large Shadow</Button>
                </div>
                <div style="display: flex; gap: 1rem; flex-wrap: wrap;">
                    <Button variant="primary" disabled>Disabled</Button>
                    <Button variant="outline" disabled>Disabled Outline</Button>
                </div>
            </div>
        `
    })
}
