import Modal from '../src/components/vue/core/basic/Modal.vue'
import Button from '../src/components/vue/core/basic/Button.vue'
import type { Meta, StoryObj } from '@storybook/vue3'
import { ref } from 'vue'

const meta: Meta<typeof Modal> = {
  title: 'Core/Modal',
  component: Modal,
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
    closeOnOverlay: {
      control: { type: 'boolean' }
    }
  },
  parameters: {
    docs: {
      description: {
        component: 'Accessible modal dialog component built with Headless UI. Supports different tones, sizes, and customizable content via slots. Features backdrop blur, escape key handling, and focus trapping.'
      }
    }
  }
}
export default meta

type Story = StoryObj<typeof meta>

export const Default: Story = {
  render: (args) => ({
    components: { Modal, Button },
    setup() {
      const isOpen = ref(false)
      return { args, isOpen }
    },
    template: `
      <div>
        <Button @click="isOpen = true">Open Modal</Button>
        <Modal v-bind="args" :open="isOpen" @close="isOpen = false">
          <p>This is a default modal with neutral tone. It can contain any content you need.</p>
          <p class="mt-4">Click outside the modal or press Escape to close it.</p>
        </Modal>
      </div>
    `
  }),
  args: {
    title: 'Modal Title',
    tone: 'neutral',
    size: 'md',
    closeOnOverlay: true
  }
}

export const WithFooter: Story = {
  render: (args) => ({
    components: { Modal, Button },
    setup() {
      const isOpen = ref(false)
      return { args, isOpen }
    },
    template: `
      <div>
        <Button @click="isOpen = true">Open Modal with Footer</Button>
        <Modal v-bind="args" :open="isOpen" @close="isOpen = false">
          <p>This modal includes a footer slot for actions or additional information.</p>
          <template #footer>
            <div class="flex justify-end gap-3">
              <Button variant="outline" tone="neutral" @click="isOpen = false">Cancel</Button>
              <Button variant="solid" tone="primary" @click="isOpen = false">Confirm</Button>
            </div>
          </template>
        </Modal>
      </div>
    `
  }),
  args: {
    title: 'Confirm Action',
    tone: 'neutral',
    size: 'md',
    closeOnOverlay: true
  }
}

export const PrimaryTone: Story = {
  render: (args) => ({
    components: { Modal, Button },
    setup() {
      const isOpen = ref(false)
      return { args, isOpen }
    },
    template: `
      <div>
        <Button tone="primary" @click="isOpen = true">Open Primary Modal</Button>
        <Modal v-bind="args" :open="isOpen" @close="isOpen = false">
          <p>This modal uses the primary tone, giving it a subtle primary color tint.</p>
        </Modal>
      </div>
    `
  }),
  args: {
    title: 'Primary Modal',
    tone: 'primary',
    size: 'md',
    closeOnOverlay: true
  }
}

export const SuccessTone: Story = {
  render: (args) => ({
    components: { Modal, Button },
    setup() {
      const isOpen = ref(false)
      return { args, isOpen }
    },
    template: `
      <div>
        <Button tone="success" @click="isOpen = true">Open Success Modal</Button>
        <Modal v-bind="args" :open="isOpen" @close="isOpen = false">
          <p>Your action was completed successfully!</p>
          <template #footer>
            <div class="flex justify-end">
              <Button tone="success" @click="isOpen = false">Got it</Button>
            </div>
          </template>
        </Modal>
      </div>
    `
  }),
  args: {
    title: 'Success',
    tone: 'success',
    size: 'md',
    closeOnOverlay: true
  }
}

export const WarningTone: Story = {
  render: (args) => ({
    components: { Modal, Button },
    setup() {
      const isOpen = ref(false)
      return { args, isOpen }
    },
    template: `
      <div>
        <Button tone="warning" @click="isOpen = true">Open Warning Modal</Button>
        <Modal v-bind="args" :open="isOpen" @close="isOpen = false">
          <p>Please review this warning before proceeding.</p>
          <template #footer>
            <div class="flex justify-end gap-3">
              <Button variant="outline" @click="isOpen = false">Cancel</Button>
              <Button tone="warning" @click="isOpen = false">Proceed</Button>
            </div>
          </template>
        </Modal>
      </div>
    `
  }),
  args: {
    title: 'Warning',
    tone: 'warning',
    size: 'md',
    closeOnOverlay: true
  }
}

