import Accordion from '../src/components/vue/core/accordion/Accordion.vue'
import {ref} from 'vue'
import type {Meta, StoryObj} from '@storybook/vue3'

const meta: Meta<typeof Accordion> = {
    title: 'Core/Accordion',
    component: Accordion,
    argTypes: {
        allowMultiple: {control: 'boolean'}
    }
}
export default meta

type Story = StoryObj<typeof meta>

const sampleItems = [
    {title: 'What is Open Ticket AI?', content: 'Open Ticket AI is an AI-powered ticket classification system.'},
    {title: 'How does it work?', content: 'It uses machine learning models to automatically categorize support tickets.'},
    {title: 'Is it open source?', content: 'Yes! Open Ticket AI is fully open source and available on GitHub.'},
]

export const SingleMode: Story = {
    render: (args) => ({
        components: {Accordion},
        setup() {
            return {args}
        },
        template: '<Accordion v-bind="args" />',
    }),
    args: {
        items: sampleItems,
        allowMultiple: false
    },
}

export const MultipleMode: Story = {
    render: (args) => ({
        components: {Accordion},
        setup() {
            return {args}
        },
        template: '<Accordion v-bind="args" />',
    }),
    args: {
        items: sampleItems,
        allowMultiple: true
    },
}

export const WithDefaultOpen: Story = {
    render: (args) => ({
        components: {Accordion},
        setup() {
            return {args}
        },
        template: '<Accordion v-bind="args" />',
    }),
    args: {
        items: [
            {title: 'First Item (Open by default)', content: 'This item is open by default.', defaultOpen: true},
            {title: 'Second Item', content: 'This item is closed by default.'},
            {title: 'Third Item', content: 'This item is also closed by default.'},
        ],
        allowMultiple: true
    },
}

export const WithVModel: Story = {
    render: (args) => ({
        components: {Accordion},
        setup() {
            const openItems = ref([0, 2])
            return {args, openItems}
        },
        template: `
      <div>
        <p class="mb-4 text-sm">Open items: {{ openItems }}</p>
        <Accordion v-bind="args" v-model="openItems" />
      </div>
    `,
    }),
    args: {
        items: sampleItems,
        allowMultiple: true
    },
}
