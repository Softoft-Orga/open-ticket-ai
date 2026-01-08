import Link from '../src/components/vue/core/basic/Link.vue'
import type {Meta, StoryObj} from '@storybook/vue3'

const meta: Meta<typeof Link> = {
    title: 'Core/Link',
    component: Link,
    argTypes: {
        to: {control: 'text', description: 'Internal route path'},
        href: {control: 'text', description: 'External URL'},
        external: {control: 'boolean', description: 'Mark as external link'},
        target: {control: 'text', description: 'Link target attribute'},
        rel: {control: 'text', description: 'Link rel attribute'}
    },
    parameters: {
        docs: {
            description: {
                component: 'Link component supporting both internal routes and external URLs with appropriate security attributes.'
            }
        }
    }
}
export default meta

type Story = StoryObj<typeof meta>

export const Internal: Story = {
    render: (args) => ({
        components: {Link},
        setup() {
            return {args}
        },
        template: '<Link v-bind="args">Internal Documentation Link</Link>'
    }),
    args: {to: '/docs/'}
}

export const External: Story = {
    render: (args) => ({
        components: {Link},
        setup() {
            return {args}
        },
        template: '<Link v-bind="args">View on GitHub</Link>'
    }),
    args: {href: 'https://github.com/Softoft-Orga/open-ticket-ai', external: true}
}

export const ExternalNewTab: Story = {
    render: (args) => ({
        components: {Link},
        setup() {
            return {args}
        },
        template: '<Link v-bind="args">Open in New Tab</Link>'
    }),
    args: {href: 'https://example.com', target: '_blank', rel: 'noopener noreferrer'}
}

export const InContext: Story = {
    render: () => ({
        components: {Link},
        template: `
            <div class="prose prose-invert max-w-2xl">
                <p>
                    For more information, please visit our 
                    <Link to="/docs/">documentation</Link> or check out the
                    <Link href="https://github.com/Softoft-Orga/open-ticket-ai" external>GitHub repository</Link>.
                </p>
            </div>
        `
    }),
}

