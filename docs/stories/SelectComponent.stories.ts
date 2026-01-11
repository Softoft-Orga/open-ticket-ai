import type {Meta, StoryObj} from '@storybook/vue3'
import SelectComponent from '../src/components/vue/core/forms/SelectComponent.vue'
import { ref } from 'vue'

/**
 * A modern, accessible select component built with Headless UI Listbox and Tailwind design tokens.
 * 
 * Features:
 * - Keyboard navigation support
 * - Focus rings using primary color tokens
 * - Disabled options support
 * - Smooth slide-down transitions
 * - Placeholder and default value behavior
 * - Error state with input recipe
 * - Size variants (sm, md, lg)
 */
const meta: Meta<typeof SelectComponent> = {
    title: 'Core/Forms/SelectComponent',
    component: SelectComponent,
    argTypes: {
        label: {
            control: 'text',
            description: 'The label displayed above the select input.',
        },
        modelValue: {
            control: 'select',
            options: [null, 'apple', 'banana', 'cherry'],
            description: 'The selected value (v-model).',
        },
        placeholder: {
            control: 'text',
            description: 'Placeholder text shown when no value is selected.',
        },
        options: {
            control: 'object',
            description: 'Array of options. Each must have a `value`, `label`, and optional `disabled` property.',
        },
        disabled: {
            control: 'boolean',
            description: 'Disables the select input.',
        },
        error: {
            control: 'boolean',
            description: 'Shows error state styling.',
        },
        size: {
            control: 'select',
            options: ['sm', 'md', 'lg'],
            description: 'Size variant from input recipe.',
        },
    },
    parameters: {
        backgrounds: {
            default: 'dark',
            values: [
                { name: 'dark', value: '#0f0814' }
            ]
        }
    },
    args: {
        label: 'Select a Fruit',
        placeholder: 'Choose an option...',
        modelValue: null,
        disabled: false,
        error: false,
        size: 'md'
    },
}

export default meta

type Story = StoryObj<typeof meta>

const sampleOptions = [
    {value: 'apple', label: 'Apple 🍎'},
    {value: 'banana', label: 'Banana 🍌'},
    {value: 'cherry', label: 'Cherry 🍒'},
    {value: 'grape', label: 'Grape 🍇', disabled: true},
    {value: 'strawberry', label: 'Strawberry 🍓'},
]

/**
 * The default story demonstrates basic usage with proper v-model binding.
 */
export const Default: Story = {
    render: (args) => ({
        components: { SelectComponent },
        setup() {
            const selected = ref(args.modelValue)
            return { args, selected }
        },
        template: `
          <div style="padding: 1rem; min-height: 250px; width: 300px;">
            <SelectComponent
                v-bind="args"
                v-model="selected"
            />
          </div>
        `,
    }),
    args: {
        options: sampleOptions,
    },
}

/**
 * This story demonstrates the component with a pre-selected value.
 */
export const WithDefaultValue: Story = {
    render: (args) => ({
        components: { SelectComponent },
        setup() {
            const selected = ref(args.modelValue)
            return { args, selected }
        },
        template: `
          <div style="padding: 1rem; min-height: 250px; width: 300px;">
            <SelectComponent
                v-bind="args"
                v-model="selected"
            />
          </div>
        `,
    }),
    args: {
        options: sampleOptions,
        modelValue: 'banana',
    },
}

/**
 * This story demonstrates the `disabled` state of the component.
 */
export const Disabled: Story = {
    render: (args) => ({
        components: { SelectComponent },
        setup() {
            const selected = ref(args.modelValue)
            return { args, selected }
        },
        template: `
          <div style="padding: 1rem; min-height: 250px; width: 300px;">
            <SelectComponent
                v-bind="args"
                v-model="selected"
            />
          </div>
        `,
    }),
    args: {
        options: sampleOptions,
        label: 'Disabled Select',
        modelValue: 'apple',
        disabled: true,
    },
}

/**
 * This story demonstrates error state styling using the input recipe.
 */
export const ErrorState: Story = {
    render: (args) => ({
        components: { SelectComponent },
        setup() {
            const selected = ref(args.modelValue)
            return { args, selected }
        },
        template: `
          <div style="padding: 1rem; min-height: 250px; width: 300px;">
            <SelectComponent
                v-bind="args"
                v-model="selected"
            />
          </div>
        `,
    }),
    args: {
        options: sampleOptions,
        label: 'Select with Error',
        error: true,
    },
}

/**
 * This story showcases options with disabled state.
 */
export const WithDisabledOptions: Story = {
    render: (args) => ({
        components: { SelectComponent },
        setup() {
            const selected = ref(args.modelValue)
            return { args, selected }
        },
        template: `
          <div style="padding: 1rem; min-height: 250px; width: 300px;">
            <SelectComponent
                v-bind="args"
                v-model="selected"
            />
          </div>
        `,
    }),
    args: {
        label: 'Select with Disabled Options',
        options: [
            {value: 'apple', label: 'Apple 🍎'},
            {value: 'banana', label: 'Banana 🍌'},
            {value: 'cherry', label: 'Cherry 🍒'},
            {value: 'grape', label: 'Grape 🍇 (Unavailable)', disabled: true},
            {value: 'orange', label: 'Orange 🍊', disabled: true},
            {value: 'strawberry', label: 'Strawberry 🍓'},
        ],
    },
}

/**
 * Small size variant using input recipe.
 */
export const SmallSize: Story = {
    render: (args) => ({
        components: { SelectComponent },
        setup() {
            const selected = ref(args.modelValue)
            return { args, selected }
        },
        template: `
          <div style="padding: 1rem; min-height: 250px; width: 300px;">
            <SelectComponent
                v-bind="args"
                v-model="selected"
            />
          </div>
        `,
    }),
    args: {
        options: sampleOptions,
        label: 'Small Select',
        size: 'sm',
    },
}

/**
 * Large size variant using input recipe.
 */
export const LargeSize: Story = {
    render: (args) => ({
        components: { SelectComponent },
        setup() {
            const selected = ref(args.modelValue)
            return { args, selected }
        },
        template: `
          <div style="padding: 1rem; min-height: 250px; width: 300px;">
            <SelectComponent
                v-bind="args"
                v-model="selected"
            />
          </div>
        `,
    }),
    args: {
        options: sampleOptions,
        label: 'Large Select',
        size: 'lg',
    },
}
