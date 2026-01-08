import Link from '../src/components/vue/core/basic/Link.vue'
import type {Meta, StoryObj} from '@storybook/vue3'

const meta: Meta<typeof Link> = {
    title: 'Core/Link',
    component: Link,
    tags: ['autodocs'],
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
    args: {
        to: '/docs/'
    }
}

export const External: Story = {
    render: (args) => ({
        components: {Link},
        setup() {
            return {args}
        },
        template: '<Link v-bind="args">External Link</Link>'
    }),
    args: {
        href: 'https://github.com/openticketai'
    }
}

export const WithUnderline: Story = {
    render: (args) => ({
        components: {Link},
        setup() {
            return {args}
        },
        template: '<Link v-bind="args">Underlined Link</Link>'
    }),
    args: {
        to: '/about/',
        underline: true
    }
}

export const CustomTarget: Story = {
    render: (args) => ({
        components: {Link},
        setup() {
            return {args}
        },
        template: '<Link v-bind="args">Same Tab External</Link>'
    }),
    args: {
        href: 'https://example.com',
        target: '_self'
    }
}