export const DangerTone: Story = {
  render: (args) => ({
    components: { Modal, Button },
    setup() {
      const isOpen = ref(false)
      return { args, isOpen }
    },
    template: `
      <div>
        <Button tone="danger" @click="isOpen = true">Open Danger Modal</Button>
        <Modal v-bind="args" :open="isOpen" @close="isOpen = false">
          <p>This action cannot be undone. Are you sure you want to proceed?</p>
          <template #footer>
            <div class="flex justify-end gap-3">
              <Button variant="outline" @click="isOpen = false">Cancel</Button>
              <Button tone="danger" @click="isOpen = false">Delete</Button>
            </div>
          </template>
        </Modal>
      </div>
    `
  }),
  args: {
    title: 'Confirm Deletion',
    tone: 'danger',
    size: 'md',
    closeOnOverlay: true
  }
}

export const InfoTone: Story = {
  render: (args) => ({
    components: { Modal, Button },
    setup() {
      const isOpen = ref(false)
      return { args, isOpen }
    },
    template: `
      <div>
        <Button tone="info" @click="isOpen = true">Open Info Modal</Button>
        <Modal v-bind="args" :open="isOpen" @close="isOpen = false">
          <p>Here's some important information you should know.</p>
          <ul class="list-disc pl-5 space-y-1 mt-4">
            <li>Point one</li>
            <li>Point two</li>
            <li>Point three</li>
          </ul>
        </Modal>
      </div>
    `
  }),
  args: {
    title: 'Information',
    tone: 'info',
    size: 'md',
    closeOnOverlay: true
  }
}

export const SmallSize: Story = {
  render: (args) => ({
    components: { Modal, Button },
    setup() {
      const isOpen = ref(false)
      return { args, isOpen }
    },
    template: `
      <div>
        <Button @click="isOpen = true">Open Small Modal</Button>
        <Modal v-bind="args" :open="isOpen" @close="isOpen = false">
          <p>This is a small modal, great for quick confirmations.</p>
        </Modal>
      </div>
    `
  }),
  args: {
    title: 'Small Modal',
    tone: 'neutral',
    size: 'sm',
    closeOnOverlay: true
  }
}

export const LargeSize: Story = {
  render: (args) => ({
    components: { Modal, Button },
    setup() {
      const isOpen = ref(false)
      return { args, isOpen }
    },
    template: `
      <div>
        <Button @click="isOpen = true">Open Large Modal</Button>
        <Modal v-bind="args" :open="isOpen" @close="isOpen = false">
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
        </Modal>
      </div>
    `
  }),
  args: {
    title: 'Large Modal',
    tone: 'neutral',
    size: 'lg',
    closeOnOverlay: true
  }
}

export const NoCloseOnOverlay: Story = {
  render: (args) => ({
    components: { Modal, Button },
    setup() {
      const isOpen = ref(false)
      return { args, isOpen }
    },
    template: `
      <div>
        <Button @click="isOpen = true">Open Modal (No Close on Overlay)</Button>
        <Modal v-bind="args" :open="isOpen" @close="isOpen = false">
          <p>This modal cannot be closed by clicking the backdrop. You must use the close button or footer actions.</p>
          <template #footer>
            <div class="flex justify-end">
              <Button @click="isOpen = false">Close</Button>
            </div>
          </template>
        </Modal>
      </div>
    `
  }),
  args: {
    title: 'Required Action',
    tone: 'neutral',
    size: 'md',
    closeOnOverlay: false
  }
}

export const CustomTitleSlot: Story = {
  render: (args) => ({
    components: { Modal, Button },
    setup() {
      const isOpen = ref(false)
      return { args, isOpen }
    },
    template: `
      <div>
        <Button @click="isOpen = true">Open Modal with Custom Title</Button>
        <Modal v-bind="args" :open="isOpen" @close="isOpen = false">
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
        </Modal>
      </div>
    `
  }),
  args: {
    tone: 'primary',
    size: 'md',
    closeOnOverlay: true
  }
}
