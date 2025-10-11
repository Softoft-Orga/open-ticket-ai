import FunctionDoc from '../.vitepress/components/autoDocs/FunctionDoc.vue'
import type {Meta, StoryObj} from '@storybook/vue3'
import {FunctionData} from "../.vitepress/composables/useApiDocs";

const meta: Meta<typeof FunctionDoc> = {
    title: 'Components/FunctionDoc',
    component: FunctionDoc,
}
export default meta

type Story = StoryObj<typeof meta>

const sampleFunc: FunctionData = {
    name: 'add',
    signature: '(a: number, b: number) => number',
    docstring: {
        short_description: 'Adds two numbers',
        long_description: 'Returns the sum of a and b.',
        params: [
            {name: 'a', type: 'number', description: 'The first number to add.'},
        ],
        raises: [],
        returns: {type: 'number', description: 'The sum of a and b.'},
    },
    is_async: false
}

export const Default: Story = {
    render: (args) => ({
        components: {FunctionDoc},
        template: '<FunctionDoc v-bind="args" />'
    }),
    args: {func: sampleFunc}
}
