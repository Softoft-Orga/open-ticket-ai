import FooterComponent from '../src/components/vue/core/navigation/FooterComponent.vue';
import type { Meta, StoryObj } from '@storybook/vue3';

const meta: Meta<typeof FooterComponent> = {
  title: 'Navigation/FooterComponent',
  component: FooterComponent,
  parameters: {
    layout: 'fullscreen',
    backgrounds: {
      default: 'dark',
      values: [{ name: 'dark', value: '#0f0814' }],
    },
  },
};
export default meta;

type Story = StoryObj<typeof meta>;

export const Default: Story = {
  args: {
    footerData: {
      brandName: 'Open Ticket AI',
      brandTagline: 'Intelligent automation for OTRS, Znuny, and Zammad. German Engineering.',
      socialHeading: 'Connect',
      sections: [
        {
          title: 'Product',
          links: [
            { label: 'Features', url: '/products' },
            { label: 'Integrations', url: '/services' },
            { label: 'Security', url: '/docs' },
          ],
        },
        {
          title: 'Company',
          links: [
            { label: 'About Us', url: '#' },
            { label: 'Careers', url: '#' },
            { label: 'Legal', url: '#' },
          ],
        },
      ],
      social: [
        {
          platform: 'github',
          url: 'https://github.com/openticketai',
          ariaLabel: 'GitHub',
        },
        {
          platform: 'linkedin',
          url: 'https://www.linkedin.com/company/open-ticket-ai',
          ariaLabel: 'LinkedIn',
        },
      ],
      copyright: 'Open Ticket AI UG. All rights reserved.',
    },
  },
  render: args => ({
    components: { FooterComponent },
    setup() {
      return { args };
    },
    template: '<FooterComponent v-bind="args" />',
  }),
};
