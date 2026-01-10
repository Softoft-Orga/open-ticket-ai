import Tabs from '../src/components/vue/core/basic/Tabs.vue'
import {ref} from 'vue'
import type {Meta, StoryObj} from '@storybook/vue3'

const meta: Meta<typeof Tabs> = {
    title: 'Core/Tabs',
    component: Tabs,
    argTypes: {
        variant: {
            control: 'select',
            options: ['underline', 'pills', 'enclosed', 'ghost']
        },
        size: {
            control: 'select',
            options: ['sm', 'md', 'lg']
        },
        alignment: {
            control: 'select',
            options: ['start', 'center', 'end', 'stretch']
        },
        fullWidth: {
            control: 'boolean'
        },
        vertical: {
            control: 'boolean'
        },
        showIndicator: {
            control: 'boolean'
        },
        glowEffect: {
            control: 'boolean'
        }
    },
    parameters: {
        backgrounds: {
            default: 'dark',
            values: [
                { name: 'dark', value: '#0b1220' }
            ]
        }
    }
}
export default meta

type Story = StoryObj<typeof meta>

export const Default: Story = {
    render: (args) => ({
        components: {Tabs},
        setup() {
            return {args}
        },
        template: `
    <div class="p-8 bg-background-dark min-h-[400px]">
      <Tabs v-bind="args">
        <template #tab-0>
          <div class="p-4 text-gray-300">
            <h3 class="text-lg font-semibold mb-2">First Tab Content</h3>
            <p>This is the content for the first tab. The default variant is underline with a glowing purple indicator.</p>
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
    </div>`
    }),
    args: {
        tabs: ['Overview', 'Features', 'Documentation']
    }
}

export const Pills: Story = {
    render: (args) => ({
        components: {Tabs},
        setup() {
            return {args}
        },
        template: `
    <div class="p-8 bg-background-dark min-h-[400px]">
      <Tabs v-bind="args">
        <template #tab-0>
          <div class="p-4 text-gray-300">
            <h3 class="text-lg font-semibold mb-2">Dashboard</h3>
            <p>Pill-style tabs with a glowing effect on the active tab.</p>
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
            <p>The pills variant provides a modern, rounded appearance.</p>
          </div>
        </template>
      </Tabs>
    </div>`
    }),
    args: {
        tabs: ['Dashboard', 'Analytics', 'Reports'],
        variant: 'pills'
    }
}

export const Enclosed: Story = {
    render: (args) => ({
        components: {Tabs},
        setup() {
            return {args}
        },
        template: `
    <div class="p-8 bg-background-dark min-h-[400px]">
      <Tabs v-bind="args">
        <template #tab-0>
          <div class="text-gray-300">
            <h3 class="text-lg font-semibold mb-2">Settings</h3>
            <p>The enclosed variant creates a card-like appearance with borders.</p>
          </div>
        </template>
        <template #tab-1>
          <div class="text-gray-300">
            <h3 class="text-lg font-semibold mb-2">Profile</h3>
            <p>Content is seamlessly integrated within the bordered container.</p>
          </div>
        </template>
        <template #tab-2>
          <div class="text-gray-300">
            <h3 class="text-lg font-semibold mb-2">Notifications</h3>
            <p>Great for forms and structured content areas.</p>
          </div>
        </template>
      </Tabs>
    </div>`
    }),
    args: {
        tabs: ['Settings', 'Profile', 'Notifications'],
        variant: 'enclosed'
    }
}

export const Ghost: Story = {
    render: (args) => ({
        components: {Tabs},
        setup() {
            return {args}
        },
        template: `
    <div class="p-8 bg-background-dark min-h-[400px]">
      <Tabs v-bind="args">
        <template #tab-0>
          <div class="p-4 text-gray-300">
            <h3 class="text-lg font-semibold mb-2">Code</h3>
            <p>Ghost variant provides a subtle, minimal design.</p>
          </div>
        </template>
        <template #tab-1>
          <div class="p-4 text-gray-300">
            <h3 class="text-lg font-semibold mb-2">Preview</h3>
            <p>Perfect for code editors or minimalist interfaces.</p>
          </div>
        </template>
      </Tabs>
    </div>`
    }),
    args: {
        tabs: ['Code', 'Preview'],
        variant: 'ghost'
    }
}

