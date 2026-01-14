import ModalTrigger from '../src/components/vue/core/basic/ModalTrigger.vue';
import Button from '../src/components/vue/core/basic/Button.vue';
import type { Meta, StoryObj } from '@storybook/vue3';

const meta: Meta<typeof ModalTrigger> = {
  title: 'Core/ModalTrigger',
  component: ModalTrigger,
  tags: ['autodocs'],
  argTypes: {
    tone: {
      control: { type: 'select' },
      options: ['neutral', 'primary', 'success', 'warning', 'danger', 'info'],
    },
    size: {
      control: { type: 'select' },
      options: ['sm', 'md', 'lg'],
    },
    closeOnOverlay: {
      control: { type: 'boolean' },
    },
    buttonVariant: {
      control: { type: 'select' },
      options: ['surface', 'outline', 'solid', 'subtle', 'ghost'],
    },
    buttonTone: {
      control: { type: 'select' },
      options: ['neutral', 'primary', 'success', 'warning', 'danger', 'info'],
    },
    buttonSize: {
      control: { type: 'select' },
      options: ['sm', 'md', 'lg'],
    },
  },
  parameters: {
    docs: {
      description: {
        component:
          'ModalTrigger component that manages its own modal state with a built-in button. The button can be customized using button* props. No modal state leaks to parent components.',
      },
    },
  },
};
export default meta;

type Story = StoryObj<typeof meta>;

export const Default: Story = {
  render: args => ({
    components: { ModalTrigger, Button },
    setup() {
      return { args };
    },
    template: `
      <ModalTrigger v-bind="args">
        <p>This is a default modal triggered by the ModalTrigger component.</p>
        <p class="mt-4">The component manages its own state internally, so no state management is needed in the parent.</p>
      </ModalTrigger>
    `,
  }),
  args: {
    title: 'Modal Title',
    tone: 'neutral',
    size: 'md',
    closeOnOverlay: true,
    buttonText: 'Open Modal',
    buttonVariant: 'surface',
    buttonTone: 'primary',
  },
};

export const CustomButton: Story = {
  render: args => ({
    components: { ModalTrigger, Button },
    setup() {
      return { args };
    },
    template: `
      <ModalTrigger v-bind="args">
        <p>This modal is opened using a customized button with outline variant.</p>
        <p class="mt-4">The button appearance can be fully controlled via the button* props.</p>
      </ModalTrigger>
    `,
  }),
  args: {
    title: 'Custom Button Style',
    tone: 'neutral',
    size: 'md',
    closeOnOverlay: true,
    buttonText: 'Custom Trigger Button',
    buttonVariant: 'outline',
    buttonTone: 'primary',
  },
};

export const WithCustomTitle: Story = {
  render: args => ({
    components: { ModalTrigger, Button },
    setup() {
      return { args };
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
    `,
  }),
  args: {
    tone: 'primary',
    size: 'md',
    closeOnOverlay: true,
    buttonText: 'Open with Custom Title',
    buttonVariant: 'surface',
    buttonTone: 'primary',
  },
};

export const WithFooter: Story = {
  render: args => ({
    components: { ModalTrigger, Button },
    setup() {
      return { args };
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
    `,
  }),
  args: {
    title: 'Confirm Action',
    tone: 'neutral',
    size: 'md',
    closeOnOverlay: true,
    buttonText: 'Open Modal with Footer',
    buttonVariant: 'surface',
    buttonTone: 'primary',
  },
};

export const PrimaryTone: Story = {
  render: args => ({
    components: { ModalTrigger, Button },
    setup() {
      return { args };
    },
    template: `
      <ModalTrigger v-bind="args">
        <p>This modal uses the primary tone, giving it a subtle primary color tint.</p>
      </ModalTrigger>
    `,
  }),
  args: {
    title: 'Primary Modal',
    tone: 'primary',
    size: 'md',
    closeOnOverlay: true,
    buttonText: 'Open Primary Modal',
    buttonVariant: 'surface',
    buttonTone: 'primary',
  },
};

export const DangerTone: Story = {
  render: args => ({
    components: { ModalTrigger, Button },
    setup() {
      return { args };
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
    `,
  }),
  args: {
    title: 'Confirm Deletion',
    tone: 'danger',
    size: 'md',
    closeOnOverlay: true,
    buttonText: 'Delete',
    buttonVariant: 'surface',
    buttonTone: 'danger',
  },
};

export const SmallSize: Story = {
  render: args => ({
    components: { ModalTrigger, Button },
    setup() {
      return { args };
    },
    template: `
      <ModalTrigger v-bind="args">
        <p>This is a small modal, great for quick confirmations.</p>
      </ModalTrigger>
    `,
  }),
  args: {
    title: 'Small Modal',
    tone: 'neutral',
    size: 'sm',
    closeOnOverlay: true,
    buttonText: 'Open Small Modal',
    buttonVariant: 'surface',
    buttonTone: 'primary',
  },
};

export const LargeSize: Story = {
  render: args => ({
    components: { ModalTrigger, Button },
    setup() {
      return { args };
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
    `,
  }),
  args: {
    title: 'Large Modal',
    tone: 'neutral',
    size: 'lg',
    closeOnOverlay: true,
    buttonText: 'Open Large Modal',
    buttonVariant: 'surface',
    buttonTone: 'primary',
  },
};

export const MultipleModals: Story = {
  render: args => ({
    components: { ModalTrigger, Button },
    setup() {
      return { args };
    },
    template: `
      <div class="flex gap-4">
        <ModalTrigger 
          title="First Modal" 
          tone="primary"
          button-text="Open First Modal"
          button-variant="surface"
          button-tone="primary"
        >
          <p>This is the first modal. Each ModalTrigger manages its own state independently.</p>
        </ModalTrigger>
        
        <ModalTrigger 
          title="Second Modal" 
          tone="success"
          button-text="Open Second Modal"
          button-variant="surface"
          button-tone="success"
        >
          <p>This is the second modal. You can have multiple modals on the same page without state conflicts.</p>
        </ModalTrigger>
        
        <ModalTrigger 
          title="Third Modal" 
          tone="info"
          button-text="Open Third Modal"
          button-variant="surface"
          button-tone="info"
        >
          <p>This is the third modal. All modals are completely independent.</p>
        </ModalTrigger>
      </div>
    `,
  }),
  args: {},
};
