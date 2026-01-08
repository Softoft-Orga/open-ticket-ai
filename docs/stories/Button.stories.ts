import Button from '../src/components/vue/core/basic/Button.vue'
import type {Meta, StoryObj} from '@storybook/vue3'

const meta: Meta<typeof Button> = {
    title: 'Core/Button',
    component: Button,
    argTypes: {
        variant: {control: {type: 'select'}, options: ['primary', 'secondary', 'info', 'success', 'warning', 'danger']},
        disabled: {control: 'boolean'}
    },
}
export default meta

type Story = StoryObj<typeof meta>

export const Primary: Story = {
    render: (args) => ({
        components: {Button},
        setup() {
            return {args}
        },
        template: '<Button v-bind="args">Primary Button</Button>'
    }),
    args: {variant: 'primary', disabled: false}
}

export const Secondary: Story = {
    render: (args) => ({
        components: {Button},
        setup() {
            return {args}
        },
        template: '<Button v-bind="args">Secondary Button</Button>'
    }),
    args: {variant: 'secondary', disabled: false}
}

export const Info: Story = {
    render: (args) => ({
        components: {Button},
        setup() {
            return {args}
        },
        template: '<Button v-bind="args">Info Button</Button>'
    }),
    args: {variant: 'info', disabled: false}
}

export const Success: Story = {
    render: (args) => ({
        components: {Button},
        setup() {
            return {args}
        },
        template: '<Button v-bind="args">Success Button</Button>'
    }),
    args: {variant: 'success', disabled: false}
}

export const Warning: Story = {
    render: (args) => ({
        components: {Button},
        setup() {
            return {args}
        },
        template: '<Button v-bind="args">Warning Button</Button>'
    }),
    args: {variant: 'warning', disabled: false}
}

export const Danger: Story = {
    render: (args) => ({
        components: {Button},
        setup() {
            return {args}
        },
        template: '<Button v-bind="args">Danger Button</Button>'
    }),
    args: {variant: 'danger', disabled: false}
}
