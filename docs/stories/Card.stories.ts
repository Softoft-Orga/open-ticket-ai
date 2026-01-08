import Card from '../src/components/vue/core/basic/Card.vue'
import Badge from '../src/components/vue/core/basic/Badge.vue'
import type {Meta, StoryObj} from '@storybook/vue3'

const meta: Meta<typeof Card> = {
    title: 'Core/Card',
    component: Card,
    tags: ['autodocs'],
    parameters: {
        docs: {
            description: {
                component: 'Card component with optional header and footer slots for structured content display.'
            }
        }
    }
}
export default meta

type Story = StoryObj<typeof meta>

export const Default: Story = {
    render: (args) => ({
        components: {Card},
        setup() {
            return {args}
        },
        template: '<Card>Simple card content without header or footer.</Card>'
    }),
}

export const WithHeader: Story = {
    render: (args) => ({
        components: {Card},
        setup() {
            return {args}
        },
        template: `
            <Card>
                <template #header>
                    <h3 class="text-lg font-bold">Card Title</h3>
                </template>
                <p>Main card content goes here with a header section above.</p>
            </Card>
        `
    }),
}

export const WithFooter: Story = {
    render: (args) => ({
        components: {Card},
        setup() {
            return {args}
        },
        template: `
            <Card>
                <p>Main card content with action buttons in the footer.</p>
                <template #footer>
                    <button class="text-vp-brand hover:underline">Learn More</button>
                </template>
            </Card>
        `
    }),
}

export const Full: Story = {
    render: (args) => ({
        components: {Card},
        setup() {
            return {args}
        },
        template: `
            <Card>
                <template #header>
                    <h3 class="text-lg font-bold">Complete Card Example</h3>
                </template>
                <p>Main content with both header and footer sections.</p>
                <template #footer>
                    <div class="flex justify-end gap-2">
                        <button class="px-4 py-2 bg-gray-700 text-white rounded hover:bg-gray-600">Cancel</button>
                        <button class="px-4 py-2 bg-indigo-600 text-white rounded hover:bg-indigo-500">Confirm</button>
                    </div>
                </template>
            </Card>
        `
    }),
}

export const WithRichContent: Story = {
    render: () => ({
        components: {Card, Badge},
        template: `
            <Card>
                <template #header>
                    <div class="flex items-center justify-between">
                        <h3 class="text-lg font-bold">AI Classification Result</h3>
                        <Badge type="success">Completed</Badge>
                    </div>
                </template>
                <div class="space-y-2">
                    <p><strong>Category:</strong> Technical Support</p>
                    <p><strong>Confidence:</strong> 94.5%</p>
                    <p><strong>Processing Time:</strong> 120ms</p>
                    <p class="text-sm text-gray-400">Ticket classified using AI model v2.1.0</p>
                </div>
                <template #footer>
                    <div class="flex justify-between items-center">
                        <span class="text-xs text-gray-500">Processed: 2024-01-15 10:30:00</span>
                        <button class="text-vp-brand hover:underline text-sm">View Details</button>
                    </div>
                </template>
            </Card>
        `
    }),
}

export const Grid: Story = {
    render: () => ({
        components: {Card},
        template: `
            <div class="grid gap-4 md:grid-cols-2 lg:grid-cols-3">
                <Card>
                    <template #header>
                        <h4 class="font-semibold">Accuracy</h4>
                    </template>
                    <p class="text-3xl font-bold text-green-400">95.2%</p>
                </Card>
                <Card>
                    <template #header>
                        <h4 class="font-semibold">Tickets Processed</h4>
                    </template>
                    <p class="text-3xl font-bold text-blue-400">12,543</p>
                </Card>
                <Card>
                    <template #header>
                        <h4 class="font-semibold">Avg Response Time</h4>
                    </template>
                    <p class="text-3xl font-bold text-purple-400">85ms</p>
                </Card>
            </div>
        `
    }),
}