export const Sizes: Story = {
    render: (args) => ({
        components: {Tabs},
        setup() {
            return {args}
        },
        template: `
    <div class="p-8 bg-background-dark space-y-8">
      <div>
        <h3 class="text-white mb-4">Small Size</h3>
        <Tabs :tabs="args.tabs" size="sm" variant="pills">
          <template #tab-0><div class="p-2 text-gray-300">Small tab content</div></template>
          <template #tab-1><div class="p-2 text-gray-300">Small tab content</div></template>
          <template #tab-2><div class="p-2 text-gray-300">Small tab content</div></template>
        </Tabs>
      </div>
      <div>
        <h3 class="text-white mb-4">Medium Size (Default)</h3>
        <Tabs :tabs="args.tabs" size="md" variant="pills">
          <template #tab-0><div class="p-4 text-gray-300">Medium tab content</div></template>
          <template #tab-1><div class="p-4 text-gray-300">Medium tab content</div></template>
          <template #tab-2><div class="p-4 text-gray-300">Medium tab content</div></template>
        </Tabs>
      </div>
      <div>
        <h3 class="text-white mb-4">Large Size</h3>
        <Tabs :tabs="args.tabs" size="lg" variant="pills">
          <template #tab-0><div class="p-6 text-gray-300">Large tab content</div></template>
          <template #tab-1><div class="p-6 text-gray-300">Large tab content</div></template>
          <template #tab-2><div class="p-6 text-gray-300">Large tab content</div></template>
        </Tabs>
      </div>
    </div>`
    }),
    args: {
        tabs: ['Tab 1', 'Tab 2', 'Tab 3']
    }
}

export const Alignments: Story = {
    render: (args) => ({
        components: {Tabs},
        setup() {
            return {args}
        },
        template: `
    <div class="p-8 bg-background-dark space-y-8">
      <div>
        <h3 class="text-white mb-4">Start (Default)</h3>
        <Tabs :tabs="args.tabs" alignment="start">
          <template #tab-0><div class="p-4 text-gray-300">Content aligned to start</div></template>
          <template #tab-1><div class="p-4 text-gray-300">Content aligned to start</div></template>
        </Tabs>
      </div>
      <div>
        <h3 class="text-white mb-4">Center</h3>
        <Tabs :tabs="args.tabs" alignment="center">
          <template #tab-0><div class="p-4 text-gray-300">Centered content</div></template>
          <template #tab-1><div class="p-4 text-gray-300">Centered content</div></template>
        </Tabs>
      </div>
      <div>
        <h3 class="text-white mb-4">End</h3>
        <Tabs :tabs="args.tabs" alignment="end">
          <template #tab-0><div class="p-4 text-gray-300">Content aligned to end</div></template>
          <template #tab-1><div class="p-4 text-gray-300">Content aligned to end</div></template>
        </Tabs>
      </div>
    </div>`
    }),
    args: {
        tabs: ['First Tab', 'Second Tab']
    }
}

export const FullWidth: Story = {
    render: (args) => ({
        components: {Tabs},
        setup() {
            return {args}
        },
        template: `
    <div class="p-8 bg-background-dark min-h-[400px]">
      <Tabs v-bind="args">
        <template #tab-0>
          <div class="p-4 text-gray-300">
            <h3 class="text-lg font-semibold mb-2">Mobile View</h3>
            <p>Full-width tabs are perfect for mobile interfaces.</p>
          </div>
        </template>
        <template #tab-1>
          <div class="p-4 text-gray-300">
            <h3 class="text-lg font-semibold mb-2">Tablet View</h3>
            <p>Each tab takes equal width for a balanced layout.</p>
          </div>
        </template>
        <template #tab-2>
          <div class="p-4 text-gray-300">
            <h3 class="text-lg font-semibold mb-2">Desktop View</h3>
            <p>Great for consistent spacing across devices.</p>
          </div>
        </template>
      </Tabs>
    </div>`
    }),
    args: {
        tabs: ['Mobile', 'Tablet', 'Desktop'],
        fullWidth: true,
        variant: 'pills'
    }
}

export const Vertical: Story = {
    render: (args) => ({
        components: {Tabs},
        setup() {
            return {args}
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
    </div>`
    }),
    args: {
        tabs: ['General', 'Security', 'Privacy', 'Notifications'],
        vertical: true,
        variant: 'pills'
    }
}

export const WithVModel: Story = {
    render: (args) => ({
        components: {Tabs},
        setup() {
            const activeTab = ref(1)
            return {args, activeTab}
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
    </div>`
    }),
    args: {
        tabs: ['Tab A', 'Tab B', 'Tab C'],
        variant: 'pills'
    }
}

export const NoGlowEffect: Story = {
    render: (args) => ({
        components: {Tabs},
        setup() {
            return {args}
        },
        template: `
    <div class="p-8 bg-background-dark min-h-[400px]">
      <Tabs v-bind="args">
        <template #tab-0>
          <div class="p-4 text-gray-300">
            <h3 class="text-lg font-semibold mb-2">Without Glow</h3>
            <p>Tabs without the glow effect for a more subtle appearance.</p>
          </div>
        </template>
        <template #tab-1>
          <div class="p-4 text-gray-300">
            <h3 class="text-lg font-semibold mb-2">Minimal Design</h3>
            <p>Disable glowEffect prop for a cleaner look.</p>
          </div>
        </template>
      </Tabs>
    </div>`
    }),
    args: {
        tabs: ['First', 'Second'],
        variant: 'pills',
        glowEffect: false
    }
}
