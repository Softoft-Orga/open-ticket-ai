import Table from '../src/components/vue/core/table/Table.vue'
import Row from '../src/components/vue/core/table/Row.vue'
import C from '../src/components/vue/core/table/C.vue'
import type {Meta, StoryObj} from '@storybook/vue3'

const meta: Meta<typeof Table> = {
    title: 'Core/Table',
    component: Table,
    argTypes: {
        variant: {
            control: 'select',
            options: ['default', 'bordered', 'borderless', 'glassy', 'compact'],
            description: 'Visual style variant of the table'
        },
        striped: {
            control: 'boolean',
            description: 'Enable alternating row background colors'
        },
        dense: {
            control: 'boolean',
            description: 'Use compact spacing for rows and cells'
        },
        width: {
            control: 'select',
            options: ['full', 'stretch', 'auto'],
            description: 'Table width behavior: full (100% width), stretch (100% with min-width), auto (content-based width)'
        },
        borderColor: {
            control: 'text',
            description: 'Custom border color class (e.g., "primary", "border-dark", "cyan-glow")'
        },
        hoverEffect: {
            control: 'boolean',
            description: 'Enable hover effect on rows'
        }
    },
    parameters: {
        docs: {
            description: {
                component: 'Flexible and responsive table component with multiple style variants, configurable borders, width control, and design token integration. Built with Tailwind CSS to match the website design system.'
            }
        }
    }
}
export default meta

type Story = StoryObj<typeof meta>

export const Default: Story = {
    render: (args) => ({
        components: {Table, Row, C},
        setup() {
            return {args}
        },
        template: `
            <Table v-bind="args">
                <Row>
                    <C header>Feature</C>
                    <C header>Description</C>
                    <C header align="right">Status</C>
                </Row>
                <Row>
                    <C>AI Classification</C>
                    <C>Automatic ticket categorization</C>
                    <C align="right" class="text-success">Active</C>
                </Row>
                <Row>
                    <C>Multi-language</C>
                    <C>Support for 50+ languages</C>
                    <C align="right" class="text-success">Active</C>
                </Row>
                <Row>
                    <C>Custom Training</C>
                    <C>Train on your own data</C>
                    <C align="right" class="text-warning">Beta</C>
                </Row>
                <Row>
                    <C>API Integration</C>
                    <C>RESTful and GraphQL APIs</C>
                    <C align="right" class="text-success">Active</C>
                </Row>
            </Table>
        `
    }),
    args: {
        variant: 'default',
        striped: true,
        dense: false,
        width: 'full',
        hoverEffect: true
    }
}

export const Bordered: Story = {
    render: (args) => ({
        components: {Table, Row, C},
        setup() {
            return {args}
        },
        template: `
            <Table v-bind="args">
                <Row>
                    <C header>Metric</C>
                    <C header align="center">Target</C>
                    <C header align="right">Current</C>
                </Row>
                <Row>
                    <C>Accuracy</C>
                    <C align="center">95%</C>
                    <C align="right" class="text-success font-semibold">95.2%</C>
                </Row>
                <Row>
                    <C>Precision</C>
                    <C align="center">90%</C>
                    <C align="right" class="text-success font-semibold">93.8%</C>
                </Row>
                <Row>
                    <C>Recall</C>
                    <C align="center">92%</C>
                    <C align="right" class="text-success font-semibold">94.5%</C>
                </Row>
                <Row>
                    <C>F1 Score</C>
                    <C align="center">91%</C>
                    <C align="right" class="text-success font-semibold">94.1%</C>
                </Row>
            </Table>
        `
    }),
    args: {
        variant: 'bordered',
        striped: true,
        dense: false,
        width: 'full',
        hoverEffect: true
    }
}

export const Glassy: Story = {
    render: (args) => ({
        components: {Table, Row, C},
        setup() {
            return {args}
        },
        template: `
            <div class="bg-gradient-to-br from-background-dark to-surface-dark p-8 rounded-xl">
                <Table v-bind="args">
                    <Row>
                        <C header>Product</C>
                        <C header>Category</C>
                        <C header align="right">Price</C>
                    </Row>
                    <Row>
                        <C class="font-medium text-primary-light">OpenTicket Lite</C>
                        <C>Automation</C>
                        <C align="right" class="font-semibold">$299/mo</C>
                    </Row>
                    <Row>
                        <C class="font-medium text-primary-light">OpenTicket Pro</C>
                        <C>Enterprise</C>
                        <C align="right" class="font-semibold">$999/mo</C>
                    </Row>
                    <Row>
                        <C class="font-medium text-primary-light">Custom Solutions</C>
                        <C>Enterprise</C>
                        <C align="right" class="font-semibold">Custom</C>
                    </Row>
                </Table>
            </div>
        `
    }),
    args: {
        variant: 'glassy',
        striped: true,
        dense: false,
        width: 'full',
        hoverEffect: true
    }
}

