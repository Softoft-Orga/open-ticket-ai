import type {Meta, StoryObj} from '@storybook/vue3'
import SelectComponent from '../src/components/vue/core/forms/SelectComponent.vue' // Adjust path if needed

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
    title: 'Core/SelectComponent',
    component: SelectComponent,
    // This part is crucial for interacting with the component in Storybook's controls panel
    argTypes: {
        // Props from the component
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

        // Event for v-model
        'update:modelValue': {
            action: 'update:modelValue',
            description: 'Event emitted when the value changes.',
        },
    },
    // Default args apply to all stories unless overridden
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
    {value: 'grape', label: 'Grape 🍇', disabled: true}, // Example of a disabled option
    {value: 'strawberry', label: 'Strawberry 🍓'},
]

/**
 * The default story is the base for all others. It uses a render function
 * to correctly handle v-model updates in Storybook's interactive environment.
 */
export const Default: Story = {
    render: (args) => ({
        components: {SelectComponent},
        setup() {
            // This setup allows the story to be interactive
            const onUpdate = () => {
                // This function is provided by Storybook to update the args
            }
            return {args, onUpdate}
        },
        // Add a wrapper for better presentation in the Storybook canvas
        template: `
          <div style="padding: 1rem; min-height: 250px; width: 300px;">
            <SelectComponent
                v-bind="args"
                :modelValue="args.modelValue"
                @update:modelValue="onUpdate"
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
    ...Default, // Reuses the render function from Default
    args: {
        ...Default.args,
        modelValue: 'banana',
    },
}

/**
 * This story demonstrates the `disabled` state of the component.
 * It is not interactive.
 */
export const Disabled: Story = {
    ...Default,
    args: {
        ...Default.args,
        label: 'Disabled Select',
        modelValue: 'apple',
        disabled: true,
    },
}

/**
 * This story demonstrates error state styling using the input recipe.
 */
export const ErrorState: Story = {
    ...Default,
    args: {
        ...Default.args,
        label: 'Select with Error',
        error: true,
    },
}

/**
 * This story showcases options with disabled state.
 * The "Grape" option cannot be selected.
 */
export const WithDisabledOptions: Story = {
    ...Default,
    args: {
        ...Default.args,
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
    ...Default,
    args: {
        ...Default.args,
        label: 'Small Select',
        size: 'sm',
    },
}

/**
 * Large size variant using input recipe.
 */
export const LargeSize: Story = {
    ...Default,
    args: {
        ...Default.args,
        label: 'Large Select',
        size: 'lg',
    },
}
