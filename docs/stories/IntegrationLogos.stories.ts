import type { Meta, StoryObj } from '@storybook/vue3';
import IntegrationLogos from '../src/components/vue/homepage/IntegrationLogos.vue';

const meta = {
  title: 'Homepage/IntegrationLogos',
  component: IntegrationLogos,
  tags: ['autodocs'],
  argTypes: {
    title: { control: 'text' },
    moreText: { control: 'text' }
  },
} satisfies Meta<typeof IntegrationLogos>;

export default meta;
type Story = StoryObj<typeof meta>;

export const Default: Story = {
  args: {
    title: 'WORKS WITH',
    integrations: [
      { name: 'OTOBO' },
      { name: 'Znuny/OTRS' },
      { name: 'Zammad' }
    ],
    moreText: 'More on request'
  },
};

export const ManyIntegrations: Story = {
  args: {
    title: 'COMPATIBLE WITH',
    integrations: [
      { name: 'OTOBO' },
      { name: 'Znuny' },
      { name: 'OTRS' },
      { name: 'Zammad' },
      { name: 'Zendesk' },
      { name: 'ServiceNow' }
    ],
    moreText: 'And many more...'
  },
};

export const NoMoreText: Story = {
  args: {
    title: 'INTEGRATIONS',
    integrations: [
      { name: 'OTOBO' },
      { name: 'Znuny/OTRS' },
      { name: 'Zammad' }
    ]
  },
};
