import type { Meta, StoryObj } from '@storybook/vue3';
import ServiceCard from '../src/components/vue/homepage/ServiceCard.vue';

const meta = {
  title: 'Homepage/ServiceCard',
  component: ServiceCard,
  tags: ['autodocs'],
  argTypes: {
    title: { control: 'text' },
    oneLiner: { control: 'text' },
    description: { control: 'text' },
    startingPrice: { control: 'number' },
    group: { 
      control: 'select',
      options: ['Integration', 'Automation', 'Services', 'Flexible', 'Model Development', 'Support', 'Analytics']
    }
  },
} satisfies Meta<typeof ServiceCard>;

export default meta;
type Story = StoryObj<typeof meta>;

export const IntegrationPackage: Story = {
  args: {
    title: 'Integration Package - Standard Stack',
    oneLiner: 'Standard Stack Integration',
    description: 'Fixed-price package to connect Open Ticket AI with OTOBO, Znuny (OTRS stack), or Zammad ticket systems. Includes technical setup and basic testing.',
    outcomes: [
      'Technical setup of Tagging AI service',
      'Connection to 1 ticket system instance',
      'Mapping tags to technical field logic',
      'One trigger setup (e.g. on creation)',
      'Basic testing + handover'
    ],
    startingPrice: 2000,
    group: 'Integration'
  },
};

export const AutomationPack: Story = {
  args: {
    title: 'OTA Automation Pack',
    oneLiner: 'Implementation of 3 core automations',
    description: 'Open Ticket Automation (OTA) is our open-source layer that translates AI tags into concrete actions. This package includes configuration of 3 automations based on your rules, testing with real ticket examples, and handover documentation.',
    outcomes: [
      'Config of 3 automations based on your rules',
      'Testing with real ticket examples',
      'Handover documentation'
    ],
    startingPrice: 3000,
    group: 'Automation'
  },
};

export const CustomModel: Story = {
  args: {
    title: 'Custom Model Training',
    oneLiner: 'Train AI models on your specific ticket data',
    description: 'Get AI models fine-tuned specifically for your organization\'s ticket patterns, categories, and workflows. Our data scientists work with your historical data to create models that understand your unique business context.',
    outcomes: [
      'Custom-trained classification models',
      'Improved accuracy for your specific use case',
      'Model performance benchmarking',
      'Regular model updates and retraining',
      'Detailed accuracy reports'
    ],
    startingPrice: 10000,
    group: 'Services'
  },
};

export const HourlyEngineering: Story = {
  args: {
    title: 'Hourly Engineering',
    oneLiner: 'Flexible engineering support',
    description: 'For extra changes beyond package scope, custom features/workflows, troubleshooting, and migrations. Get expert engineering support on an as-needed basis.',
    outcomes: [
      'Custom feature development',
      'Workflow customization',
      'Troubleshooting support',
      'Migration assistance',
      'Technical consultation'
    ],
    startingPrice: 200,
    group: 'Flexible'
  },
};

export const NoPrice: Story = {
  args: {
    title: 'Custom Development',
    oneLiner: 'Special Requirements',
    description: 'Anything beyond tag-model creation: special architectures, constraints, on-prem performance targets, multilingual requirements, advanced-evaluation, long-term training programs.',
    outcomes: [
      'Special architectures and constraints',
      'On-prem performance optimization',
      'Advanced multilingual requirements',
      'Long-term training programs',
      'Custom evaluation frameworks'
    ],
    group: 'Model Development'
  },
};
