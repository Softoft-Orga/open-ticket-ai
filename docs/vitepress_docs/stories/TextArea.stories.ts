// TextArea.stories.ts
import TextArea from '../.vitepress/components/core/forms/TextArea.vue'
import type {Meta, StoryObj} from '@storybook/vue3'

const meta: Meta<typeof TextArea> = {
    title: 'Core/TextArea',
    component: TextArea,
    argTypes: {
        modelValue: {control: 'text'},
        placeholder: {control: 'text'},
        disabled: {control: 'boolean'},
    },
}
export default meta

type Story = StoryObj<typeof meta>

export const Default: Story = {
    render: (args, {updateArgs}) => ({
        components: {TextArea},
        setup() {
            return {args, updateArgs}
        },
        template: `
            <TextArea
                v-bind="args"
                @update:modelValue="value => updateArgs({ modelValue: value })"
            />
        `,
    }),
    args: {
        modelValue: '',
        placeholder: '',
        disabled: false,
    },
}

export const WithPlaceholder: Story = {
    ...Default,
    args: {
        ...Default.args,
        placeholder: 'Enter your description…',
    },
}

export const Disabled: Story = {
    ...Default,
    args: {
        modelValue: 'Read-only content',
        placeholder: 'Disabled textarea',
        disabled: true,
    },
}
