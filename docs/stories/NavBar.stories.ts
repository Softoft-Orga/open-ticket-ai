import NavBar from '../src/components/vue/navigation/NavBar.vue'
import type {Meta, StoryObj} from '@storybook/vue3'

const meta: Meta<typeof NavBar> = {
    title: 'Navigation/NavBar',
    component: NavBar,
    parameters: {
        layout: 'fullscreen',
    }
}
export default meta

type Story = StoryObj<typeof meta>

export const Default: Story = {
    render: (args) => ({
        components: {NavBar},
        setup() {
            return {args}
        },
        template: '<NavBar v-bind="args" />'
    }),
    args: {}
}

export const WithCustomBrand: Story = {
    render: (args) => ({
        components: {NavBar},
        setup() {
            return {args}
        },
        template: '<NavBar v-bind="args" />'
    }),
    args: {
        brand: {
            name: 'My Product',
            logoSrc: 'https://via.placeholder.com/32',
            href: '/'
        }
    }
}

export const WithCustomLinks: Story = {
    render: (args) => ({
        components: {NavBar},
        setup() {
            return {args}
        },
        template: '<NavBar v-bind="args" />'
    }),
    args: {
        links: [
            {label: 'Home', href: '/'},
            {label: 'Features', href: '/features/'},
            {label: 'Docs', href: '/docs/'},
            {label: 'Contact', href: '/contact/'}
        ]
    }
}

export const WithCTA: Story = {
    render: (args) => ({
        components: {NavBar},
        setup() {
            return {args}
        },
        template: '<NavBar v-bind="args" />'
    }),
    args: {
        ctaButton: {
            label: 'Get Started',
            href: '/getting-started/'
        }
    }
}

export const FullyCustomized: Story = {
    render: (args) => ({
        components: {NavBar},
        setup() {
            return {args}
        },
        template: '<NavBar v-bind="args" />'
    }),
    args: {
        brand: {
            name: 'Open Ticket AI',
            logoSrc: null,
            href: '/'
        },
        links: [
            {label: 'Documentation', href: '/docs/'},
            {label: 'Live Demo', href: '/demo/'},
            {label: 'Marketplace', href: '/marketplace/'},
            {label: 'Pricing', href: '/pricing/'},
            {label: 'Blog', href: '/blog/'}
        ],
        ctaButton: {
            label: 'Try It Free',
            href: '/demo/'
        }
    }
}
