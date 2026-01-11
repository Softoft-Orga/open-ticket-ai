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
    ctaUrl: {
      control: 'text',
      description: 'URL for the primary CTA button',
    },
    links: {
      control: 'object',
      description: 'Array of navigation items with url and label',
    },
    logoUrl: {
      control: 'text',
      description: 'URL for the logo image',
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
          <p class="text-gray-400 mt-2">Navbar with centered navigation links and a primary CTA button at the end.</p>
          <p class="text-gray-400 mt-2">Desktop view shows all items inline. Mobile view uses a slide-in dropdown menu.</p>
        </div>
      </div>
    `
  }),
  args: {
    links: [
      { label: 'Products', url: '/products/' },
      { label: 'Services', url: '/services/' },
      { label: 'Pricing', url: '/pricing/' },
    ],
    ctaLabel: 'Get Started',
    ctaUrl: '/get-started/',
  }
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
    links: [
      { label: 'Home', url: '/' },
      { label: 'Features', url: '/features/' },
      { label: 'Solutions', url: '/solutions/' },
      { label: 'Contact', url: '/contact/' },
    ],
    ctaLabel: 'Try Demo',
    ctaUrl: '/demo/',
  }
}

export const WithoutCTA: Story = {
  render: (args) => ({
    components: { NavBar },
    setup() {
      return { args }
    },
    template: `
      <div class="min-h-screen bg-slate-900">
        <NavBar v-bind="args" />
        <div class="p-8">
          <h1 class="text-white text-2xl">Navbar Without CTA</h1>
          <p class="text-gray-400 mt-2">Navigation bar without a CTA button.</p>
        </div>
      </div>
    `
  }),
  args: {
    links: [
      { label: 'Products', url: '/products/' },
      { label: 'Services', url: '/services/' },
      { label: 'Pricing', url: '/pricing/' },
    ],
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
          <p class="text-gray-400 mt-2">Click the hamburger menu to see the mobile dropdown menu.</p>
          <p class="text-gray-400 mt-2">Features:</p>
          <ul class="text-gray-400 mt-2 list-disc ml-6 space-y-1">
            <li>Slide-in transition from the right</li>
            <li>Navigation links with active state</li>
            <li>Primary CTA button at the bottom</li>
            <li>Backdrop overlay with blur effect</li>
          </ul>
        </div>
      </div>
    `
  }),
  args: {
    links: [
      { label: 'Products', url: '/products/' },
      { label: 'Services', url: '/services/' },
      { label: 'Pricing', url: '/pricing/' },
    ],
    ctaLabel: 'Get Started',
    ctaUrl: '/get-started/',
  },
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
  args: {
    links: [
      { label: 'Products', url: '/products/' },
      { label: 'Services', url: '/services/' },
      { label: 'Pricing', url: '/pricing/' },
    ],
    ctaLabel: 'Get Started',
    ctaUrl: '/get-started/',
  }
}
