import Accordion from '../src/components/vue/core/accordion/Accordion.vue';
import AccordionItem from '../src/components/vue/core/accordion/AccordionItem.vue';
import type { Meta, StoryObj } from '@storybook/vue3';
import { ref } from 'vue';

const VARIANTS = ['default', 'ghost', 'bordered', 'gradient'] as const;

const meta: Meta<typeof Accordion> = {
  title: 'Core/Accordion',
  component: Accordion,
  argTypes: {
    variant: {
      control: 'select',
      options: VARIANTS,
    },
    multiple: {
      control: 'boolean',
    },
  },
};
export default meta;

type Story = StoryObj<typeof meta>;

const sampleItems = [
  {
    id: 'ai-automation',
    title: 'AI-Powered Automation',
    content:
      "Automatically process and resolve tickets using advanced AI algorithms that learn from your team's patterns and improve over time.",
  },
  {
    id: 'smart-priority',
    title: 'Smart Prioritization',
    content:
      'Intelligent ticket routing and prioritization based on urgency, customer tier, and historical resolution patterns.',
  },
  {
    id: 'multi-channel',
    title: 'Multi-Channel Support',
    content:
      'Seamlessly integrate with email, chat, social media, and phone support across all your customer touchpoints.',
  },
];

const longSampleItems = [
  {
    id: 'getting-started',
    title: 'Getting Started',
    content:
      'Learn the basics of our platform with this comprehensive introduction to key features and workflows.',
  },
  {
    id: 'advanced-config',
    title: 'Advanced Configuration',
    content:
      'Deep dive into advanced settings, custom rules, and integration options to tailor the system to your needs.',
  },
  {
    id: 'api-integration',
    title: 'API Integration',
    content:
      'Connect your existing tools and services using our robust REST API with comprehensive documentation and examples.',
  },
  {
    id: 'security',
    title: 'Security & Compliance',
    content:
      'Understanding our security measures, data protection policies, and compliance certifications including GDPR and SOC 2.',
  },
  {
    id: 'troubleshooting',
    title: 'Troubleshooting',
    content:
      'Common issues and their solutions, along with tips for debugging and optimizing performance.',
  },
];

export const DefaultVariant: Story = {
  render: args => ({
    components: { Accordion },
    setup() {
      return { args };
    },
    template: `
            <div class="bg-surface-dark p-8 rounded-lg">
                <h3 class="text-white text-xl font-bold mb-4">Default Variant</h3>
                <Accordion v-bind="args" />
            </div>
        `,
  }),
  args: {
    items: sampleItems,
    variant: 'default',
  },
};

export const GhostVariant: Story = {
  render: args => ({
    components: { Accordion },
    setup() {
      return { args };
    },
    template: `
            <div class="bg-surface-dark p-8 rounded-lg">
                <h3 class="text-white text-xl font-bold mb-4">Ghost Variant</h3>
                <Accordion v-bind="args" />
            </div>
        `,
  }),
  args: {
    items: sampleItems,
    variant: 'ghost',
  },
};

export const BorderedVariant: Story = {
  render: args => ({
    components: { Accordion },
    setup() {
      return { args };
    },
    template: `
            <div class="bg-surface-dark p-8 rounded-lg">
                <h3 class="text-white text-xl font-bold mb-4">Bordered Variant</h3>
                <Accordion v-bind="args" />
            </div>
        `,
  }),
  args: {
    items: sampleItems,
    variant: 'bordered',
  },
};

export const GradientVariant: Story = {
  render: args => ({
    components: { Accordion },
    setup() {
      return { args };
    },
    template: `
            <div class="bg-surface-dark p-8 rounded-lg">
                <h3 class="text-white text-xl font-bold mb-4">Gradient Variant</h3>
                <Accordion v-bind="args" />
            </div>
        `,
  }),
  args: {
    items: sampleItems,
    variant: 'gradient',
  },
};

