import FeatureGrid from '../src/components/vue/core/basic/FeatureGrid.vue'
import Card from '../src/components/vue/core/basic/Card.vue'
import Badge from '../src/components/vue/core/basic/Badge.vue'
import type {Meta, StoryObj} from '@storybook/vue3'

const meta: Meta<typeof FeatureGrid> = {
    title: 'Core/FeatureGrid',
    component: FeatureGrid,
    parameters: {
        docs: {
            description: {
                component: 'Responsive grid layout component for displaying features in a 1-3 column layout depending on screen size.'
            }
        }
    }
}
export default meta

type Story = StoryObj<typeof meta>

export const Default: Story = {
    render: () => ({
        components: {FeatureGrid, Card},
        template: `
      <FeatureGrid>
        <Card>
          <template #header>
            <h3 class="font-semibold">Feature 1</h3>
          </template>
          <p>Basic feature description</p>
        </Card>
        <Card>
          <template #header>
            <h3 class="font-semibold">Feature 2</h3>
          </template>
          <p>Another feature description</p>
        </Card>
        <Card>
          <template #header>
            <h3 class="font-semibold">Feature 3</h3>
          </template>
          <p>Third feature description</p>
        </Card>
      </FeatureGrid>
    `,
    }),
}

export const ProductFeatures: Story = {
    render: () => ({
        components: {FeatureGrid, Card, Badge},
        template: `
      <FeatureGrid>
        <Card>
          <template #header>
            <div class="flex items-center justify-between">
              <h3 class="font-semibold">AI Classification</h3>
              <Badge type="primary">Core</Badge>
            </div>
          </template>
          <p class="text-sm text-gray-300">Automatically categorize tickets using advanced machine learning models with 95%+ accuracy.</p>
        </Card>
        <Card>
          <template #header>
            <div class="flex items-center justify-between">
              <h3 class="font-semibold">Multi-language Support</h3>
              <Badge type="success">Available</Badge>
            </div>
          </template>
          <p class="text-sm text-gray-300">Process tickets in over 50 languages with automatic language detection and translation.</p>
        </Card>
        <Card>
          <template #header>
            <div class="flex items-center justify-between">
              <h3 class="font-semibold">Custom Training</h3>
              <Badge type="warning">Beta</Badge>
            </div>
          </template>
          <p class="text-sm text-gray-300">Train the AI on your own ticket data to improve accuracy for your specific use cases.</p>
        </Card>
        <Card>
          <template #header>
            <div class="flex items-center justify-between">
              <h3 class="font-semibold">Real-time Analytics</h3>
              <Badge type="primary">Core</Badge>
            </div>
          </template>
          <p class="text-sm text-gray-300">Monitor classification performance with real-time dashboards and detailed metrics.</p>
        </Card>
        <Card>
          <template #header>
            <div class="flex items-center justify-between">
              <h3 class="font-semibold">API Integration</h3>
              <Badge type="success">Available</Badge>
            </div>
          </template>
          <p class="text-sm text-gray-300">Integrate with your existing systems using our comprehensive REST API and webhooks.</p>
        </Card>
        <Card>
          <template #header>
            <div class="flex items-center justify-between">
              <h3 class="font-semibold">Team Collaboration</h3>
              <Badge type="primary">Core</Badge>
            </div>
          </template>
          <p class="text-sm text-gray-300">Collaborate with your team on ticket classification rules and model improvements.</p>
        </Card>
      </FeatureGrid>
    `,
    }),
}

export const TwoColumns: Story = {
    render: () => ({
        components: {FeatureGrid, Card},
        template: `
      <FeatureGrid>
        <Card>
          <template #header>
            <h3 class="font-semibold">Fast</h3>
          </template>
          <p>Process thousands of tickets per second</p>
        </Card>
        <Card>
          <template #header>
            <h3 class="font-semibold">Accurate</h3>
          </template>
          <p>95%+ classification accuracy</p>
        </Card>
      </FeatureGrid>
    `,
    }),
}

