import Tabs from '../src/components/vue/core/basic/Tabs.vue';
import { ref } from 'vue';
import type { Meta, StoryObj } from '@storybook/vue3';
import { TONES, SIZES } from '../src/components/vue/core/design-system/tokens.ts';

const TAB_STYLES = ['underline', 'pill'] as const;

const meta: Meta<typeof Tabs> = {
  title: 'Core/Tabs',
  component: Tabs,
  argTypes: {
    style: {
      control: 'select',
      options: TAB_STYLES,
    },
    tone: {
      control: 'select',
      options: TONES,
    },
    size: {
      control: 'select',
      options: SIZES,
    },
    vertical: {
      control: 'boolean',
    },
  },
  parameters: {
    backgrounds: {
      default: 'dark',
      values: [{ name: 'dark', value: '#0b1220' }],
    },
  },
};
export default meta;

type Story = StoryObj<typeof meta>;

export const Default: Story = {
  render: args => ({
    components: { Tabs },
    setup() {
      return { args };
    },
    template: `
    <div class="p-8 bg-background-dark min-h-[400px]">
      <Tabs v-bind="args">
        <template #tab-0>
          <div class="p-4 text-gray-300">
            <h3 class="text-lg font-semibold mb-2">First Tab Content</h3>
            <p>This is the content for the first tab. The default style is underline with tone-based selection indicator.</p>
          </div>
        </template>
        <template #tab-1>
          <div class="p-4 text-gray-300">
            <h3 class="text-lg font-semibold mb-2">Second Tab Content</h3>
            <p>Navigate between tabs using mouse clicks or keyboard (Arrow keys, Home, End).</p>
          </div>
        </template>
        <template #tab-2>
          <div class="p-4 text-gray-300">
            <h3 class="text-lg font-semibold mb-2">Third Tab Content</h3>
            <p>The component is fully accessible with proper ARIA attributes.</p>
          </div>
        </template>
      </Tabs>
    </div>`,
  }),
  args: {
    tabs: ['Overview', 'Features', 'Documentation'],
    style: 'underline',
    tone: 'primary',
    size: 'md',
  },
};

export const Pills: Story = {
  render: args => ({
    components: { Tabs },
    setup() {
      return { args };
    },
    template: `
    <div class="p-8 bg-background-dark min-h-[400px]">
      <Tabs v-bind="args">
        <template #tab-0>
          <div class="p-4 text-gray-300">
            <h3 class="text-lg font-semibold mb-2">Dashboard</h3>
            <p>Pill-style tabs with a background container.</p>
          </div>
        </template>
        <template #tab-1>
          <div class="p-4 text-gray-300">
            <h3 class="text-lg font-semibold mb-2">Analytics</h3>
            <p>Perfect for settings panels or segmented controls.</p>
          </div>
        </template>
        <template #tab-2>
          <div class="p-4 text-gray-300">
            <h3 class="text-lg font-semibold mb-2">Reports</h3>
            <p>The pill variant provides a modern, rounded appearance.</p>
          </div>
        </template>
      </Tabs>
    </div>`,
  }),
  args: {
    tabs: ['Dashboard', 'Analytics', 'Reports'],
    style: 'pill',
    tone: 'primary',
    size: 'md',
  },
};

export const Sizes: Story = {
  render: args => ({
    components: { Tabs },
    setup() {
      return { args };
    },
    template: `
    <div class="p-8 bg-background-dark space-y-8">
      <div>
        <h3 class="text-white mb-4">Small Size</h3>
        <Tabs :tabs="args.tabs" size="sm" style="pill" tone="primary">
          <template #tab-0><div class="p-2 text-gray-300">Small tab content</div></template>
          <template #tab-1><div class="p-2 text-gray-300">Small tab content</div></template>
          <template #tab-2><div class="p-2 text-gray-300">Small tab content</div></template>
        </Tabs>
      </div>
      <div>
        <h3 class="text-white mb-4">Medium Size (Default)</h3>
        <Tabs :tabs="args.tabs" size="md" style="pill" tone="primary">
          <template #tab-0><div class="p-4 text-gray-300">Medium tab content</div></template>
          <template #tab-1><div class="p-4 text-gray-300">Medium tab content</div></template>
          <template #tab-2><div class="p-4 text-gray-300">Medium tab content</div></template>
        </Tabs>
      </div>
      <div>
        <h3 class="text-white mb-4">Large Size</h3>
        <Tabs :tabs="args.tabs" size="lg" style="pill" tone="primary">
          <template #tab-0><div class="p-6 text-gray-300">Large tab content</div></template>
          <template #tab-1><div class="p-6 text-gray-300">Large tab content</div></template>
          <template #tab-2><div class="p-6 text-gray-300">Large tab content</div></template>
        </Tabs>
      </div>
    </div>`,
  }),
  args: {
    tabs: ['Tab 1', 'Tab 2', 'Tab 3'],
  },
};

