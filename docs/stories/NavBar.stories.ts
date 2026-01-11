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
  argTypes: {
    ctaLabel: {
      control: 'text',
      description: 'Label for the primary CTA button',
    },
    currentPath: {
      control: 'text',
      description: 'Current active path for highlighting navigation items',
    },
    navItems: {
      control: 'object',
      description: 'Array of navigation items with href and label',
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
          <p class="text-gray-400 mt-2">Simple navbar with logo, navigation links, and a primary CTA button.</p>
          <p class="text-gray-400 mt-2">Desktop view shows all items inline. Mobile view uses a slide-over menu.</p>
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
          <p class="text-gray-400 mt-2">Navbar with custom navigation links and CTA button label.</p>
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
    ],
    ctaLabel: 'Try Demo'
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
          <p class="text-gray-400 mt-2">The "Products" link is highlighted as active.</p>
        </div>
      </div>
    `
  }),
  args: {
    currentPath: '/products/'
  }
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
          <p class="text-gray-400 mt-2">Click the hamburger menu to see the mobile slide-over panel.</p>
          <p class="text-gray-400 mt-2">Features:</p>
          <ul class="text-gray-400 mt-2 list-disc ml-6 space-y-1">
            <li>Headless UI Dialog component for accessibility</li>
            <li>Slide-in transition from the right</li>
            <li>Navigation links with active state</li>
            <li>Primary CTA button at the bottom</li>
            <li>Focus trap and backdrop overlay</li>
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

export const KeyboardAccessibility: Story = {
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
          <p class="text-gray-400 mt-2">The navbar is fully keyboard accessible:</p>
          <ul class="text-gray-400 mt-2 list-disc ml-6 space-y-1">
            <li><strong class="text-white">Tab</strong>: Navigate through all interactive elements</li>
            <li><strong class="text-white">Enter/Space</strong>: Activate buttons and links</li>
            <li><strong class="text-white">Escape</strong>: Close mobile menu</li>
          </ul>
        </div>
      </div>
    `
  }),
}
