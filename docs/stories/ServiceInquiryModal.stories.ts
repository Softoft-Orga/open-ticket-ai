import type { Meta, StoryObj } from '@storybook/vue3'
import ServiceInquiryModal from '../src/components/vue/forms/ServiceInquiryModal.vue'
import { ref } from 'vue'

const meta = {
  title: 'Forms/ServiceInquiryModal',
  component: ServiceInquiryModal,
  tags: ['autodocs'],
  argTypes: {
    isOpen: {
      control: 'boolean',
      description: 'Controls the modal visibility'
    },
    selectedService: {
      control: 'select',
      options: [
        '',
        'Evaluation Dataset Generation',
        'Training Dataset Generation',
        'Enterprise Dataset Generation',
        'Integration Package - Standard Stack',
        'Integration Package - Enterprise/Custom',
        'OTA Automation Pack',
        'Custom Tags Model - Synthetic',
        'Custom Tag Model - Real Data',
        'Custom Development',
        'Hourly Engineering',
        'Ongoing Support Subscription'
      ],
      description: 'Pre-selected service option'
    }
  }
} satisfies Meta<typeof ServiceInquiryModal>

export default meta
type Story = StoryObj<typeof meta>

export const Default: Story = {
  render: (args) => ({
    components: { ServiceInquiryModal },
    setup() {
      const isOpen = ref(true)
      return { args, isOpen }
    },
    template: `
      <div>
        <button 
          @click="isOpen = true"
          class="px-6 py-3 rounded-lg bg-gradient-to-r from-primary to-purple-600 text-white font-bold hover:from-primary-dark hover:to-purple-700 transition-all shadow-lg shadow-primary/20"
        >
          Open Service Inquiry
        </button>
        <ServiceInquiryModal 
          :isOpen="isOpen" 
          :selectedService="args.selectedService"
          @close="isOpen = false" 
        />
      </div>
    `
  }),
  args: {
    selectedService: ''
  }
}

export const WithPreselectedService: Story = {
  render: (args) => ({
    components: { ServiceInquiryModal },
    setup() {
      const isOpen = ref(true)
      return { args, isOpen }
    },
    template: `
      <div>
        <button 
          @click="isOpen = true"
          class="px-6 py-3 rounded-lg bg-gradient-to-r from-primary to-purple-600 text-white font-bold hover:from-primary-dark hover:to-purple-700 transition-all shadow-lg shadow-primary/20"
        >
          Get Rollout Plan
        </button>
        <ServiceInquiryModal 
          :isOpen="isOpen" 
          :selectedService="args.selectedService"
          @close="isOpen = false" 
        />
      </div>
    `
  }),
  args: {
    selectedService: 'Training Dataset Generation'
  }
}

export const IntegrationInquiry: Story = {
  render: (args) => ({
    components: { ServiceInquiryModal },
    setup() {
      const isOpen = ref(true)
      return { args, isOpen }
    },
    template: `
      <div>
        <button 
          @click="isOpen = true"
          class="px-6 py-3 rounded-lg border border-white/20 text-white font-bold hover:bg-white/5 transition-colors"
        >
          Request Proposal
        </button>
        <ServiceInquiryModal 
          :isOpen="isOpen" 
          :selectedService="args.selectedService"
          @close="isOpen = false" 
        />
      </div>
    `
  }),
  args: {
    selectedService: 'Integration Package - Standard Stack'
  }
}
