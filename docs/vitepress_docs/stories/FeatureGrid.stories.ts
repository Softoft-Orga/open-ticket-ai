import FeatureGrid from '../.vitepress/components/core/basic/FeatureGrid.vue'
import Card from '../.vitepress/components/core/basic/Card.vue'
import type { Meta, StoryObj } from '@storybook/vue3'

const meta: Meta<typeof FeatureGrid> = {
  title: 'Core/FeatureGrid',
  component: FeatureGrid,
}
export default meta

type Story = StoryObj<typeof meta>

export const Default: Story = {
  render: () => ({
    components: { FeatureGrid, Card },
    template: `
      <FeatureGrid>
        <Card>Feature 1</Card>
        <Card>Feature 2</Card>
        <Card>Feature 3</Card>
      </FeatureGrid>
    `,
  }),
}
