import Docstring from '../.vitepress/components/autoDocs/Docstring.vue'
import type {Meta, StoryObj} from '@storybook/vue3'

const meta: Meta<typeof Docstring> = {
    title: 'Components/Docstring',
    component: Docstring,
}
export default meta

type Story = StoryObj<typeof meta>

const sampleDoc = {
    short_description: 'Example function',
    long_description: 'This is a long description for the example function.',
    params: [
        {name: 'foo', type: 'string', description: 'Foo parameter'}
    ],
    returns: {type: 'number', description: 'Return value'}
}

export const Default: Story = {
    render: (args) => ({
        components: {Docstring},
        setup() {
            return {args}
        },
        template: '<Docstring v-bind="args" />'
    }),
    args: {doc: sampleDoc}
}
