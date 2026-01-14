import ModalTrigger from '../src/components/vue/core/basic/ModalTrigger.vue'
import Button from '../src/components/vue/core/basic/Button.vue'
import type { Meta, StoryObj } from '@storybook/vue3'

const meta: Meta<typeof ModalTrigger> = {
  title: 'Core/ModalTrigger',
  component: ModalTrigger,
  tags: ['autodocs'],
  argTypes: {
    tone: {
      control: { type: 'select' },
      options: ['neutral', 'primary', 'success', 'warning', 'danger', 'info']
    },
    size: {
      control: { type: 'select' },
      options: ['sm', 'md', 'lg']
    },
    buttonVariant: {
      control: { type: 'select' },
      options: ['surface', 'solid', 'outline', 'ghost', 'subtle']
    },
    buttonTone: {
      control: { type: 'select' },
      options: ['neutral', 'primary', 'success', 'warning', 'danger', 'info']
    },
    buttonSize: {
      control: { type: 'select' },
      options: ['sm', 'md', 'lg']
    },
    closeOnOverlay: {
      control: { type: 'boolean' }
    }
  },
  parameters: {
    docs: {
      description: {
        component: 'ModalTrigger component that manages its own modal state. Exposes an open() function via the #button slot, allowing custom trigger buttons while keeping state internal. No modal state leaks to parent components.'
      }
    }
  }
}
export default meta

type Story = StoryObj<typeof meta>

export const Default: Story = {
  render: (args) => ({
    components: { ModalTrigger },
    setup() {
      return { args }
    },
    template: `
      <ModalTrigger v-bind="args">
        <p>This is a default modal triggered by the ModalTrigger component.</p>
        <p class="mt-4">The component manages its own state internally, so no state management is needed in the parent.</p>
      </ModalTrigger>
    `
  }),
  args: {
    title: 'Modal Title',
    buttonText: 'Open Modal',
    tone: 'neutral',
    size: 'md',
    buttonVariant: 'surface',
    buttonTone: 'primary',
    buttonSize: 'md',
    closeOnOverlay: true
  }
}

export const CustomButtonSlot: Story = {
  render: (args) => ({
    components: { ModalTrigger, Button },
    setup() {
      return { args }
    },
    template: `
      <ModalTrigger v-bind="args">
        <template #button="{ open }">
          <Button variant="outline" tone="primary" @click="open">
            Custom Trigger Button
          </Button>
        </template>
        <p>This modal is opened using a custom button provided via the #button slot.</p>
        <p class="mt-4">The open() function is exposed via the slot props, allowing full control over when and how the modal opens.</p>
      </ModalTrigger>
    `
  }),
  args: {
    title: 'Custom Button Trigger',
    tone: 'neutral',
    size: 'md',
    closeOnOverlay: true
  }
}

export const WithCustomTitle: Story = {
  render: (args) => ({
    components: { ModalTrigger },
    setup() {
      return { args }
    },
    template: `
      <ModalTrigger v-bind="args">
        <template #title>
          <div class="flex items-center gap-3">
            <div class="w-12 h-12 rounded-full bg-primary/20 flex items-center justify-center">
              <svg class="w-6 h-6 text-primary" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
              </svg>
            </div>
            <h3 class="text-2xl font-bold text-white">Custom Title with Icon</h3>
          </div>
        </template>
        <p>This modal demonstrates using the title slot for custom header content.</p>
      </ModalTrigger>
    `
  }),
  args: {
    buttonText: 'Open with Custom Title',
    tone: 'primary',
    size: 'md',
    buttonVariant: 'surface',
    buttonTone: 'primary',
    buttonSize: 'md',
    closeOnOverlay: true
  }
}

export const WithFooter: Story = {
  render: (args) => ({
    components: { ModalTrigger, Button },
    setup() {
      return { args }
    },
    template: `
      <ModalTrigger v-bind="args">
        <p>This modal includes a footer slot for actions or additional information.</p>
        <template #footer>
          <div class="flex justify-end gap-3">
            <Button variant="outline" tone="neutral">Cancel</Button>
            <Button variant="solid" tone="primary">Confirm</Button>
          </div>
        </template>
      </ModalTrigger>
    `
  }),
  args: {
    title: 'Confirm Action',
    buttonText: 'Open Modal with Footer',
    tone: 'neutral',
    size: 'md',
    buttonVariant: 'surface',
    buttonTone: 'primary',
    buttonSize: 'md',
    closeOnOverlay: true
  }
}

