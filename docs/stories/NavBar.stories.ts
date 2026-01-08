import NavBar from '../src/components/vue/navigation/NavBar.vue'
import type {Meta, StoryObj} from '@storybook/vue3'

const meta: Meta<typeof NavBar> = {
    title: 'Navigation/NavBar',
    component: NavBar,
    tags: ['autodocs'],
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
}

export const WithLogo: Story = {
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
            tagline: 'AI-Powered Ticketing',
            logoSrc: 'https://via.placeholder.com/32'
        }
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
        cta: {
            label: 'Get Started',
            href: '/getting-started/'
        }
    }
}

export const CustomLinks: Story = {
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
            {label: 'Solutions', href: '/solutions/'},
            {label: 'Contact', href: '/contact/'},
        ],
        cta: {
            label: 'Sign Up',
            href: '/signup/'
        }
    }
}

export const Full: Story = {
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
            tagline: 'Intelligent Support',
            logoSrc: 'https://via.placeholder.com/32'
        },
        links: [
            {label: 'Product', href: '/product/'},
            {label: 'Solutions', href: '/solutions/'},
            {label: 'Docs', href: '/docs/'},
            {label: 'Pricing', href: '/pricing/'},
        ],
        cta: {
            label: 'Try Demo',
            href: '/demo/'
        }
    }
}
