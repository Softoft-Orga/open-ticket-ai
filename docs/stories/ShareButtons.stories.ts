import ShareButtons from '../src/components/vue/blog/ShareButtons.vue'
import type { Meta, StoryObj } from '@storybook/vue3'

const meta: Meta<typeof ShareButtons> = {
  title: 'Blog/ShareButtons',
  component: ShareButtons,
  tags: ['autodocs'],
  parameters: {
    docs: {
      description: {
        component: 'Share buttons component for enabling readers to share blog posts on social media or copy the link.'
      }
    }
  }
}
export default meta

type Story = StoryObj<typeof meta>

export const Default: Story = {
  render: (args) => ({
    components: { ShareButtons },
    setup() {
      return { args }
    },
    template: '<ShareButtons v-bind="args" />'
  }),
  args: {
    title: 'How to Build AI-Powered Support Automation',
    url: 'https://openticketai.com/blog/ai-support-automation'
  }
}

export const WithCurrentUrl: Story = {
  render: (args) => ({
    components: { ShareButtons },
    setup() {
      return { args }
    },
    template: '<ShareButtons v-bind="args" />'
  }),
  args: {
    title: 'The Future of Customer Support'
  }
}
