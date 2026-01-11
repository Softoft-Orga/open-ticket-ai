import Table from '../src/components/vue/core/table/Table.vue'
import Row from '../src/components/vue/core/table/Row.vue'
import C from '../src/components/vue/core/table/C.vue'
import type {Meta, StoryObj} from '@storybook/vue3'
import {ELEVATIONS, RADII} from "../src/design-system/tokens.ts";

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
        radius: {
            control: 'select',
            options: RADII,
            description: 'Border radius size from design tokens (md, lg, xl, 2xl)'
        },
        elevation: {
            control: 'select',
            options: ELEVATIONS,
            description: 'Shadow/elevation level from design tokens (none, sm, md, lg)'
        },
        hoverEffect: {
            control: 'boolean',
            description: 'Enable hover effect on rows'
        }
    },
    parameters: {
        docs: {
            description: {
                component: 'Flexible and responsive table component with multiple style variants, configurable radius and elevation from design tokens, and strong hover effects. Built with Tailwind CSS to match the dark theme design system.'
            }
        }
    },
    args: {
        variant: 'default',
        striped: true,
        dense: false,
        width: 'full',
        hoverEffect: true,
        radius: 'xl',
        elevation: 'sm'
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
        hoverEffect: true,
        radius: 'xl',
        elevation: 'sm'
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
        hoverEffect: true,
        radius: 'xl',
        elevation: 'md'
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
        hoverEffect: true,
        radius: '2xl',
        elevation: 'md'
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
        hoverEffect: true,
        radius: 'xl',
        elevation: 'none'
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
        hoverEffect: true,
        radius: 'lg',
        elevation: 'sm'
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
        hoverEffect: true,
        radius: 'xl',
        elevation: 'sm'
    }
}

export const StretchWidth: Story = {
    render: (args) => ({
        components: {Table, Row, C},
        setup() {
            return {args}
        },
        template: `
            <div class="max-w-5xl">
                <Table v-bind="args">
                    <Row>
                        <C header>Region</C>
                        <C header>Tickets</C>
                        <C header align="right">SLA Met</C>
                    </Row>
                    <Row>
                        <C>North America</C>
                        <C>5,432</C>
                        <C align="right" class="text-success">98.4%</C>
                    </Row>
                    <Row>
                        <C>Europe</C>
                        <C>4,118</C>
                        <C align="right" class="text-success">97.6%</C>
                    </Row>
                    <Row>
                        <C>APAC</C>
                        <C>3,905</C>
                        <C align="right" class="text-warning">94.1%</C>
                    </Row>
                </Table>
            </div>
        `
    }),
    args: {
        width: 'stretch'
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
        hoverEffect: false,
        radius: 'xl',
        elevation: 'sm'
    }
}

export const LargeRadius: Story = {
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
        hoverEffect: true,
        radius: '2xl',
        elevation: 'lg'
    }
}

export const HighElevation: Story = {
    render: (args) => ({
        components: {Table, Row, C},
        setup() {
            return {args}
        },
        template: `
            <div class="bg-gradient-to-br from-background-dark to-surface-dark p-8">
                <Table v-bind="args">
                    <Row>
                        <C header>Priority</C>
                        <C header>Count</C>
                        <C header align="right">Percentage</C>
                    </Row>
                    <Row>
                        <C class="text-danger font-semibold">Critical</C>
                        <C>12</C>
                        <C align="right">8%</C>
                    </Row>
                    <Row>
                        <C class="text-warning font-semibold">High</C>
                        <C>45</C>
                        <C align="right">30%</C>
                    </Row>
                    <Row>
                        <C class="text-info font-semibold">Medium</C>
                        <C>67</C>
                        <C align="right">45%</C>
                    </Row>
                    <Row>
                        <C class="text-success font-semibold">Low</C>
                        <C>26</C>
                        <C align="right">17%</C>
                    </Row>
                </Table>
            </div>
        `
    }),
    args: {
        variant: 'default',
        striped: true,
        dense: false,
        width: 'full',
        hoverEffect: true,
        radius: 'xl',
        elevation: 'lg'
    }
}

export const MinimalRadius: Story = {
    render: (args) => ({
        components: {Table, Row, C},
        setup() {
            return {args}
        },
        template: `
            <Table v-bind="args">
                <Row>
                    <C header>Service</C>
                    <C header align="center">Uptime</C>
                    <C header align="right">Response Time</C>
                </Row>
                <Row>
                    <C>API Gateway</C>
                    <C align="center" class="text-success">99.9%</C>
                    <C align="right">23ms</C>
                </Row>
                <Row>
                    <C>Database</C>
                    <C align="center" class="text-success">99.95%</C>
                    <C align="right">12ms</C>
                </Row>
                <Row>
                    <C>Cache</C>
                    <C align="center" class="text-success">99.99%</C>
                    <C align="right">3ms</C>
                </Row>
            </Table>
        `
    }),
    args: {
        variant: 'compact',
        striped: true,
        dense: true,
        width: 'full',
        hoverEffect: true,
        radius: 'md',
        elevation: 'none'
    }
}
