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
        navItems: [
            {label: 'Products', href: '/products/'},
            {label: 'Services', href: '/services/'},
            {label: 'Docs', href: '/docs/'},
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
        navItems: [
            {label: 'Products', href: '/products/'},
            {label: 'Services', href: '/services/'},
            {label: 'Docs', href: '/docs/'},
        ]
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
        navItems: [
            {label: 'Home', href: '/'},
            {label: 'Features', href: '/features/'},
            {label: 'Solutions', href: '/solutions/'},
            {label: 'Contact', href: '/contact/'},
        ]
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
        navItems: [
             {label: 'Product', href: '/product/'},
             {label: 'Solutions', href: '/solutions/'},
             {label: 'Docs', href: '/docs/'},
             {label: 'Pricing', href: '/pricing/'},
        ]
    }
}

export const DocsDropdown: Story = {
    render: (args) => ({
        components: {NavBar},
        setup() {
            return {args}
        },
        template: '<div class="bg-slate-900 p-4"><NavBar v-bind="args" /></div>'
    }),
    args: {
        navItems: [
             {label: 'Home', href: '/'},
             {label: 'Solutions', href: '/solutions/'},
             {label: 'Pricing', href: '/pricing/'},
        ]
    }
}
