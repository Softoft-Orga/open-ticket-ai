import Card from '../.vitepress/components/core/basic/Card.vue'
import type { Meta, StoryObj } from '@storybook/vue3'

const meta: Meta<typeof Card> = {
  title: 'Core/Card',
  component: Card,
  tags: ['autodocs'],
}
export default meta

type Story = StoryObj<typeof meta>

export const Default: Story = {
  render: (args) => ({
    components: { Card },
    setup() { return { args } },
    template: '<Card>Simple card content</Card>'
  }),
}

export const WithHeader: Story = {
  render: (args) => ({
    components: { Card },
    setup() { return { args } },
    template: `
      <Card>
        <template #header>
          <h3 class="text-lg font-bold">Card Title</h3>
        </template>
        <p>Main card content goes here.</p>
      </Card>
    `
  }),
}

export const WithFooter: Story = {
  render: (args) => ({
    components: { Card },
    setup() { return { args } },
    template: `
      <Card>
        <p>Main card content goes here.</p>
        <template #footer>
          <button class="text-vp-brand hover:underline">Action Button</button>
        </template>
      </Card>
    `
  }),
}

export const Full: Story = {
  render: (args) => ({
    components: { Card },
    setup() { return { args } },
    template: `
      <Card>
        <template #header>
          <h3 class="text-lg font-bold">Card Title</h3>
        </template>
        <p>Main card content goes here.</p>
        <template #footer>
          <button class="text-vp-brand hover:underline">Action Button</button>
        </template>
      </Card>
    `
  }),
}
