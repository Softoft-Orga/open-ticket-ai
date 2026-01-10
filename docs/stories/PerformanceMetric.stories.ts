import PerformanceMetric from '../src/components/vue/product/PerformanceMetric.vue';
import type { Meta, StoryObj } from '@storybook/vue3';

const meta: Meta<typeof PerformanceMetric> = {
  title: 'Product/PerformanceMetric',
  component: PerformanceMetric,
  argTypes: {
    label: {
      control: 'text',
      description: 'Metric label (uppercase recommended)'
    },
    value: {
      control: 'text',
      description: 'Metric value'
    }
  },
  parameters: {
    docs: {
      description: {
        component: 'Performance metric display card with label and value.'
      }
    },
    backgrounds: { default: 'dark' }
  }
};

export default meta;
type Story = StoryObj<typeof meta>;

export const Default: Story = {
  render: (args) => ({
    components: { PerformanceMetric },
    setup() {
      return { args };
    },
    template: '<div class="p-8 max-w-xs"><PerformanceMetric v-bind="args" /></div>'
  }),
  args: {
    label: 'MODEL SIZE',
    value: '500M Params'
  }
};

export const VRAMRequirement: Story = {
  render: (args) => ({
    components: { PerformanceMetric },
    setup() {
      return { args };
    },
    template: '<div class="p-8 max-w-xs"><PerformanceMetric v-bind="args" /></div>'
  }),
  args: {
    label: 'VRAM REQUIREMENT',
    value: '<1GB'
  }
};

export const Accuracy: Story = {
  render: (args) => ({
    components: { PerformanceMetric },
    setup() {
      return { args };
    },
    template: '<div class="p-8 max-w-xs"><PerformanceMetric v-bind="args" /></div>'
  }),
  args: {
    label: 'AVERAGE ACCURACY',
    value: '~82%'
  }
};

export const Grid: Story = {
  render: () => ({
    components: { PerformanceMetric },
    template: `
      <div class="p-8">
        <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
          <PerformanceMetric label="MODEL SIZE" value="500M Params" />
          <PerformanceMetric label="VRAM REQUIREMENT" value="<1GB" />
          <PerformanceMetric label="AVERAGE ACCURACY" value="~82%" />
          <PerformanceMetric label="LANGUAGE SUPPORT" value="Global / Multilingual" />
        </div>
      </div>
    `
  })
};
