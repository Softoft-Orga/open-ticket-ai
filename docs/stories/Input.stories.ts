// Input.stories.ts
import TextField from '../src/components/vue/core/forms/TextField.vue'
import {ref} from 'vue'
import type {Meta, StoryObj} from '@storybook/vue3'

const meta: Meta<typeof TextField> = {
    title: 'Core/TextField',
    component: TextField,
    argTypes: {
        modelValue: {control: 'text', description: 'Input value (v-model)'},
        placeholder: {control: 'text', description: 'Placeholder text'},
        disabled: {control: 'boolean', description: 'Disabled state'},
        type: {control: 'text', description: 'Input type attribute'}
    },
    parameters: {
        docs: {
            description: {
                component: 'Text input field component with v-model support and various input types.'
            }
        }
    }
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

export const WithValue: Story = {
    ...Default,
    args: {
        modelValue: 'Example text content',
        placeholder: 'Enter your text here…',
    },
}

export const Disabled: Story = {
    ...Default,
    args: {
        modelValue: 'Cannot edit this field',
        placeholder: 'Disabled field',
        disabled: true,
    },
}

export const EmailInput: Story = {
    ...Default,
    args: {
        modelValue: '',
        placeholder: 'you@example.com',
        type: 'email',
    },
}

export const Interactive: Story = {
    render: (args) => ({
        components: {TextField},
        setup() {
            const value = ref('')
            return {args, value}
        },
        template: `
            <div class="space-y-4">
                <div>
                    <label class="block text-sm font-medium mb-2">Email Address</label>
                    <TextField v-model="value" placeholder="you@example.com" type="email" />
                </div>
                <p class="text-sm text-gray-400">Current value: {{ value || '(empty)' }}</p>
            </div>
        `,
    }),
}

