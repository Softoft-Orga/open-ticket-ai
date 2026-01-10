import type { Meta, StoryObj } from '@storybook/vue3';
import LiteProDetail from '../src/components/vue/product/LiteProDetail.vue';

const meta = {
  title: 'Product/LiteProDetail',
  component: LiteProDetail,
  tags: ['autodocs'],
  parameters: {
    layout: 'fullscreen',
    backgrounds: { default: 'dark' },
    docs: {
      description: {
        component: 'Product detail page for Tagging AI Lite Pro showing specifications, features, and comparison table. Uses shared Card, Badge, and Button components.'
      }
    }
  }
} satisfies Meta<typeof LiteProDetail>;

export default meta;
type Story = StoryObj<typeof meta>;

export const Default: Story = {
  render: () => ({
    components: { LiteProDetail },
    template: '<LiteProDetail />'
  })
};

export const Mobile: Story = {
  render: () => ({
    components: { LiteProDetail },
    template: '<LiteProDetail />'
  }),
  parameters: {
    viewport: {
      defaultViewport: 'mobile1'
    }
  }
};

export const Tablet: Story = {
  render: () => ({
    components: { LiteProDetail },
    template: '<LiteProDetail />'
  }),
  parameters: {
    viewport: {
      defaultViewport: 'tablet'
    }
  }
};
