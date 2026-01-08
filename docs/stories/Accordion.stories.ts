import Accordion from '../src/components/vue/core/accordion/Accordion.vue'
import type {Meta, StoryObj} from '@storybook/vue3'
import {ref} from 'vue'

const meta: Meta<typeof Accordion> = {
    title: 'Core/Accordion',
    component: Accordion,
    argTypes: {
        multiple: {control: 'boolean'}
    }
}
export default meta

type Story = StoryObj<typeof meta>

const sampleItems = [
    {title: 'Item 1', content: 'Content of item 1'},
    {title: 'Item 2', content: 'Content of item 2'},
    {title: 'Item 3', content: 'Content of item 3'},
]

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
        multiple: true
    },
}

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
        multiple: false
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
      <div>
        <p class="mb-4 text-sm text-gray-400">Open items: {{ openItems }}</p>
        <Accordion v-bind="args" v-model="openItems" />
      </div>
    `,
    }),
    args: {
        items: sampleItems,
        multiple: true
    },
}
