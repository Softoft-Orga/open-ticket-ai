import type { Meta, StoryObj } from '@storybook/vue3';
import FeatureShowcase from '../src/components/vue/homepage/FeatureShowcase.vue';

const meta = {
  title: 'Homepage/FeatureShowcase',
  component: FeatureShowcase,
  tags: ['autodocs'],
  argTypes: {
    badge: { control: 'text' },
    title: { control: 'text' },
    description: { control: 'text' },
    ctaText: { control: 'text' },
    imageSrc: { control: 'text' },
    imageAlt: { control: 'text' }
  },
} satisfies Meta<typeof FeatureShowcase>;

export default meta;
type Story = StoryObj<typeof meta>;

export const TaggingAI: Story = {
  args: {
    badge: 'Core Engine',
    title: 'Tagging AI',
    description: 'Hierarchical, multilingual ticket classification that stays on your server.',
    features: [
      {
        title: '100% On-Premise Execution',
        description: 'Ticket data processed locally'
      },
      {
        title: 'Multi-language Support',
        description: 'EN, DE, FR, etc.'
      },
      {
        title: 'Custom Hierarchical Taxonomies',
        description: 'Handling complex nested tags and multiple languages with enterprise-grade precision'
      }
    ],
    ctaText: 'Learn More'
  },
};

export const WithImage: Story = {
  args: {
    badge: 'Featured',
    title: 'Open Ticket Automation',
    description: 'Drive workflows based on AI-generated tags without writing code. Connect to your helpdesk and automate routing, prioritization, and responses.',
    features: [
      {
        title: 'Routing & Escalation',
        description: 'Automatic ticket assignment based on tags'
      },
      {
        title: 'Field updates, templates, triggers',
        description: 'Configure actions without coding'
      },
      {
        title: 'Escalation and notification rules',
        description: 'Define complex workflows visually'
      }
    ],
    ctaText: 'Explore Workflows'
  },
};

export const NoBadge: Story = {
  args: {
    title: 'Enterprise Security',
    description: 'Built for organizations with strict data governance requirements. All processing happens on your infrastructure.',
    features: [
      {
        title: 'Zero Cloud Dependencies'
      },
      {
        title: 'Full Audit Logging'
      },
      {
        title: 'Role-Based Access Control'
      }
    ]
  },
};
