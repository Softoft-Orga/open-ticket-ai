import type { Meta, StoryObj } from '@storybook/vue3';
import PagefindSearch from '../src/components/vue/PagefindSearch.vue';

const meta: Meta<typeof PagefindSearch> = {
  title: 'Components/Docs/PagefindSearch',
  component: PagefindSearch,
  tags: ['autodocs'],
  parameters: {
    layout: 'padded',
    backgrounds: {
      default: 'dark',
      values: [
        { name: 'dark', value: '#0f0814' },
        { name: 'light', value: '#ffffff' },
      ],
    },
  },
  decorators: [
    () => ({
      template: `
        <div style="max-width: 800px; margin: 0 auto; padding: 2rem;">
          <story />
        </div>
      `,
    }),
  ],
};

export default meta;
type Story = StoryObj<typeof PagefindSearch>;

export const Default: Story = {
  render: () => ({
    components: { PagefindSearch },
    template: `
      <div class="space-y-4">
        <h2 class="text-2xl font-bold text-white mb-4">Search Documentation</h2>
        <PagefindSearch />
      </div>
    `,
  }),
};

export const WithContext: Story = {
  render: () => ({
    components: { PagefindSearch },
    template: `
      <div class="min-h-screen bg-background-dark py-24 relative overflow-hidden">
        <div class="absolute inset-0 pointer-events-none z-0">
          <div class="absolute -top-[10%] -left-[10%] w-1/2 h-1/2 bg-primary/5 rounded-full blur-[120px]"></div>
          <div class="absolute -bottom-[10%] -right-[10%] w-2/5 h-2/5 bg-purple-900/10 rounded-full blur-[120px]"></div>
        </div>
        
        <div class="relative z-10 max-w-7xl mx-auto px-6">
          <div class="text-center max-w-3xl mx-auto mb-20">
            <h2 class="text-5xl md:text-7xl font-black tracking-tight mb-6 bg-clip-text text-transparent bg-gradient-to-r from-white via-slate-200 to-slate-400">
              Documentation
            </h2>
            <p class="text-xl text-slate-400 max-w-2xl mx-auto leading-relaxed">
              Choose the documentation you need. Explore API references, implementation guides, and best practices.
            </p>
          </div>

          <div class="w-full max-w-2xl mx-auto mb-24 relative group">
            <div class="absolute -inset-1 bg-gradient-to-r from-primary/30 to-purple-600/30 rounded-2xl blur opacity-30 group-hover:opacity-60 transition duration-500"></div>
            <div class="relative">
              <PagefindSearch />
            </div>
          </div>
        </div>
      </div>
    `,
  }),
};

export const Mobile: Story = {
  parameters: {
    viewport: {
      defaultViewport: 'mobile1',
    },
  },
  render: () => ({
    components: { PagefindSearch },
    template: `
      <div class="space-y-4">
        <h2 class="text-xl font-bold text-white mb-4">Search (Mobile)</h2>
        <PagefindSearch />
      </div>
    `,
  }),
};