export const MultipleMode: Story = {
  render: args => ({
    components: { Accordion },
    setup() {
      return { args };
    },
    template: `
            <div class="bg-surface-dark p-8 rounded-lg">
                <h3 class="text-white text-xl font-bold mb-4">Multiple Mode</h3>
                <p class="text-text-dim text-sm mb-4">Multiple items can be open at the same time</p>
                <Accordion v-bind="args" />
            </div>
        `,
  }),
  args: {
    items: sampleItems.map((item, i) => ({
      ...item,
      defaultOpen: i === 0 || i === 1,
    })),
    variant: 'bordered',
    multiple: true,
  },
};

export const ItemsWithCustomSlots: Story = {
  render: args => ({
    components: { Accordion },
    setup() {
      return { args };
    },
    template: `
            <div class="bg-surface-dark p-8 rounded-lg">
                <h3 class="text-white text-xl font-bold mb-4">Items + Custom Title Slots</h3>
                <p class="text-text-dim text-sm mb-4">Using items prop with custom title rendering via slots</p>
                <Accordion v-bind="args" variant="bordered">
                    <template #title="{ item, index, open }">
                        <div class="flex items-center gap-3">
                            <div :class="[
                                'w-8 h-8 rounded-full flex items-center justify-center text-sm font-bold',
                                open ? 'bg-primary text-white' : 'bg-surface-lighter text-text-dim'
                            ]">
                                {{ index + 1 }}
                            </div>
                            <span class="font-semibold text-lg text-white">{{ item.title }}</span>
                        </div>
                    </template>
                </Accordion>
            </div>
        `,
  }),
  args: {
    items: sampleItems,
  },
};

export const ManualComposition: Story = {
  render: args => ({
    components: { Accordion, AccordionItem },
    setup() {
      return { args };
    },
    template: `
            <div class="bg-surface-dark p-8 rounded-lg">
                <h3 class="text-white text-xl font-bold mb-4">Manual Composition</h3>
                <p class="text-text-dim text-sm mb-4">Using AccordionItem components directly without items prop</p>
                <Accordion variant="bordered">
                    <AccordionItem id="custom-1" variant="bordered">
                        <template #title="{ open }">
                            <div class="flex items-center gap-3">
                                <svg class="w-6 h-6" :class="open ? 'text-primary' : 'text-text-dim'" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 10V3L4 14h7v7l9-11h-7z" />
                                </svg>
                                <span class="font-semibold text-lg text-white">Custom Icon & Title</span>
                            </div>
                        </template>
                        <div class="text-text-dim">
                            <p>Fully custom content with custom title slot including an icon.</p>
                        </div>
                    </AccordionItem>
                    
                    <AccordionItem id="custom-2" variant="bordered">
                        <template #title="{ open }">
                            <div class="flex items-center justify-between w-full pr-8">
                                <span class="font-semibold text-lg text-white">Rich Content Example</span>
                                <span :class="[
                                    'px-2 py-1 text-xs rounded-full',
                                    open ? 'bg-primary/20 text-primary' : 'bg-surface-lighter text-text-dim'
                                ]">
                                    {{ open ? 'Expanded' : 'Collapsed' }}
                                </span>
                            </div>
                        </template>
                        <div class="space-y-2 text-text-dim">
                            <p>You can include any Vue components or HTML in both the title and content slots.</p>
                            <ul class="list-disc list-inside space-y-1 ml-4">
                                <li>Custom layouts</li>
                                <li>Interactive elements</li>
                                <li>Complex data visualization</li>
                            </ul>
                        </div>
                    </AccordionItem>
                    
                    <AccordionItem id="custom-3" variant="bordered" :default-open="true">
                        <template #title>
                            <span class="font-semibold text-lg text-white">Opened by Default</span>
                        </template>
                        <div class="text-text-dim">
                            <p>This item is open by default using the defaultOpen prop.</p>
                        </div>
                    </AccordionItem>
                </Accordion>
            </div>
        `,
  }),
  args: {},
};

