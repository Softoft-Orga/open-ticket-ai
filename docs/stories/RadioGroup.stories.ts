import RadioGroup from '../src/components/vue/core/forms/RadioGroup.vue'
import RadioGroupOption from '../src/components/vue/core/forms/RadioGroupOption.vue'
import type { Meta, StoryObj } from '@storybook/vue3'
import { ref } from 'vue'

const meta: Meta<typeof RadioGroup> = {
  title: 'Core/Forms/RadioGroup',
  component: RadioGroup,
  argTypes: {
    modelValue: { control: 'text' },
    label: { control: 'text' },
    disabled: { control: 'boolean' }
  },
  parameters: {
    backgrounds: {
      default: 'dark',
      values: [
        { name: 'dark', value: '#0f0814' }
      ]
    }
  }
}
export default meta

type Story = StoryObj<typeof meta>

export const Primary: Story = {
  render: (args) => ({
    components: { RadioGroup, RadioGroupOption },
    setup() {
      const selected = ref('option1')
      return { args, selected }
    },
    template: `
      <div style="max-width: 500px;">
        <RadioGroup v-bind="args" v-model="selected">
          <RadioGroupOption value="option1" label="Option 1" description="This is the first option" variant="primary" />
          <RadioGroupOption value="option2" label="Option 2" description="This is the second option" variant="primary" />
          <RadioGroupOption value="option3" label="Option 3" description="This is the third option" variant="primary" />
        </RadioGroup>
      </div>
    `
  }),
  args: {
    label: 'Choose an option',
    disabled: false
  }
}

export const Secondary: Story = {
  render: (args) => ({
    components: { RadioGroup, RadioGroupOption },
    setup() {
      const selected = ref('plan2')
      return { args, selected }
    },
    template: `
      <div style="max-width: 500px;">
        <RadioGroup v-bind="args" v-model="selected">
          <RadioGroupOption value="plan1" label="Lite Free" description="Perfect for getting started" variant="secondary" />
          <RadioGroupOption value="plan2" label="Lite Pro" description="Best for small teams" variant="secondary" />
          <RadioGroupOption value="plan3" label="Enterprise" description="For large organizations" variant="secondary" />
        </RadioGroup>
      </div>
    `
  }),
  args: {
    label: 'Select your plan',
    disabled: false
  }
}

export const Outline: Story = {
  render: (args) => ({
    components: { RadioGroup, RadioGroupOption },
    setup() {
      const selected = ref('email')
      return { args, selected }
    },
    template: `
      <div style="max-width: 500px;">
        <RadioGroup v-bind="args" v-model="selected">
          <RadioGroupOption value="email" label="Email notifications" variant="outline" />
          <RadioGroupOption value="sms" label="SMS notifications" variant="outline" />
          <RadioGroupOption value="push" label="Push notifications" variant="outline" />
        </RadioGroup>
      </div>
    `
  }),
  args: {
    label: 'Notification method',
    disabled: false
  }
}

export const Ghost: Story = {
  render: (args) => ({
    components: { RadioGroup, RadioGroupOption },
    setup() {
      const selected = ref('light')
      return { args, selected }
    },
    template: `
      <div style="max-width: 500px;">
        <RadioGroup v-bind="args" v-model="selected">
          <RadioGroupOption value="light" label="Light mode" variant="ghost" />
          <RadioGroupOption value="dark" label="Dark mode" variant="ghost" />
          <RadioGroupOption value="auto" label="Auto (system)" variant="ghost" />
        </RadioGroup>
      </div>
    `
  }),
  args: {
    label: 'Theme preference',
    disabled: false
  }
}

export const WithTones: Story = {
  render: (args) => ({
    components: { RadioGroup, RadioGroupOption },
    setup() {
      const selected = ref('medium')
      return { args, selected }
    },
    template: `
      <div style="max-width: 500px;">
        <RadioGroup v-bind="args" v-model="selected">
          <RadioGroupOption value="low" label="Low priority" description="Can be addressed later" tone="info" />
          <RadioGroupOption value="medium" label="Medium priority" description="Should be addressed soon" tone="warning" />
          <RadioGroupOption value="high" label="High priority" description="Needs immediate attention" tone="danger" />
          <RadioGroupOption value="completed" label="Completed" description="Task is done" tone="success" />
        </RadioGroup>
      </div>
    `
  }),
  args: {
    label: 'Set priority level',
    disabled: false
  }
}

