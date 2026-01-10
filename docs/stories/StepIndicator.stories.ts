import StepIndicator from '../src/components/vue/core/StepIndicator.vue'
import type { Meta, StoryObj } from '@storybook/vue3'

const meta: Meta<typeof StepIndicator> = {
  title: 'Docs/StepIndicator',
  component: StepIndicator,
  tags: ['autodocs'],
  parameters: {
    docs: {
      description: {
        component: 'Step indicator component for displaying multi-step processes or tutorials in documentation.'
      }
    }
  }
}
export default meta

type Story = StoryObj<typeof meta>

export const FirstStep: Story = {
  render: (args) => ({
    components: { StepIndicator },
    setup() {
      return { args }
    },
    template: '<StepIndicator v-bind="args" />'
  }),
  args: {
    steps: ['Install', 'Configure', 'Deploy', 'Monitor'],
    currentStep: 0
  }
}

export const MiddleStep: Story = {
  render: (args) => ({
    components: { StepIndicator },
    setup() {
      return { args }
    },
    template: '<StepIndicator v-bind="args" />'
  }),
  args: {
    steps: ['Install', 'Configure', 'Deploy', 'Monitor'],
    currentStep: 2
  }
}

export const LastStep: Story = {
  render: (args) => ({
    components: { StepIndicator },
    setup() {
      return { args }
    },
    template: '<StepIndicator v-bind="args" />'
  }),
  args: {
    steps: ['Install', 'Configure', 'Deploy', 'Monitor'],
    currentStep: 3
  }
}

export const ThreeSteps: Story = {
  render: (args) => ({
    components: { StepIndicator },
    setup() {
      return { args }
    },
    template: '<StepIndicator v-bind="args" />'
  }),
  args: {
    steps: ['Setup', 'Build', 'Launch'],
    currentStep: 1
  }
}

export const ManySteps: Story = {
  render: (args) => ({
    components: { StepIndicator },
    setup() {
      return { args }
    },
    template: '<StepIndicator v-bind="args" />'
  }),
  args: {
    steps: ['Create Account', 'Verify Email', 'Choose Plan', 'Add Payment', 'Configure Settings', 'Launch'],
    currentStep: 3
  }
}