export const ControlledState: Story = {
  render: args => ({
    components: { Accordion },
    setup() {
      const openItem = ref('smart-priority');
      return { args, openItem, sampleItems };
    },
    template: `
            <div class="bg-surface-dark p-8 rounded-lg space-y-4">
                <h3 class="text-white text-xl font-bold mb-4">Controlled State (v-model)</h3>
                <p class="text-text-dim text-sm mb-4">Open item controlled by parent component</p>
                
                <div class="flex gap-2 mb-4">
                    <button 
                        v-for="item in sampleItems"
                        :key="item.id"
                        @click="openItem = item.id"
                        :class="[
                            'px-3 py-1.5 text-sm rounded-lg transition-colors',
                            openItem === item.id 
                                ? 'bg-primary text-white' 
                                : 'bg-surface-lighter text-text-dim hover:bg-surface-dark'
                        ]"
                    >
                        {{ item.title }}
                    </button>
                    <button 
                        @click="openItem = ''"
                        :class="[
                            'px-3 py-1.5 text-sm rounded-lg transition-colors',
                            openItem === '' 
                                ? 'bg-primary text-white' 
                                : 'bg-surface-lighter text-text-dim hover:bg-surface-dark'
                        ]"
                    >
                        Close All
                    </button>
                </div>
                
                <Accordion 
                    :items="sampleItems" 
                    variant="gradient"
                    v-model="openItem"
                />
                
                <p class="text-text-dim text-sm mt-4">Current open item: <code class="bg-surface-lighter px-2 py-1 rounded">{{ openItem || 'none' }}</code></p>
            </div>
        `,
  }),
  args: {},
};

export const StandaloneItem: Story = {
  render: args => ({
    components: { AccordionItem },
    setup() {
      return { args };
    },
    template: `
            <div class="bg-surface-dark p-8 rounded-lg space-y-4">
                <h3 class="text-white text-xl font-bold mb-4">Standalone AccordionItem Examples</h3>
                
                <div>
                    <h4 class="text-white text-sm font-semibold mb-2">Default</h4>
                    <AccordionItem id="standalone-default" title="Click to expand" variant="default">
                        <p class="text-gray-400">This is a standalone accordion item with default styling.</p>
                    </AccordionItem>
                </div>
                
                <div>
                    <h4 class="text-white text-sm font-semibold mb-2">Bordered</h4>
                    <AccordionItem id="standalone-bordered" title="Bordered item" variant="bordered">
                        <p class="text-gray-400">This accordion item has a border and rounded corners.</p>
                    </AccordionItem>
                </div>
                
                <div>
                    <h4 class="text-white text-sm font-semibold mb-2">Gradient</h4>
                    <AccordionItem id="standalone-gradient" title="Gradient item" variant="gradient" :default-open="true">
                        <p class="text-gray-400">This accordion item has a gradient background and is open by default.</p>
                    </AccordionItem>
                </div>
            </div>
        `,
  }),
  args: {},
};

export const AllVariantsShowcase: Story = {
  render: args => ({
    components: { Accordion },
    setup() {
      return { args, longSampleItems };
    },
    template: `
            <div class="bg-background-dark p-8 space-y-8">
                <div class="bg-surface-dark p-8 rounded-lg">
                    <h3 class="text-white text-2xl font-bold mb-2">Default Variant</h3>
                    <p class="text-text-dim text-sm mb-6">Clean dividers, minimal styling</p>
                    <Accordion :items="longSampleItems" variant="default" />
                </div>
                
                <div class="bg-surface-dark p-8 rounded-lg">
                    <h3 class="text-white text-2xl font-bold mb-2">Ghost Variant</h3>
                    <p class="text-text-dim text-sm mb-6">Subtle, minimal spacing</p>
                    <Accordion :items="longSampleItems" variant="ghost" />
                </div>
                
                <div class="bg-surface-dark p-8 rounded-lg">
                    <h3 class="text-white text-2xl font-bold mb-2">Bordered Variant</h3>
                    <p class="text-text-dim text-sm mb-6">Individual cards with borders</p>
                    <Accordion :items="longSampleItems" variant="bordered" />
                </div>
                
                <div class="bg-surface-dark p-8 rounded-lg">
                    <h3 class="text-white text-2xl font-bold mb-2">Gradient Variant</h3>
                    <p class="text-text-dim text-sm mb-6">Premium look with gradient backgrounds</p>
                    <Accordion :items="longSampleItems" variant="gradient" />
                </div>
            </div>
        `,
  }),
  args: {},
};
