// Input.stories.ts
import TextInput from '../src/components/vue/core/forms/TextInput.vue'
import {ref} from 'vue'
import type {Meta, StoryObj} from '@storybook/vue3'

const meta: Meta<typeof TextInput> = {
    title: 'Core/TextInput',
    component: TextInput,
    argTypes: {
        modelValue: {control: 'text', description: 'Input value (v-model)'},
        placeholder: {control: 'text', description: 'Placeholder text'},
        disabled: {control: 'boolean', description: 'Disabled state'},
        type: {control: 'text', description: 'Input type attribute'},
        variant: {control: {type: 'select'}, options: ['primary', 'secondary', 'outline', 'ghost']},
        size: {control: {type: 'select'}, options: ['sm', 'md', 'lg']}
    },
    parameters: {
        docs: {
            description: {
                component: 'Text input field component with v-model support, variants, and dark mode styling.'
            }
        },
        backgrounds: {
            default: 'dark',
            values: [
                { name: 'dark', value: '#0f0814' }
            ]
        }
    }
}
export default meta

type Story = StoryObj<typeof meta>

export const Primary: Story = {
    render: (args, {updateArgs}) => ({
        components: {TextInput},
        setup() {
            return {args, updateArgs}
        },
        template: `
            <TextInput
                v-bind="args"
                @update:modelValue="value => updateArgs({ modelValue: value })"
            />
        `,
    }),
    args: {
        modelValue: '',
        placeholder: 'Enter your text...',
        disabled: false,
        variant: 'primary',
        size: 'md'
    },
}

export const Secondary: Story = {
    render: (args, {updateArgs}) => ({
        components: {TextInput},
        setup() {
            return {args, updateArgs}
        },
        template: `
            <TextInput
                v-bind="args"
                @update:modelValue="value => updateArgs({ modelValue: value })"
            />
        `,
    }),
    args: {
        modelValue: '',
        placeholder: 'Secondary input...',
        disabled: false,
        variant: 'secondary',
        size: 'md'
    },
}

export const Outline: Story = {
    render: (args, {updateArgs}) => ({
        components: {TextInput},
        setup() {
            return {args, updateArgs}
        },
        template: `
            <TextInput
                v-bind="args"
                @update:modelValue="value => updateArgs({ modelValue: value })"
            />
        `,
    }),
    args: {
        modelValue: '',
        placeholder: 'Outline input...',
        disabled: false,
        variant: 'outline',
        size: 'md'
    },
}

export const Ghost: Story = {
    render: (args, {updateArgs}) => ({
        components: {TextInput},
        setup() {
            return {args, updateArgs}
        },
        template: `
            <TextInput
                v-bind="args"
                @update:modelValue="value => updateArgs({ modelValue: value })"
            />
        `,
    }),
    args: {
        modelValue: '',
        placeholder: 'Ghost input...',
        disabled: false,
        variant: 'ghost',
        size: 'md'
    },
}

export const SmallSize: Story = {
    render: (args, {updateArgs}) => ({
        components: {TextInput},
        setup() {
            return {args, updateArgs}
        },
        template: `
            <TextInput
                v-bind="args"
                @update:modelValue="value => updateArgs({ modelValue: value })"
            />
        `,
    }),
    args: {
        modelValue: '',
        placeholder: 'Small input...',
        variant: 'primary',
        size: 'sm'
    },
}

export const LargeSize: Story = {
    render: (args, {updateArgs}) => ({
        components: {TextInput},
        setup() {
            return {args, updateArgs}
        },
        template: `
            <TextInput
                v-bind="args"
                @update:modelValue="value => updateArgs({ modelValue: value })"
            />
        `,
    }),
    args: {
        modelValue: '',
        placeholder: 'Large input...',
        variant: 'primary',
        size: 'lg'
    },
}

export const WithValue: Story = {
    render: (args, {updateArgs}) => ({
        components: {TextInput},
        setup() {
            return {args, updateArgs}
        },
        template: `
            <TextInput
                v-bind="args"
                @update:modelValue="value => updateArgs({ modelValue: value })"
            />
        `,
    }),
    args: {
        modelValue: 'Example text content',
        placeholder: 'Enter your text...',
        variant: 'primary',
        size: 'md'
    },
}

export const Disabled: Story = {
    render: (args, {updateArgs}) => ({
        components: {TextInput},
        setup() {
            return {args, updateArgs}
        },
        template: `
            <TextInput
                v-bind="args"
                @update:modelValue="value => updateArgs({ modelValue: value })"
            />
        `,
    }),
    args: {
        modelValue: 'Cannot edit this field',
        placeholder: 'Disabled field',
        disabled: true,
        variant: 'primary',
        size: 'md'
    },
}

export const EmailInput: Story = {
    render: (args, {updateArgs}) => ({
        components: {TextInput},
        setup() {
            return {args, updateArgs}
        },
        template: `
            <TextInput
                v-bind="args"
                @update:modelValue="value => updateArgs({ modelValue: value })"
            />
        `,
    }),
    args: {
        modelValue: '',
        placeholder: 'you@example.com',
        type: 'email',
        variant: 'primary',
        size: 'md'
    },
}

export const AllVariants: Story = {
    render: () => ({
        components: {TextInput},
        template: `
            <div style="display: flex; flex-direction: column; gap: 1.5rem; padding: 2rem; max-width: 600px;">
                <div>
                    <h3 style="color: #e6e7ea; margin-bottom: 0.5rem; font-size: 0.875rem;">Primary</h3>
                    <TextInput variant="primary" placeholder="Primary input..." />
                </div>
                <div>
                    <h3 style="color: #e6e7ea; margin-bottom: 0.5rem; font-size: 0.875rem;">Secondary</h3>
                    <TextInput variant="secondary" placeholder="Secondary input..." />
                </div>
                <div>
                    <h3 style="color: #e6e7ea; margin-bottom: 0.5rem; font-size: 0.875rem;">Outline</h3>
                    <TextInput variant="outline" placeholder="Outline input..." />
                </div>
                <div>
                    <h3 style="color: #e6e7ea; margin-bottom: 0.5rem; font-size: 0.875rem;">Ghost</h3>
                    <TextInput variant="ghost" placeholder="Ghost input..." />
                </div>
                <div>
                    <h3 style="color: #e6e7ea; margin-bottom: 0.5rem; font-size: 0.875rem;">Sizes</h3>
                    <div style="display: flex; flex-direction: column; gap: 0.75rem;">
                        <TextInput variant="primary" size="sm" placeholder="Small" />
                        <TextInput variant="primary" size="md" placeholder="Medium (default)" />
                        <TextInput variant="primary" size="lg" placeholder="Large" />
                    </div>
                </div>
                <div>
                    <h3 style="color: #e6e7ea; margin-bottom: 0.5rem; font-size: 0.875rem;">Disabled</h3>
                    <TextInput variant="primary" disabled placeholder="Disabled input" modelValue="Cannot edit" />
                </div>
            </div>
        `
    })
}

export const Interactive: Story = {
    render: (args) => ({
        components: {TextInput},
        setup() {
            const value = ref('')
            return {args, value}
        },
        template: `
            <div style="display: flex; flex-direction: column; gap: 1rem; max-width: 400px;">
                <div>
                    <label style="display: block; font-size: 0.875rem; font-weight: 500; margin-bottom: 0.5rem; color: #e6e7ea;">Email Address</label>
                    <TextInput v-model="value" placeholder="you@example.com" type="email" variant="primary" />
                </div>
                <p style="font-size: 0.875rem; color: #b790cb;">Current value: {{ value || '(empty)' }}</p>
            </div>
        `,
    }),
}

