import CodeDocumentation from '../.vitepress/components/autoDocs/CodeDocumentation.vue'
import type {Meta, StoryObj} from '@storybook/vue3'

const meta: Meta<typeof CodeDocumentation> = {
    title: 'Components/CodeDocumentation',
    component: CodeDocumentation,
}
export default meta

type Story = StoryObj<typeof meta>

export const PackageView: Story = {
    render: (args) => ({
        components: {CodeDocumentation},
        setup() {
            return {args}
        },
        template: '<CodeDocumentation v-bind="args" />'
    }),
    args: {
        packageId: 'scripts.doc_generation'
    }
}

export const ClassView: Story = {
    render: (args) => ({
        components: {CodeDocumentation},
        setup() {
            return {args}
        },
        template: '<CodeDocumentation v-bind="args" />'
    }),
    args: {
        classId: 'scripts.doc_generation.add_docstrings.DocstringGenerator'
    }
}
