import LiteFreeDetail from '../src/components/vue/product/LiteFreeDetail.vue';
import type { Meta, StoryObj } from '@storybook/vue3';

const meta: Meta<typeof LiteFreeDetail> = {
  title: 'Product/LiteFreeDetail',
  component: LiteFreeDetail,
  parameters: {
    layout: 'fullscreen',
    docs: {
      description: {
        component: 'Complete product detail page for Tagging AI Lite Free, featuring interactive examples and taxonomy display.'
      }
    },
    backgrounds: { default: 'dark' }
  }
};

export default meta;
type Story = StoryObj<typeof meta>;

export const Default: Story = {
  render: () => ({
    components: { LiteFreeDetail },
    template: '<LiteFreeDetail />'
  })
};
