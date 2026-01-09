import AuthorBio from '../src/components/vue/blog/AuthorBio.vue'
import type { Meta, StoryObj } from '@storybook/vue3'

const meta: Meta<typeof AuthorBio> = {
  title: 'Blog/AuthorBio',
  component: AuthorBio,
  tags: ['autodocs'],
  parameters: {
    docs: {
      description: {
        component: 'Author bio component for displaying author information at the end of blog posts.'
      }
    }
  }
}
export default meta

type Story = StoryObj<typeof meta>

export const WithAvatar: Story = {
  render: (args) => ({
    components: { AuthorBio },
    setup() {
      return { args }
    },
    template: '<AuthorBio v-bind="args" />'
  }),
  args: {
    name: 'Sarah Johnson',
    role: 'Senior AI Engineer',
    bio: 'Sarah is a passionate AI engineer with over 10 years of experience in machine learning and natural language processing. She loves building intelligent systems that make a real difference.',
    avatar: 'https://i.pravatar.cc/150?img=5',
    social: {
      twitter: 'https://twitter.com/sarahjohnson',
      github: 'https://github.com/sarahjohnson',
      linkedin: 'https://linkedin.com/in/sarahjohnson'
    }
  }
}

export const WithoutAvatar: Story = {
  render: (args) => ({
    components: { AuthorBio },
    setup() {
      return { args }
    },
    template: '<AuthorBio v-bind="args" />'
  }),
  args: {
    name: 'Alex Chen',
    role: 'Product Manager',
    bio: 'Alex leads product development at Open Ticket AI, focusing on creating intuitive and powerful automation tools for support teams.',
    social: {
      twitter: 'https://twitter.com/alexchen',
      linkedin: 'https://linkedin.com/in/alexchen'
    }
  }
}

export const WithoutRole: Story = {
  render: (args) => ({
    components: { AuthorBio },
    setup() {
      return { args }
    },
    template: '<AuthorBio v-bind="args" />'
  }),
  args: {
    name: 'Jamie Lee',
    bio: 'Tech enthusiast and writer passionate about AI, automation, and the future of customer support.',
    avatar: 'https://i.pravatar.cc/150?img=12',
    social: {
      twitter: 'https://twitter.com/jamielee'
    }
  }
}

export const MinimalSocial: Story = {
  render: (args) => ({
    components: { AuthorBio },
    setup() {
      return { args }
    },
    template: '<AuthorBio v-bind="args" />'
  }),
  args: {
    name: 'Morgan Taylor',
    role: 'Technical Writer',
    bio: 'Morgan creates documentation and tutorials that help developers get the most out of Open Ticket AI.',
    social: {
      github: 'https://github.com/morgantaylor'
    }
  }
}
