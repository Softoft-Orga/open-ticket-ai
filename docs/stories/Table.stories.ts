import Table from '../src/components/vue/core/table/Table.vue'
import Row from '../src/components/vue/core/table/Row.vue'
import type {Meta, StoryObj} from '@storybook/vue3'

const meta: Meta<typeof Table> = {
    title: 'Core/Table',
    component: Table,
    argTypes: {
        striped: {
            control: 'boolean',
            description: 'Enable striped rows'
        },
        dense: {
            control: 'boolean',
            description: 'Use dense/compact spacing'
        }
    },
    parameters: {
        docs: {
            description: {
                component: 'Responsive table component with support for striped rows and dense mode. Use Row component for table rows.'
            }
        }
    }
}
export default meta

type Story = StoryObj<typeof meta>

export const Default: Story = {
    render: (args) => ({
        components: {Table, Row},
        setup() {
            return {args}
        },
        template: `
            <Table v-bind="args">
                <Row>
                    <td class="px-4 py-3 font-medium">Feature</td>
                    <td class="px-4 py-3">Description</td>
                    <td class="px-4 py-3 text-right">Status</td>
                </Row>
                <Row>
                    <td class="px-4 py-3 font-medium">AI Classification</td>
                    <td class="px-4 py-3">Automatic ticket categorization</td>
                    <td class="px-4 py-3 text-right text-green-400">Active</td>
                </Row>
                <Row>
                    <td class="px-4 py-3 font-medium">Multi-language</td>
                    <td class="px-4 py-3">Support for 50+ languages</td>
                    <td class="px-4 py-3 text-right text-green-400">Active</td>
                </Row>
                <Row>
                    <td class="px-4 py-3 font-medium">Custom Training</td>
                    <td class="px-4 py-3">Train on your own data</td>
                    <td class="px-4 py-3 text-right text-yellow-400">Beta</td>
                </Row>
            </Table>
        `
    }),
    args: {
        striped: true,
        dense: false
    }
}

export const Dense: Story = {
    render: (args) => ({
        components: {Table, Row},
        setup() {
            return {args}
        },
        template: `
            <Table v-bind="args">
                <Row>
                    <td class="px-3 py-2 font-medium">Metric</td>
                    <td class="px-3 py-2 text-right">Value</td>
                </Row>
                <Row>
                    <td class="px-3 py-2 font-medium">Accuracy</td>
                    <td class="px-3 py-2 text-right">95.2%</td>
                </Row>
                <Row>
                    <td class="px-3 py-2 font-medium">Precision</td>
                    <td class="px-3 py-2 text-right">93.8%</td>
                </Row>
                <Row>
                    <td class="px-3 py-2 font-medium">Recall</td>
                    <td class="px-3 py-2 text-right">94.5%</td>
                </Row>
                <Row>
                    <td class="px-3 py-2 font-medium">F1 Score</td>
                    <td class="px-3 py-2 text-right">94.1%</td>
                </Row>
            </Table>
        `
    }),
    args: {
        striped: true,
        dense: true
    }
}

export const NoStripes: Story = {
    render: (args) => ({
        components: {Table, Row},
        setup() {
            return {args}
        },
        template: `
            <Table v-bind="args">
                <Row>
                    <td class="px-4 py-3 font-medium">Category</td>
                    <td class="px-4 py-3 text-right">Count</td>
                </Row>
                <Row>
                    <td class="px-4 py-3 font-medium">Billing</td>
                    <td class="px-4 py-3 text-right">1,234</td>
                </Row>
                <Row>
                    <td class="px-4 py-3 font-medium">Technical</td>
                    <td class="px-4 py-3 text-right">2,567</td>
                </Row>
                <Row>
                    <td class="px-4 py-3 font-medium">General</td>
                    <td class="px-4 py-3 text-right">789</td>
                </Row>
            </Table>
        `
    }),
    args: {
        striped: false,
        dense: false
    }
}
