import Alert from '../src/components/vue/docs/Alert.vue'
import type { Meta, StoryObj } from '@storybook/vue3'

const meta: Meta<typeof Alert> = {
  title: 'Docs/Alert',
  component: Alert,
  tags: ['autodocs'],
  argTypes: {
    type: {
      control: { type: 'select' },
      options: ['info', 'success', 'warning', 'danger', 'tip']
    }
  },
  parameters: {
    docs: {
      description: {
        component: 'Alert component for displaying important information, warnings, tips, and other messages in documentation.'
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
