// Input.stories.ts
import TextField from '../.vitepress/components/core/forms/TextField.vue'
import type {Meta, StoryObj} from '@storybook/vue3'

const meta: Meta<typeof TextField> = {
    title: 'Core/TextField',
    component: TextField,
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
        components: {TextField},
        setup() {
            return {args, updateArgs}
        },
        template: `
            <TextField
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
        placeholder: 'Enter your text here…',
    },
}

export const Disabled: Story = {
    ...Default,
    args: {
        modelValue: 'Cannot edit',
        placeholder: 'Disabled field',
        disabled: true,
    },
}
