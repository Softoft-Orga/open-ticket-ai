import NavBar from '../src/components/vue/core/navigation/NavBar.vue'
import type { Meta, StoryObj } from '@storybook/vue3'

const meta: Meta<typeof NavBar> = {
  title: 'Navigation/NavBar',
  component: NavBar,
  tags: ['autodocs'],
  parameters: {
    layout: 'fullscreen',
    backgrounds: {
      default: 'dark',
      values: [
        { name: 'dark', value: '#0a0118' },
      ],
    },
  },
}
export default meta

type Story = StoryObj<typeof meta>

export const Default: Story = {
  render: (args) => ({
    components: { NavBar },
    setup() {
      return { args }
    },
    template: `
      <div class="min-h-screen bg-slate-900">
        <NavBar v-bind="args" />
        <div class="p-8">
          <h1 class="text-white text-2xl">Default Navbar</h1>
          <p class="text-gray-400 mt-2">This shows the navbar in its default state with standard navigation items.</p>
        </div>
      </div>
    `
  }),
}

export const CustomNavItems: Story = {
  render: (args) => ({
    components: { NavBar },
    setup() {
      return { args }
    },
    template: `
      <div class="min-h-screen bg-slate-900">
        <NavBar v-bind="args" />
        <div class="p-8">
          <h1 class="text-white text-2xl">Custom Navigation Items</h1>
          <p class="text-gray-400 mt-2">Shows the navbar with custom navigation links.</p>
        </div>
      </div>
    `
  }),
  args: {
    navItems: [
      { label: 'Home', href: '/' },
      { label: 'Features', href: '/features/' },
      { label: 'Solutions', href: '/solutions/' },
      { label: 'Contact', href: '/contact/' },
    ]
  }
}

export const WithActiveLink: Story = {
  render: (args) => ({
    components: { NavBar },
    setup() {
      return { args }
    },
    template: `
      <div class="min-h-screen bg-slate-900">
        <NavBar v-bind="args" />
        <div class="p-8">
          <h1 class="text-white text-2xl">Active Link State</h1>
          <p class="text-gray-400 mt-2">Shows the navbar with the "Products" link in active state.</p>
        </div>
      </div>
    `
  }),
  args: {
    currentPath: '/products/'
  }
}

export const DropdownDemo: Story = {
  render: (args) => ({
    components: { NavBar },
    setup() {
      return { args }
    },
    template: `
      <div class="min-h-screen bg-slate-900">
        <NavBar v-bind="args" />
        <div class="p-8">
          <h1 class="text-white text-2xl">Dropdown Menu</h1>
          <p class="text-gray-400 mt-2">Click on "Docs" to see the Headless UI Popover menu with resources and product guides.</p>
        </div>
      </div>
    `
  }),
}

export const MobileView: Story = {
  render: (args) => ({
    components: { NavBar },
    setup() {
      return { args }
    },
    template: `
      <div class="min-h-screen bg-slate-900">
        <NavBar v-bind="args" />
        <div class="p-8">
          <h1 class="text-white text-2xl">Mobile Menu</h1>
          <p class="text-gray-400 mt-2">Resize your browser to mobile size or click the hamburger menu button to see the mobile menu.</p>
          <p class="text-gray-400 mt-2">The mobile menu features:</p>
          <ul class="text-gray-400 mt-2 list-disc ml-6 space-y-1">
            <li>Full-screen slide-over panel with Dialog component</li>
            <li>Focus trap for accessibility</li>
            <li>Collapsible Docs section using Disclosure component</li>
            <li>Primary and Secondary buttons at the bottom</li>
            <li>Smooth slide-in transition from the right</li>
          </ul>
        </div>
      </div>
    `
  }),
  parameters: {
    viewport: {
      defaultViewport: 'mobile1'
    }
  }
}

export const ButtonVariants: Story = {
  render: (args) => ({
    components: { NavBar },
    setup() {
      return { args }
    },
    template: `
      <div class="min-h-screen bg-slate-900">
        <NavBar v-bind="args" />
        <div class="p-8">
          <h1 class="text-white text-2xl">Button Variants</h1>
          <p class="text-gray-400 mt-2">The navbar uses our Button component with two variants:</p>
          <ul class="text-gray-400 mt-2 list-disc ml-6 space-y-1">
            <li><strong class="text-white">Primary Button</strong>: "See Demo" - Purple gradient with glow effect</li>
            <li><strong class="text-white">Secondary Button</strong>: "Contact Sales" - White background</li>
          </ul>
          <p class="text-gray-400 mt-2">Both buttons are visible on desktop, and appear at the bottom of the mobile menu.</p>
        </div>
      </div>
    `
  }),
}

export const KeyboardNavigation: Story = {
  render: (args) => ({
    components: { NavBar },
    setup() {
      return { args }
    },
    template: `
      <div class="min-h-screen bg-slate-900">
        <NavBar v-bind="args" />
        <div class="p-8 space-y-3">
          <h1 class="text-white text-2xl">Keyboard Accessibility</h1>
          <p class="text-gray-400">The navbar is fully keyboard accessible:</p>
          <ul class="text-gray-400 list-disc ml-6 space-y-1">
            <li><strong class="text-white">Tab</strong>: Navigate through links, popover trigger, and buttons</li>
            <li><strong class="text-white">Enter/Space</strong>: Toggle the Docs popover and mobile menu</li>
            <li><strong class="text-white">Arrow Keys</strong>: Move focus inside the popover menu (Headless UI manages focus)</li>
            <li><strong class="text-white">Escape</strong>: Close popover or mobile dialog</li>
          </ul>
        </div>
      </div>
    `
  }),
}
