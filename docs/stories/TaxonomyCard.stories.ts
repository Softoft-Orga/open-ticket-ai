import TaxonomyCard from '../src/components/vue/product/TaxonomyCard.vue';
import type { Meta, StoryObj } from '@storybook/vue3';

const meta: Meta<typeof TaxonomyCard> = {
  title: 'Product/TaxonomyCard',
  component: TaxonomyCard,
  argTypes: {
    title: {
      control: 'text',
      description: 'Taxonomy category title'
    },
    desc: {
      control: 'text',
      description: 'Short description of the category'
    },
    items: {
      control: 'object',
      description: 'Array of taxonomy items'
    }
  },
  parameters: {
    docs: {
      description: {
        component: 'Taxonomy category card displaying a title, description, and list of items. Built using the Card component with Tailwind design tokens.'
      }
    },
    backgrounds: { default: 'dark' }
  }
};

export default meta;
type Story = StoryObj<typeof meta>;

export const Industry: Story = {
  render: (args) => ({
    components: { TaxonomyCard },
    setup() {
      return { args };
    },
    template: '<div class="p-8 max-w-md"><TaxonomyCard v-bind="args" /></div>'
  }),
  args: {
    title: 'INDUSTRY',
    desc: 'Domain of the customer\'s business',
    items: [
      'TECH_IT',
      'FINANCE_SERVICES',
      'CONSUMER_RETAIL',
      'PUBLIC_HEALTH',
      'INDUSTRIAL'
    ]
  }
};

export const Intent: Story = {
  render: (args) => ({
    components: { TaxonomyCard },
    setup() {
      return { args };
    },
    template: '<div class="p-8 max-w-md"><TaxonomyCard v-bind="args" /></div>'
  }),
  args: {
    title: 'INTENT',
    desc: 'What the user wants to achieve',
    items: [
      'INCIDENT',
      'SERVICE_REQUEST',
      'QUESTION',
      'COMPLAINT',
      'CHANGE_REQUEST'
    ]
  }
};

export const FailureSymptom: Story = {
  render: (args) => ({
    components: { TaxonomyCard },
    setup() {
      return { args };
    },
    template: '<div class="p-8 max-w-md"><TaxonomyCard v-bind="args" /></div>'
  }),
  args: {
    title: 'FAILURE SYMPTOM',
    desc: 'Manifestation of the problem',
    items: [
      'AVAILABILITY',
      'PERFORMANCE',
      'FUNCTIONALITY',
      'AUTHENTICATION',
      'INTEGRATION'
    ]
  }
};

export const Grid: Story = {
  render: () => ({
    components: { TaxonomyCard },
    template: `
      <div class="p-8">
        <div class="grid md:grid-cols-3 gap-6">
          <TaxonomyCard
            title="INDUSTRY"
            desc="Domain of the customer's business"
            :items="['TECH_IT', 'FINANCE_SERVICES', 'CONSUMER_RETAIL']"
          />
          <TaxonomyCard
            title="INTENT"
            desc="What the user wants to achieve"
            :items="['INCIDENT', 'SERVICE_REQUEST', 'QUESTION']"
          />
          <TaxonomyCard
            title="FAILURE SYMPTOM"
            desc="Manifestation of the problem"
            :items="['AVAILABILITY', 'PERFORMANCE', 'FUNCTIONALITY']"
          />
        </div>
      </div>
    `
  })
};
