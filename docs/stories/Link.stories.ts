import Link from '../src/components/vue/core/basic/Link.vue'
import type {Meta, StoryObj} from '@storybook/vue3'

const meta: Meta<typeof Link> = {
    title: 'Core/Link',
    component: Link,
    argTypes: {
        to: {control: 'text'},
        href: {control: 'text'},
        external: {control: 'boolean'},
        target: {control: 'text'},
        rel: {control: 'text'}
    },
}
export default meta

type Story = StoryObj<typeof meta>

export const Internal: Story = {
    render: (args) => ({
        components: {Link},
        setup() {
            return {args}
        },
        template: '<Link v-bind="args">Internal Link</Link>'
    }),
    args: {to: '/docs/'}
}

export const External: Story = {
    render: (args) => ({
        components: {Link},
        setup() {
            return {args}
        },
        template: '<Link v-bind="args">External Link</Link>'
    }),
    args: {href: 'https://github.com', external: true}
}

export const WithCustomTarget: Story = {
    render: (args) => ({
        components: {Link},
        setup() {
            return {args}
        },
        template: '<Link v-bind="args">Link in New Tab</Link>'
    }),
    args: {href: 'https://example.com', target: '_blank'}
}
