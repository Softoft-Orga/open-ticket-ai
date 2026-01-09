import TagFilter from '../src/components/vue/blog/TagFilter.vue'
import type { Meta, StoryObj } from '@storybook/vue3'

const meta: Meta<typeof TagFilter> = {
  title: 'Blog/TagFilter',
  component: TagFilter,
  tags: ['autodocs'],
  parameters: {
    docs: {
      description: {
        component: 'Tag filter component for filtering blog posts by categories or topics.'
      }
    }
  }
}
export default meta

type Story = StoryObj<typeof meta>

export const Default: Story = {
  render: (args) => ({
    components: { TagFilter },
    setup() {
      return { args }
    },
    template: '<TagFilter v-bind="args" />'
  }),
  args: {
    tags: ['AI/ML', 'Automation', 'Support', 'Engineering', 'Product Updates']
  }
}

export const WithPreselected: Story = {
  render: (args) => ({
    components: { TagFilter },
    setup() {
      return { args }
    },
    template: '<TagFilter v-bind="args" />'
  }),
  args: {
    tags: ['AI/ML', 'Automation', 'Support', 'Engineering', 'Product Updates'],
    modelValue: ['AI/ML', 'Automation']
  }
}

export const ManyTags: Story = {
  render: (args) => ({
    components: { TagFilter },
    setup() {
      return { args }
    },
    template: '<TagFilter v-bind="args" />'
  }),
  args: {
    tags: [
      'AI/ML',
      'Automation',
      'Support',
      'Engineering',
      'Product Updates',
      'Security',
      'API',
      'Integration',
      'Best Practices',
      'Case Studies'
    ]
  }
}

export const FewTags: Story = {
  render: (args) => ({
    components: { TagFilter },
    setup() {
      return { args }
    },
    template: '<TagFilter v-bind="args" />'
  }),
  args: {
    tags: ['Tutorial', 'News', 'Guide']
  }
}
