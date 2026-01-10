// TextArea.stories.ts
import TextArea from '../src/components/vue/core/forms/TextArea.vue'
import type {Meta, StoryObj} from '@storybook/vue3'
import { ChatBubbleLeftRightIcon } from '@heroicons/vue/24/outline'

const meta: Meta<typeof TextArea> = {
    title: 'Core/Forms/TextArea',
    component: TextArea,
    argTypes: {
        modelValue: {control: 'text'},
        placeholder: {control: 'text'},
        disabled: {control: 'boolean'},
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
    },
}
