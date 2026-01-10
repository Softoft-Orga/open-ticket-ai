// TextArea.stories.ts
import TextArea from '../src/components/vue/core/forms/TextArea.vue'
import type {Meta, StoryObj} from '@storybook/vue3'
import { ChatBubbleLeftRightIcon } from '@heroicons/vue/24/outline'
import { SIZES } from '../src/components/vue/core/design-system/tokens'

const meta: Meta<typeof TextArea> = {
    title: 'Core/Forms/TextArea',
    component: TextArea,
    argTypes: {
        modelValue: {control: 'text'},
        placeholder: {control: 'text'},
        disabled: {control: 'boolean'},
        size: {
            control: 'select',
            options: SIZES,
        },
        autoResize: {control: 'boolean'},
    },
    parameters: {
        backgrounds: {
            default: 'dark',
            values: [
                { name: 'dark', value: '#0f0814' },
            ],
        },
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
            <div class="p-8">
                <TextArea
                    v-bind="args"
                    @update:modelValue="value => updateArgs({ modelValue: value })"
                />
            </div>
        `,
    }),
    args: {
        modelValue: '',
        placeholder: 'Enter your message here...',
        disabled: false,
        size: 'md',
        autoResize: true,
    },
}

export const WithPlaceholder: Story = {
    ...Default,
    args: {
        ...Default.args,
        placeholder: 'Describe your issue in detail…',
    },
}

export const WithIcon: Story = {
    render: (args, {updateArgs}) => ({
        components: {TextArea},
        setup() {
            return {args, updateArgs, ChatBubbleLeftRightIcon}
        },
        template: `
            <div class="p-8">
                <TextArea
                    v-bind="args"
                    :icon="ChatBubbleLeftRightIcon"
                    @update:modelValue="value => updateArgs({ modelValue: value })"
                />
            </div>
        `,
    }),
    args: {
        modelValue: '',
        placeholder: 'How can we help you?',
        disabled: false,
    },
}

export const WithContent: Story = {
    ...Default,
    args: {
        modelValue: 'This is some existing content in the textarea. The styling now matches our website\'s design system with purple accents and glassy surfaces.',
        placeholder: 'Enter your description…',
        disabled: false,
    },
}

export const Disabled: Story = {
    ...Default,
    args: {
        modelValue: 'Read-only content that cannot be edited',
        placeholder: 'Disabled textarea',
        disabled: true,
    },
}

export const LongContent: Story = {
    ...Default,
    args: {
        modelValue: `This is a longer piece of content to demonstrate how the TextArea handles multiple lines of text.

The styling includes:
- Deep purple theme colors
- Glassy surface effect
- Neon purple glow on focus
- Smooth transitions
- Consistent with the overall design system`,
        placeholder: 'Enter your description…',
        disabled: false,
        size: 'md',
        autoResize: true,
    },
}

export const SmallSize: Story = {
    render: (args, {updateArgs}) => ({
        components: {TextArea},
        setup() {
            return {args, updateArgs}
        },
        template: `
            <div class="p-8">
                <TextArea
                    v-bind="args"
                    @update:modelValue="value => updateArgs({ modelValue: value })"
                />
            </div>
        `,
    }),
    args: {
        modelValue: '',
        placeholder: 'Small textarea...',
        disabled: false,
        size: 'sm',
        autoResize: true,
    },
}

export const LargeSize: Story = {
    render: (args, {updateArgs}) => ({
        components: {TextArea},
        setup() {
            return {args, updateArgs}
        },
        template: `
            <div class="p-8">
                <TextArea
                    v-bind="args"
                    @update:modelValue="value => updateArgs({ modelValue: value })"
                />
            </div>
        `,
    }),
    args: {
        modelValue: '',
        placeholder: 'Large textarea with more space...',
        disabled: false,
        size: 'lg',
        autoResize: true,
    },
}

export const AllSizes: Story = {
    render: (args) => ({
        components: {TextArea},
        setup() {
            return {args}
        },
        template: `
            <div class="p-8 space-y-6">
                <div>
                    <label class="block text-sm font-medium text-text-dim mb-2">Small (sm)</label>
                    <TextArea size="sm" placeholder="Small size textarea..." :autoResize="args.autoResize" />
                </div>
                <div>
                    <label class="block text-sm font-medium text-text-dim mb-2">Medium (md) - Default</label>
                    <TextArea size="md" placeholder="Medium size textarea..." :autoResize="args.autoResize" />
                </div>
                <div>
                    <label class="block text-sm font-medium text-text-dim mb-2">Large (lg)</label>
                    <TextArea size="lg" placeholder="Large size textarea..." :autoResize="args.autoResize" />
                </div>
            </div>
        `,
    }),
    args: {
        autoResize: true,
    },
}

export const AutoResizeDemo: Story = {
    render: (args) => ({
        components: {TextArea},
        setup() {
            return {args}
        },
        template: `
            <div class="p-8 space-y-6">
                <div>
                    <label class="block text-sm font-medium text-text-dim mb-2">Auto-resize enabled (default)</label>
                    <TextArea
                        placeholder="Start typing to see the textarea grow..."
                        :autoResize="true"
                        :size="args.size"
                    />
                    <p class="mt-2 text-xs text-text-dim">Type multiple lines to see the textarea grow automatically (max height: 400px)</p>
                </div>
                <div>
                    <label class="block text-sm font-medium text-text-dim mb-2">Auto-resize disabled</label>
                    <TextArea
                        placeholder="This textarea has fixed height and can be manually resized"
                        :autoResize="false"
                        :size="args.size"
                    />
                    <p class="mt-2 text-xs text-text-dim">Manual resize enabled (drag corner)</p>
                </div>
            </div>
        `,
    }),
    args: {
        size: 'md',
    },
}
