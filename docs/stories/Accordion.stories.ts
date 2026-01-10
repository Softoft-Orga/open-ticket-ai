import Accordion from '../src/components/vue/core/accordion/Accordion.vue'
import AccordionItem from '../src/components/vue/core/accordion/AccordionItem.vue'
import {ref} from 'vue'
import type {Meta, StoryObj} from '@storybook/vue3'

const meta: Meta<typeof Accordion> = {
    title: 'Core/Accordion',
    component: Accordion,
    argTypes: {
        multiple: {control: 'boolean'},
        variant: {
            control: 'select',
            options: ['default', 'ghost', 'bordered', 'gradient']
        }
    }
}
export default meta

type Story = StoryObj<typeof meta>

const sampleItems = [
    {title: 'AI-Powered Automation', content: 'Automatically process and resolve tickets using advanced AI algorithms that learn from your team\'s patterns and improve over time.'},
    {title: 'Smart Prioritization', content: 'Intelligent ticket routing and prioritization based on urgency, customer tier, and historical resolution patterns.'},
    {title: 'Multi-Channel Support', content: 'Seamlessly integrate with email, chat, social media, and phone support across all your customer touchpoints.'},
]

const longSampleItems = [
    {title: 'Getting Started', content: 'Learn the basics of our platform with this comprehensive introduction to key features and workflows.'},
    {title: 'Advanced Configuration', content: 'Deep dive into advanced settings, custom rules, and integration options to tailor the system to your needs.'},
    {title: 'API Integration', content: 'Connect your existing tools and services using our robust REST API with comprehensive documentation and examples.'},
    {title: 'Security & Compliance', content: 'Understanding our security measures, data protection policies, and compliance certifications including GDPR and SOC 2.'},
    {title: 'Troubleshooting', content: 'Common issues and their solutions, along with tips for debugging and optimizing performance.'},
]

export const DefaultVariant: Story = {
    render: (args) => ({
        components: {Accordion},
        setup() {
            return {args}
        },
        template: `
            <div class="bg-surface-dark p-8 rounded-lg">
                <h3 class="text-white text-xl font-bold mb-4">Default Variant</h3>
                <Accordion v-bind="args" />
            </div>
        `,
    }),
    args: {
        items: sampleItems,
        multiple: true,
        variant: 'default'
    },
}

export const GhostVariant: Story = {
    render: (args) => ({
        components: {Accordion},
        setup() {
            return {args}
        },
        template: `
            <div class="bg-surface-dark p-8 rounded-lg">
                <h3 class="text-white text-xl font-bold mb-4">Ghost Variant</h3>
                <Accordion v-bind="args" />
            </div>
        `,
    }),
    args: {
        items: sampleItems,
        multiple: true,
        variant: 'ghost'
    },
}

export const BorderedVariant: Story = {
    render: (args) => ({
        components: {Accordion},
        setup() {
            return {args}
        },
        template: `
            <div class="bg-surface-dark p-8 rounded-lg">
                <h3 class="text-white text-xl font-bold mb-4">Bordered Variant</h3>
                <Accordion v-bind="args" />
            </div>
        `,
    }),
    args: {
        items: sampleItems,
        multiple: true,
        variant: 'bordered'
    },
}

export const GradientVariant: Story = {
    render: (args) => ({
        components: {Accordion},
        setup() {
            return {args}
        },
        template: `
            <div class="bg-surface-dark p-8 rounded-lg">
                <h3 class="text-white text-xl font-bold mb-4">Gradient Variant</h3>
                <Accordion v-bind="args" />
            </div>
        `,
    }),
    args: {
        items: sampleItems,
        multiple: true,
        variant: 'gradient'
    },
}

export const SingleMode: Story = {
    render: (args) => ({
        components: {Accordion},
        setup() {
            return {args}
        },
        template: `
            <div class="bg-surface-dark p-8 rounded-lg">
                <h3 class="text-white text-xl font-bold mb-4">Single Mode (Only one item open at a time)</h3>
                <Accordion v-bind="args" />
            </div>
        `,
    }),
    args: {
        items: sampleItems,
        multiple: false,
        variant: 'bordered'
    },
}

export const WithVModel: Story = {
    render: (args) => ({
        components: {Accordion},
        setup() {
            const openItems = ref([0])
            return {args, openItems}
        },
        template: `
            <div class="bg-surface-dark p-8 rounded-lg">
                <h3 class="text-white text-xl font-bold mb-4">Controlled with v-model</h3>
                <p class="mb-4 text-sm text-gray-400">Open items: {{ openItems }}</p>
                <Accordion v-bind="args" v-model="openItems" />
            </div>
        `,
    }),
    args: {
        items: sampleItems,
        multiple: true,
        variant: 'gradient'
    },
}

export const StandaloneItem: Story = {
    render: (args) => ({
        components: {AccordionItem},
        setup() {
            return {args}
        },
        template: `
            <div class="bg-surface-dark p-8 rounded-lg space-y-4">
                <h3 class="text-white text-xl font-bold mb-4">Standalone AccordionItem Examples</h3>
                
                <div>
                    <h4 class="text-white text-sm font-semibold mb-2">Default</h4>
                    <AccordionItem title="Click to expand" variant="default">
                        <p class="text-gray-400">This is a standalone accordion item with default styling.</p>
                    </AccordionItem>
                </div>
                
                <div>
                    <h4 class="text-white text-sm font-semibold mb-2">Bordered</h4>
                    <AccordionItem title="Bordered item" variant="bordered">
                        <p class="text-gray-400">This accordion item has a border and rounded corners.</p>
                    </AccordionItem>
                </div>
                
                <div>
                    <h4 class="text-white text-sm font-semibold mb-2">Gradient</h4>
                    <AccordionItem title="Gradient item" variant="gradient" :default-open="true">
                        <p class="text-gray-400">This accordion item has a gradient background and is open by default.</p>
                    </AccordionItem>
                </div>
            </div>
        `,
    }),
    args: {},
}

export const AllVariantsShowcase: Story = {
    render: (args) => ({
        components: {Accordion},
        setup() {
            return {args, longSampleItems}
        },
        template: `
            <div class="bg-background-dark p-8 space-y-8">
                <div class="bg-surface-dark p-8 rounded-lg">
                    <h3 class="text-white text-2xl font-bold mb-2">Default Variant</h3>
                    <p class="text-gray-400 text-sm mb-6">Clean dividers, minimal styling</p>
                    <Accordion :items="longSampleItems" variant="default" :multiple="true" />
                </div>
                
                <div class="bg-surface-dark p-8 rounded-lg">
                    <h3 class="text-white text-2xl font-bold mb-2">Ghost Variant</h3>
                    <p class="text-gray-400 text-sm mb-6">Subtle, minimal spacing</p>
                    <Accordion :items="longSampleItems" variant="ghost" :multiple="true" />
                </div>
                
                <div class="bg-surface-dark p-8 rounded-lg">
                    <h3 class="text-white text-2xl font-bold mb-2">Bordered Variant</h3>
                    <p class="text-gray-400 text-sm mb-6">Individual cards with borders</p>
                    <Accordion :items="longSampleItems" variant="bordered" :multiple="true" />
                </div>
                
                <div class="bg-surface-dark p-8 rounded-lg">
                    <h3 class="text-white text-2xl font-bold mb-2">Gradient Variant</h3>
                    <p class="text-gray-400 text-sm mb-6">Premium look with gradient backgrounds</p>
                    <Accordion :items="longSampleItems" variant="gradient" :multiple="true" />
                </div>
            </div>
        `,
    }),
    args: {},
}
