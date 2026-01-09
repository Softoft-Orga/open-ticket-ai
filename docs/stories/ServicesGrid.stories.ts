import type { Meta, StoryObj } from '@storybook/vue3';
import ServicesGrid from '../src/components/vue/homepage/ServicesGrid.vue';

const meta = {
  title: 'Homepage/ServicesGrid',
  component: ServicesGrid,
  tags: ['autodocs'],
  argTypes: {
    title: { control: 'text' },
    subtitle: { control: 'text' }
  },
} satisfies Meta<typeof ServicesGrid>;

export default meta;
type Story = StoryObj<typeof meta>;

const sampleServices = [
  {
    slug: 'integration-standard-stack',
    title: 'Integration Package - Standard Stack',
    oneLiner: 'Standard Stack Integration',
    description: 'Fixed-price package to connect Open Ticket AI with OTOBO, Znuny (OTRS stack), or Zammad ticket systems. Includes technical setup and basic testing.',
    outcomes: [
      'Technical setup of Tagging AI service',
      'Connection to 1 ticket system instance',
      'Mapping tags to technical field logic'
    ],
    startingPrice: 2000,
    group: 'Integration'
  },
  {
    slug: 'ota-automation-pack',
    title: 'OTA Automation Pack',
    oneLiner: 'Implementation of 3 core automations',
    description: 'Open Ticket Automation (OTA) is our open-source layer that translates AI tags into concrete actions.',
    outcomes: [
      'Config of 3 automations based on your rules',
      'Testing with real ticket examples',
      'Handover documentation'
    ],
    startingPrice: 3000,
    group: 'Automation'
  },
  {
    slug: 'custom-model-training',
    title: 'Custom Model Training',
    oneLiner: 'Train AI models on your specific ticket data',
    description: 'Get AI models fine-tuned specifically for your organization\'s ticket patterns, categories, and workflows.',
    outcomes: [
      'Custom-trained classification models',
      'Improved accuracy for your specific use case',
      'Model performance benchmarking'
    ],
    startingPrice: 10000,
    group: 'Services'
  },
  {
    slug: 'consulting',
    title: 'AI Consulting Services',
    oneLiner: 'Strategic guidance for AI-powered support automation',
    description: 'Work with our AI experts to develop a comprehensive strategy for automating your support workflows.',
    outcomes: [
      'AI readiness assessment',
      'Custom automation strategy',
      'ROI analysis and projections'
    ],
    startingPrice: 3000,
    group: 'Services'
  },
  {
    slug: 'hourly-engineering',
    title: 'Hourly Engineering',
    oneLiner: 'Flexible engineering support',
    description: 'For extra changes beyond package scope, custom features/workflows, troubleshooting, and migrations.',
    outcomes: [
      'Custom feature development',
      'Workflow customization',
      'Troubleshooting support'
    ],
    startingPrice: 200,
    group: 'Flexible'
  },
  {
    slug: 'ongoing-support',
    title: 'Ongoing Support',
    oneLiner: 'Continuous system maintenance',
    description: 'Keep the system stable with updates, monitoring, and priority fixes.',
    outcomes: [
      'Updates and compatibility maintenance',
      'Monitoring and incident response service',
      'Monthly check-in and improvements'
    ],
    startingPrice: 2000,
    group: 'Support'
  }
];

export const Default: Story = {
  args: {
    title: 'Services that get you live fast',
    subtitle: 'Integration packages, automation setup, and custom development for your needs',
    services: sampleServices
  },
};

export const ThreeServices: Story = {
  args: {
    title: 'Our Core Services',
    subtitle: 'Everything you need to get started',
    services: sampleServices.slice(0, 3)
  },
};

export const CustomTitle: Story = {
  args: {
    title: 'Professional Services',
    subtitle: 'Expert support for your AI automation journey',
    services: sampleServices
  },
};
