import RelatedPosts from '../src/components/vue/blog/RelatedPosts.vue'
import type { Meta, StoryObj } from '@storybook/vue3'

const meta: Meta<typeof RelatedPosts> = {
  title: 'Blog/RelatedPosts',
  component: RelatedPosts,
  tags: ['autodocs'],
  parameters: {
    docs: {
      description: {
        component: 'Related posts component for displaying relevant articles at the end of blog posts to encourage further reading.'
      }
    }
  }
}
export default meta

type Story = StoryObj<typeof meta>

const samplePosts = [
  {
    title: 'Getting Started with AI Ticket Classification',
    description: 'Learn how to implement AI-powered ticket classification in your support workflow.',
    category: 'Tutorial',
    date: 'Jan 5, 2024',
    image: 'https://picsum.photos/400/250?1',
    href: '/blog/ai-ticket-classification'
  },
  {
    title: 'Best Practices for Support Automation',
    description: 'Discover proven strategies for automating your customer support operations effectively.',
    category: 'Guide',
    date: 'Jan 3, 2024',
    image: 'https://picsum.photos/400/250?2',
    href: '/blog/support-automation-best-practices'
  },
  {
    title: 'Understanding Machine Learning Models',
    description: 'A deep dive into the ML models that power intelligent ticket routing and classification.',
    category: 'Technical',
    date: 'Dec 28, 2023',
    image: 'https://picsum.photos/400/250?3',
    href: '/blog/ml-models-explained'
  }
]

export const ThreePosts: Story = {
  render: (args) => ({
    components: { RelatedPosts },
    setup() {
      return { args }
    },
    template: '<RelatedPosts v-bind="args" />'
  }),
  args: {
    posts: samplePosts
  }
}

export const TwoPosts: Story = {
  render: (args) => ({
    components: { RelatedPosts },
    setup() {
      return { args }
    },
    template: '<RelatedPosts v-bind="args" />'
  }),
  args: {
    posts: samplePosts.slice(0, 2)
  }
}

export const WithoutImages: Story = {
  render: (args) => ({
    components: { RelatedPosts },
    setup() {
      return { args }
    },
    template: '<RelatedPosts v-bind="args" />'
  }),
  args: {
    posts: samplePosts.map(post => ({ ...post, image: undefined }))
  }
}