export const Tones: Story = {
  render: () => ({
    components: { Tabs },
    template: `
    <div class="p-8 bg-background-dark space-y-8">
      <div>
        <h3 class="text-white mb-4">Primary Tone</h3>
        <Tabs :tabs="['First', 'Second', 'Third']" style="pill" tone="primary">
          <template #tab-0><div class="p-4 text-gray-300">Primary tone selected</div></template>
          <template #tab-1><div class="p-4 text-gray-300">Content</div></template>
          <template #tab-2><div class="p-4 text-gray-300">Content</div></template>
        </Tabs>
      </div>
      <div>
        <h3 class="text-white mb-4">Success Tone</h3>
        <Tabs :tabs="['First', 'Second', 'Third']" style="pill" tone="success">
          <template #tab-0><div class="p-4 text-gray-300">Success tone selected</div></template>
          <template #tab-1><div class="p-4 text-gray-300">Content</div></template>
          <template #tab-2><div class="p-4 text-gray-300">Content</div></template>
        </Tabs>
      </div>
      <div>
        <h3 class="text-white mb-4">Warning Tone</h3>
        <Tabs :tabs="['First', 'Second', 'Third']" style="pill" tone="warning">
          <template #tab-0><div class="p-4 text-gray-300">Warning tone selected</div></template>
          <template #tab-1><div class="p-4 text-gray-300">Content</div></template>
          <template #tab-2><div class="p-4 text-gray-300">Content</div></template>
        </Tabs>
      </div>
    </div>`,
  }),
};

export const Vertical: Story = {
  render: args => ({
    components: { Tabs },
    setup() {
      return { args };
    },
    template: `
    <div class="p-8 bg-background-dark min-h-[400px]">
      <Tabs v-bind="args">
        <template #tab-0>
          <div class="p-6 text-gray-300 bg-surface-dark rounded-xl">
            <h3 class="text-lg font-semibold mb-2">General Settings</h3>
            <p>Vertical tabs are ideal for sidebar navigation or settings panels.</p>
            <p class="mt-2">They provide more space for longer tab labels.</p>
          </div>
        </template>
        <template #tab-1>
          <div class="p-6 text-gray-300 bg-surface-dark rounded-xl">
            <h3 class="text-lg font-semibold mb-2">Security Settings</h3>
            <p>Configure your security preferences here.</p>
            <p class="mt-2">Perfect for complex settings interfaces.</p>
          </div>
        </template>
        <template #tab-2>
          <div class="p-6 text-gray-300 bg-surface-dark rounded-xl">
            <h3 class="text-lg font-semibold mb-2">Privacy Settings</h3>
            <p>Manage your privacy and data settings.</p>
            <p class="mt-2">The vertical layout provides a clean, organized appearance.</p>
          </div>
        </template>
        <template #tab-3>
          <div class="p-6 text-gray-300 bg-surface-dark rounded-xl">
            <h3 class="text-lg font-semibold mb-2">Notifications</h3>
            <p>Control how and when you receive notifications.</p>
          </div>
        </template>
      </Tabs>
    </div>`,
  }),
  args: {
    tabs: ['General', 'Security', 'Privacy', 'Notifications'],
    vertical: true,
    style: 'pill',
    tone: 'primary',
    size: 'md',
  },
};

export const WithVModel: Story = {
  render: args => ({
    components: { Tabs },
    setup() {
      const activeTab = ref(1);
      return { args, activeTab };
    },
    template: `
    <div class="p-8 bg-background-dark min-h-[400px]">
      <div class="mb-4 p-3 bg-surface-dark rounded-lg">
        <p class="text-sm text-gray-300">
          Active tab index: <span class="text-primary font-semibold">{{ activeTab }}</span>
        </p>
      </div>
      <Tabs v-bind="args" v-model="activeTab">
        <template #tab-0>
          <div class="p-4 text-gray-300">
            <h3 class="text-lg font-semibold mb-2">Tab A</h3>
            <p>Using v-model for two-way binding with external state.</p>
          </div>
        </template>
        <template #tab-1>
          <div class="p-4 text-gray-300">
            <h3 class="text-lg font-semibold mb-2">Tab B (Initially Active)</h3>
            <p>The active tab is controlled by the parent component.</p>
          </div>
        </template>
        <template #tab-2>
          <div class="p-4 text-gray-300">
            <h3 class="text-lg font-semibold mb-2">Tab C</h3>
            <p>You can programmatically control which tab is active.</p>
          </div>
        </template>
      </Tabs>
      <div class="mt-6 flex gap-2">
        <button
          @click="activeTab = 0"
          class="px-4 py-2 bg-primary text-white rounded-lg hover:bg-primary-dark transition"
        >
          Go to Tab A
        </button>
        <button
          @click="activeTab = 1"
          class="px-4 py-2 bg-primary text-white rounded-lg hover:bg-primary-dark transition"
        >
          Go to Tab B
        </button>
        <button
          @click="activeTab = 2"
          class="px-4 py-2 bg-primary text-white rounded-lg hover:bg-primary-dark transition"
        >
          Go to Tab C
        </button>
      </div>
    </div>`,
  }),
  args: {
    tabs: ['Tab A', 'Tab B', 'Tab C'],
    style: 'pill',
    tone: 'primary',
    size: 'md',
  },
};