export const Disabled: Story = {
  render: (args) => ({
    components: { RadioGroup, RadioGroupOption },
    setup() {
      const selected = ref('option2')
      return { args, selected }
    },
    template: `
      <div style="max-width: 500px;">
        <RadioGroup v-bind="args" v-model="selected">
          <RadioGroupOption value="option1" label="Option 1" description="This option is disabled" variant="primary" />
          <RadioGroupOption value="option2" label="Option 2" description="This option is also disabled" variant="primary" />
          <RadioGroupOption value="option3" label="Option 3" description="All options are disabled" variant="primary" />
        </RadioGroup>
      </div>
    `
  }),
  args: {
    label: 'Disabled radio group',
    disabled: true
  }
}

export const WithDescriptionSlot: Story = {
  render: (args) => ({
    components: { RadioGroup, RadioGroupOption },
    setup() {
      const selected = ref('option1')
      return { args, selected }
    },
    template: `
      <div style="max-width: 500px;">
        <RadioGroup v-bind="args" v-model="selected">
          <template #description>
            <p>Choose the option that best fits your needs. You can change this later in settings.</p>
          </template>
          <RadioGroupOption value="option1" label="Basic" variant="primary">
            <template #description>
              <span style="color: #16dba0;">✓ All core features included</span>
            </template>
          </RadioGroupOption>
          <RadioGroupOption value="option2" label="Professional" variant="primary">
            <template #description>
              <span style="color: #16dba0;">✓ Everything in Basic + Advanced analytics</span>
            </template>
          </RadioGroupOption>
          <RadioGroupOption value="option3" label="Enterprise" variant="primary">
            <template #description>
              <span style="color: #16dba0;">✓ Everything in Professional + Priority support</span>
            </template>
          </RadioGroupOption>
        </RadioGroup>
      </div>
    `
  }),
  args: {
    label: 'Select your subscription tier',
    disabled: false
  }
}

export const AllVariants: Story = {
  render: () => ({
    components: { RadioGroup, RadioGroupOption },
    setup() {
      const selectedPrimary = ref('p1')
      const selectedSecondary = ref('s2')
      const selectedOutline = ref('o1')
      const selectedGhost = ref('g3')
      return { selectedPrimary, selectedSecondary, selectedOutline, selectedGhost }
    },
    template: `
      <div style="display: flex; flex-direction: column; gap: 2rem; padding: 2rem;">
        <div style="max-width: 500px;">
          <RadioGroup label="Primary Variant" v-model="selectedPrimary">
            <RadioGroupOption value="p1" label="Primary Option 1" variant="primary" />
            <RadioGroupOption value="p2" label="Primary Option 2" variant="primary" />
          </RadioGroup>
        </div>
        
        <div style="max-width: 500px;">
          <RadioGroup label="Secondary Variant" v-model="selectedSecondary">
            <RadioGroupOption value="s1" label="Secondary Option 1" variant="secondary" />
            <RadioGroupOption value="s2" label="Secondary Option 2" variant="secondary" />
          </RadioGroup>
        </div>
        
        <div style="max-width: 500px;">
          <RadioGroup label="Outline Variant" v-model="selectedOutline">
            <RadioGroupOption value="o1" label="Outline Option 1" variant="outline" />
            <RadioGroupOption value="o2" label="Outline Option 2" variant="outline" />
          </RadioGroup>
        </div>
        
        <div style="max-width: 500px;">
          <RadioGroup label="Ghost Variant" v-model="selectedGhost">
            <RadioGroupOption value="g1" label="Ghost Option 1" variant="ghost" />
            <RadioGroupOption value="g2" label="Ghost Option 2" variant="ghost" />
            <RadioGroupOption value="g3" label="Ghost Option 3" variant="ghost" />
          </RadioGroup>
        </div>
      </div>
    `
  })
}