export const Borderless: Story = {
    render: (args) => ({
        components: {Table, Row, C},
        setup() {
            return {args}
        },
        template: `
            <Table v-bind="args">
                <Row>
                    <C header>Name</C>
                    <C header>Role</C>
                    <C header align="right">Tickets Resolved</C>
                </Row>
                <Row>
                    <C class="font-medium">Sarah Johnson</C>
                    <C>Senior Support</C>
                    <C align="right">1,234</C>
                </Row>
                <Row>
                    <C class="font-medium">Mike Chen</C>
                    <C>Support Lead</C>
                    <C align="right">2,567</C>
                </Row>
                <Row>
                    <C class="font-medium">Emma Davis</C>
                    <C>Support Specialist</C>
                    <C align="right">987</C>
                </Row>
            </Table>
        `
    }),
    args: {
        variant: 'borderless',
        striped: true,
        dense: false,
        width: 'full',
        hoverEffect: true
    }
}

export const Compact: Story = {
    render: (args) => ({
        components: {Table, Row, C},
        setup() {
            return {args}
        },
        template: `
            <Table v-bind="args">
                <Row>
                    <C header>ID</C>
                    <C header>Status</C>
                    <C header>Priority</C>
                    <C header align="right">Time</C>
                </Row>
                <Row>
                    <C class="text-text-dim">#1234</C>
                    <C><span class="px-2 py-1 bg-success/20 text-success rounded text-xs">Open</span></C>
                    <C><span class="px-2 py-1 bg-danger/20 text-danger rounded text-xs">High</span></C>
                    <C align="right" class="text-text-dim">2h ago</C>
                </Row>
                <Row>
                    <C class="text-text-dim">#1235</C>
                    <C><span class="px-2 py-1 bg-warning/20 text-warning rounded text-xs">Pending</span></C>
                    <C><span class="px-2 py-1 bg-info/20 text-info rounded text-xs">Medium</span></C>
                    <C align="right" class="text-text-dim">5h ago</C>
                </Row>
                <Row>
                    <C class="text-text-dim">#1236</C>
                    <C><span class="px-2 py-1 bg-muted/20 text-muted rounded text-xs">Closed</span></C>
                    <C><span class="px-2 py-1 bg-success/20 text-success rounded text-xs">Low</span></C>
                    <C align="right" class="text-text-dim">1d ago</C>
                </Row>
            </Table>
        `
    }),
    args: {
        variant: 'compact',
        striped: true,
        dense: true,
        width: 'full',
        hoverEffect: true
    }
}

export const AutoWidth: Story = {
    render: (args) => ({
        components: {Table, Row, C},
        setup() {
            return {args}
        },
        template: `
            <div class="flex justify-center">
                <Table v-bind="args">
                    <Row>
                        <C header>Code</C>
                        <C header>Language</C>
                    </Row>
                    <Row>
                        <C class="font-mono">en</C>
                        <C>English</C>
                    </Row>
                    <Row>
                        <C class="font-mono">es</C>
                        <C>Spanish</C>
                    </Row>
                    <Row>
                        <C class="font-mono">fr</C>
                        <C>French</C>
                    </Row>
                </Table>
            </div>
        `
    }),
    args: {
        variant: 'default',
        striped: true,
        dense: false,
        width: 'auto',
        hoverEffect: true
    }
}

export const CustomBorder: Story = {
    render: (args) => ({
        components: {Table, Row, C},
        setup() {
            return {args}
        },
        template: `
            <Table v-bind="args">
                <Row>
                    <C header>Feature</C>
                    <C header align="right">Enabled</C>
                </Row>
                <Row>
                    <C>AI-Powered Routing</C>
                    <C align="right" class="text-success">✓</C>
                </Row>
                <Row>
                    <C>Smart Categorization</C>
                    <C align="right" class="text-success">✓</C>
                </Row>
                <Row>
                    <C>Auto-Response</C>
                    <C align="right" class="text-danger">✗</C>
                </Row>
            </Table>
        `
    }),
    args: {
        variant: 'bordered',
        striped: false,
        dense: false,
        width: 'full',
        borderColor: 'primary',
        hoverEffect: true
    }
}

export const NoHover: Story = {
    render: (args) => ({
        components: {Table, Row, C},
        setup() {
            return {args}
        },
        template: `
            <Table v-bind="args">
                <Row>
                    <C header>Quarter</C>
                    <C header align="right">Revenue</C>
                    <C header align="right">Growth</C>
                </Row>
                <Row>
                    <C>Q1 2024</C>
                    <C align="right">$1.2M</C>
                    <C align="right" class="text-success">+15%</C>
                </Row>
                <Row>
                    <C>Q2 2024</C>
                    <C align="right">$1.5M</C>
                    <C align="right" class="text-success">+25%</C>
                </Row>
                <Row>
                    <C>Q3 2024</C>
                    <C align="right">$1.8M</C>
                    <C align="right" class="text-success">+20%</C>
                </Row>
            </Table>
        `
    }),
    args: {
        variant: 'default',
        striped: true,
        dense: false,
        width: 'full',
        hoverEffect: false
    }
}