export const PrimaryTone: Story = {
  render: (args) => ({
    components: { ModalTrigger },
    setup() {
      return { args }
    },
    template: `
      <ModalTrigger v-bind="args">
        <p>This modal uses the primary tone, giving it a subtle primary color tint.</p>
      </ModalTrigger>
    `
  }),
  args: {
    title: 'Primary Modal',
    buttonText: 'Open Primary Modal',
    tone: 'primary',
    size: 'md',
    buttonVariant: 'surface',
    buttonTone: 'primary',
    buttonSize: 'md',
    closeOnOverlay: true
  }
}

export const DangerTone: Story = {
  render: (args) => ({
    components: { ModalTrigger, Button },
    setup() {
      return { args }
    },
    template: `
      <ModalTrigger v-bind="args">
        <p>This action cannot be undone. Are you sure you want to proceed?</p>
        <template #footer>
          <div class="flex justify-end gap-3">
            <Button variant="outline">Cancel</Button>
            <Button tone="danger">Delete</Button>
          </div>
        </template>
      </ModalTrigger>
    `
  }),
  args: {
    title: 'Confirm Deletion',
    buttonText: 'Delete',
    tone: 'danger',
    size: 'md',
    buttonVariant: 'surface',
    buttonTone: 'danger',
    buttonSize: 'md',
    closeOnOverlay: true
  }
}

export const SmallSize: Story = {
  render: (args) => ({
    components: { ModalTrigger },
    setup() {
      return { args }
    },
    template: `
      <ModalTrigger v-bind="args">
        <p>This is a small modal, great for quick confirmations.</p>
      </ModalTrigger>
    `
  }),
  args: {
    title: 'Small Modal',
    buttonText: 'Open Small Modal',
    tone: 'neutral',
    size: 'sm',
    buttonVariant: 'surface',
    buttonTone: 'primary',
    buttonSize: 'md',
    closeOnOverlay: true
  }
}

export const LargeSize: Story = {
  render: (args) => ({
    components: { ModalTrigger },
    setup() {
      return { args }
    },
    template: `
      <ModalTrigger v-bind="args">
        <p>This is a large modal, suitable for forms or detailed content.</p>
        <div class="mt-4 space-y-4">
          <p>It can contain multiple sections and longer content without feeling cramped.</p>
          <p>The increased width makes it ideal for:</p>
          <ul class="list-disc pl-5 space-y-1">
            <li>Complex forms with multiple fields</li>
            <li>Detailed product information</li>
            <li>Image galleries or media content</li>
            <li>Multi-step wizards</li>
          </ul>
        </div>
      </ModalTrigger>
    `
  }),
  args: {
    title: 'Large Modal',
    buttonText: 'Open Large Modal',
    tone: 'neutral',
    size: 'lg',
    buttonVariant: 'surface',
    buttonTone: 'primary',
    buttonSize: 'md',
    closeOnOverlay: true
  }
}

export const MultipleModals: Story = {
  render: (args) => ({
    components: { ModalTrigger },
    setup() {
      return { args }
    },
    template: `
      <div class="flex gap-4">
        <ModalTrigger 
          title="First Modal" 
          buttonText="Open First Modal"
          tone="primary"
        >
          <p>This is the first modal. Each ModalTrigger manages its own state independently.</p>
        </ModalTrigger>
        
        <ModalTrigger 
          title="Second Modal" 
          buttonText="Open Second Modal"
          tone="success"
        >
          <p>This is the second modal. You can have multiple modals on the same page without state conflicts.</p>
        </ModalTrigger>
        
        <ModalTrigger 
          title="Third Modal" 
          buttonText="Open Third Modal"
          tone="info"
        >
          <p>This is the third modal. All modals are completely independent.</p>
        </ModalTrigger>
      </div>
    `
  }),
  args: {}
}
