import Alert from '../src/components/vue/core/Alert.vue'
import type { Meta, StoryObj } from '@storybook/vue3'

const meta: Meta<typeof Alert> = {
  title: 'Docs/Alert',
  component: Alert,
  tags: ['autodocs'],
  argTypes: {
    type: {
      control: { type: 'select' },
      options: ['info', 'success', 'warning', 'danger', 'tip']
    },
    variant: {
      control: { type: 'select' },
      options: ['default', 'inline']
    }
  },
  parameters: {
    docs: {
      description: {
        component: 'Alert component for displaying important information, warnings, tips, and other messages in documentation. Supports default and inline variants, with optional footer slot.'
      }
    }
  }
}
export default meta

type Story = StoryObj<typeof meta>

export const Info: Story = {
  render: (args) => ({
    components: { Alert },
    setup() {
      return { args }
    },
    template: '<Alert v-bind="args">This is an informational message that provides helpful context to the reader.</Alert>'
  }),
  args: {
    type: 'info',
    title: 'Information'
  }
}

export const Success: Story = {
  render: (args) => ({
    components: { Alert },
    setup() {
      return { args }
    },
    template: '<Alert v-bind="args">Your operation completed successfully!</Alert>'
  }),
  args: {
    type: 'success',
    title: 'Success'
  }
}

export const Warning: Story = {
  render: (args) => ({
    components: { Alert },
    setup() {
      return { args }
    },
    template: '<Alert v-bind="args">Please be careful when performing this operation.</Alert>'
  }),
  args: {
    type: 'warning',
    title: 'Warning'
  }
}

export const Danger: Story = {
  render: (args) => ({
    components: { Alert },
    setup() {
      return { args }
    },
    template: '<Alert v-bind="args">This action cannot be undone. Proceed with caution.</Alert>'
  }),
  args: {
    type: 'danger',
    title: 'Danger'
  }
}

export const Tip: Story = {
  render: (args) => ({
    components: { Alert },
    setup() {
      return { args }
    },
    template: '<Alert v-bind="args">You can use keyboard shortcuts to navigate faster!</Alert>'
  }),
  args: {
    type: 'tip',
    title: 'Pro Tip'
  }
}

export const WithoutIcon: Story = {
  render: (args) => ({
    components: { Alert },
    setup() {
      return { args }
    },
    template: '<Alert v-bind="args">This alert has no icon displayed.</Alert>'
  }),
  args: {
    type: 'info',
    hideIcon: true
  }
}

export const WithoutTitle: Story = {
  render: (args) => ({
    components: { Alert },
    setup() {
      return { args }
    },
    template: '<Alert v-bind="args">This is an alert without a title, just the content.</Alert>'
  }),
  args: {
    type: 'tip'
  }
}

export const LongContent: Story = {
  render: (args) => ({
    components: { Alert },
    setup() {
      return { args }
    },
    template: `
      <Alert v-bind="args">
        <p class="mb-2">This alert contains multiple paragraphs of content to demonstrate how it handles longer text.</p>
        <p class="mb-2">You can include any HTML content within the alert component, making it very flexible for different use cases.</p>
        <ul class="list-disc pl-5 space-y-1">
          <li>Support for rich content</li>
          <li>Lists and formatting</li>
          <li>Multiple paragraphs</li>
        </ul>
      </Alert>
    `
  }),
  args: {
    type: 'info',
    title: 'Detailed Information'
  }
}

export const WithFooter: Story = {
  render: (args) => ({
    components: { Alert },
    setup() {
      return { args }
    },
    template: `
      <Alert v-bind="args">
        This is an alert with a footer section that can contain actions or additional information.
        <template #footer>
          <div class="flex gap-3 text-sm">
            <button class="text-info hover:text-info/80 font-medium">Learn more</button>
            <button class="text-gray-400 hover:text-gray-300">Dismiss</button>
          </div>
        </template>
      </Alert>
    `
  }),
  args: {
    type: 'info',
    title: 'Alert with Footer'
  }
}

export const InlineVariant: Story = {
  render: (args) => ({
    components: { Alert },
    setup() {
      return { args }
    },
    template: '<Alert v-bind="args">This is a subtle inline alert without a border, perfect for less prominent notifications.</Alert>'
  }),
  args: {
    type: 'tip',
    variant: 'inline',
    title: 'Inline Alert'
  }
}

export const InlineSuccess: Story = {
  render: (args) => ({
    components: { Alert },
    setup() {
      return { args }
    },
    template: '<Alert v-bind="args">Configuration saved successfully!</Alert>'
  }),
  args: {
    type: 'success',
    variant: 'inline'
  }
}

export const InlineWarning: Story = {
  render: (args) => ({
    components: { Alert },
    setup() {
      return { args }
    },
    template: '<Alert v-bind="args">This feature is deprecated and will be removed in the next version.</Alert>'
  }),
  args: {
    type: 'warning',
    variant: 'inline'
  }
}

export const SuccessWithFooter: Story = {
  render: (args) => ({
    components: { Alert },
    setup() {
      return { args }
    },
    template: `
      <Alert v-bind="args">
        Your changes have been successfully saved and are now live.
        <template #footer>
          <div class="flex gap-3 text-sm">
            <button class="text-success hover:text-success/80 font-medium">View changes</button>
            <button class="text-gray-400 hover:text-gray-300">OK</button>
          </div>
        </template>
      </Alert>
    `
  }),
  args: {
    type: 'success',
    title: 'Changes Saved'
  }
}

export const DangerWithFooter: Story = {
  render: (args) => ({
    components: { Alert },
    setup() {
      return { args }
    },
    template: `
      <Alert v-bind="args">
        This action will permanently delete all data and cannot be undone.
        <template #footer>
          <div class="flex gap-3 text-sm">
            <button class="text-danger hover:text-danger/80 font-medium">Delete anyway</button>
            <button class="text-gray-400 hover:text-gray-300">Cancel</button>
          </div>
        </template>
      </Alert>
    `
  }),
  args: {
    type: 'danger',
    title: 'Confirm Deletion'
  }
}
