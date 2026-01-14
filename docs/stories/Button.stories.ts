import Button from '../src/components/vue/core/basic/Button.vue'
import type {Meta, StoryObj} from '@storybook/vue3'
import { SIZES, TONES, RADII, VARIANTS } from '../src/components/vue/core/design-system/tokens.ts'

const meta: Meta<typeof Button> = {
    title: 'Core/Button',
    component: Button,
    argTypes: {
        variant: {control: {type: 'select'}, options: VARIANTS},
        size: {control: {type: 'select'}, options: SIZES},
        tone: {control: {type: 'select'}, options: [undefined, ...TONES]},
        radius: {control: {type: 'select'}, options: RADII},
        disabled: {control: 'boolean'},
        loading: {control: 'boolean'},
        block: {control: 'boolean'}
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
    args: {variant: 'surface', tone: 'primary', size: 'md', radius: 'xl', disabled: false}
}

export const Solid: Story = {
    render: (args) => ({
        components: {Button},
        setup() {
            return {args}
        },
        template: '<Button v-bind="args">Surface Button</Button>'
    }),
    args: {variant: 'surface', tone: 'primary', size: 'md', radius: 'xl', disabled: false}
}

export const Outline: Story = {
    render: (args) => ({
        components: {Button},
        setup() {
            return {args}
        },
        template: '<Button v-bind="args">Contact Sales</Button>'
    }),
    args: {variant: 'outline', tone: 'primary', size: 'md', radius: 'xl', disabled: false}
}

export const Subtle: Story = {
    render: (args) => ({
        components: {Button},
        setup() {
            return {args}
        },
        template: '<Button v-bind="args">Learn More</Button>'
    }),
    args: {variant: 'subtle', tone: 'primary', size: 'md', radius: 'xl', disabled: false}
}

export const SmallSize: Story = {
    render: (args) => ({
        components: {Button},
        setup() {
            return {args}
        },
        template: '<Button v-bind="args">Small Button</Button>'
    }),
    args: {variant: 'surface', tone: 'primary', size: 'sm', radius: 'xl', disabled: false}
}

export const LargeSize: Story = {
    render: (args) => ({
        components: {Button},
        setup() {
            return {args}
        },
        template: '<Button v-bind="args">Large Button</Button>'
    }),
    args: {variant: 'surface', tone: 'primary', size: 'lg', radius: 'xl', disabled: false}
}

export const Disabled: Story = {
    render: (args) => ({
        components: {Button},
        setup() {
            return {args}
        },
        template: '<Button v-bind="args">Disabled Button</Button>'
    }),
    args: {variant: 'surface', tone: 'primary', size: 'md', radius: 'xl', disabled: true}
}

export const Loading: Story = {
    render: (args) => ({
        components: {Button},
        setup() {
            return {args}
        },
        template: '<Button v-bind="args">Loading...</Button>'
    }),
    args: {variant: 'surface', tone: 'primary', size: 'md', radius: 'xl', loading: true}
}

export const Block: Story = {
    render: (args) => ({
        components: {Button},
        setup() {
            return {args}
        },
        template: '<Button v-bind="args">Block Button</Button>'
    }),
    args: {variant: 'surface', tone: 'primary', size: 'md', radius: 'xl', block: true}
}

export const ToneInfo: Story = {
    render: (args) => ({
        components: {Button},
        setup() {
            return {args}
        },
        template: '<Button v-bind="args">Info Button</Button>'
    }),
    args: {variant: 'surface', tone: 'info', size: 'md', radius: 'xl', disabled: false}
}

export const ToneSuccess: Story = {
    render: (args) => ({
        components: {Button},
        setup() {
            return {args}
        },
        template: '<Button v-bind="args">Success Button</Button>'
    }),
    args: {variant: 'surface', tone: 'success', size: 'md', radius: 'xl', disabled: false}
}

export const ToneWarning: Story = {
    render: (args) => ({
        components: {Button},
        setup() {
            return {args}
        },
        template: '<Button v-bind="args">Warning Button</Button>'
    }),
    args: {variant: 'surface', tone: 'warning', size: 'md', radius: 'xl', disabled: false}
}

export const ToneDanger: Story = {
    render: (args) => ({
        components: {Button},
        setup() {
            return {args}
        },
        template: '<Button v-bind="args">Danger Button</Button>'
    }),
    args: {variant: 'surface', tone: 'danger', size: 'md', radius: 'xl', disabled: false}
}

export const AllVariants: Story = {
    render: () => ({
        components: {Button},
        template: `
            <div style="display: flex; flex-direction: column; gap: 1rem; padding: 2rem;">
                <div style="display: flex; gap: 1rem; flex-wrap: wrap;">
                    <Button variant="surface" tone="primary">Surface</Button>
                    <Button variant="outline" tone="primary">Outline</Button>
                    <Button variant="subtle" tone="primary">Subtle</Button>
                </div>
                <div style="display: flex; gap: 1rem; flex-wrap: wrap;">
                    <Button variant="surface" tone="neutral">Neutral</Button>
                    <Button variant="surface" tone="info">Info</Button>
                    <Button variant="surface" tone="success">Success</Button>
                    <Button variant="surface" tone="warning">Warning</Button>
                    <Button variant="surface" tone="danger">Danger</Button>
                </div>
                <div style="display: flex; gap: 1rem; flex-wrap: wrap;">
                    <Button variant="surface" tone="primary" size="sm">Small</Button>
                    <Button variant="surface" tone="primary" size="md">Medium</Button>
                    <Button variant="surface" tone="primary" size="lg">Large</Button>
                </div>
                <div style="display: flex; gap: 1rem; flex-wrap: wrap;">
                    <Button variant="surface" tone="primary" disabled>Disabled</Button>
                    <Button variant="surface" tone="primary" loading>Loading</Button>
                </div>
            </div>
        `
    })
}
