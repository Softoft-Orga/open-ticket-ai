import CodeTabs from '../src/components/vue/docs/CodeTabs.vue'
import type { Meta, StoryObj } from '@storybook/vue3'

const meta: Meta<typeof CodeTabs> = {
  title: 'Docs/CodeTabs',
  component: CodeTabs,
  tags: ['autodocs'],
  parameters: {
    docs: {
      description: {
        component: 'Tabbed container component for displaying multiple code examples or variations in documentation.'
      }
    }
  }
}
export default meta

type Story = StoryObj<typeof meta>

export const LanguageExamples: Story = {
  render: (args) => ({
    components: { CodeTabs },
    setup() {
      return { args }
    },
    template: `
      <CodeTabs v-bind="args">
        <template #tab-0>
          <pre class="text-sm font-mono text-white">const api = new OpenTicketAI({
  apiKey: 'your-api-key'
});

const result = await api.classify(ticket);</pre>
        </template>
        <template #tab-1>
          <pre class="text-sm font-mono text-white">api = OpenTicketAI(api_key='your-api-key')

result = api.classify(ticket)</pre>
        </template>
        <template #tab-2>
          <pre class="text-sm font-mono text-white">package main

import "github.com/openticketai/sdk-go"

func main() {
    api := openticketai.New("your-api-key")
    result := api.Classify(ticket)
}</pre>
        </template>
      </CodeTabs>
    `
  }),
  args: {
    tabs: ['JavaScript', 'Python', 'Go']
  }
}

export const ConfigExamples: Story = {
  render: (args) => ({
    components: { CodeTabs },
    setup() {
      return { args }
    },
    template: `
      <CodeTabs v-bind="args">
        <template #tab-0>
          <pre class="text-sm font-mono text-white">{
  "model": "gpt-4",
  "temperature": 0.7,
  "maxTokens": 1000
}</pre>
        </template>
        <template #tab-1>
          <pre class="text-sm font-mono text-white">model: gpt-4
temperature: 0.7
maxTokens: 1000</pre>
        </template>
        <template #tab-2>
          <pre class="text-sm font-mono text-white">model = "gpt-4"
temperature = 0.7
maxTokens = 1000</pre>
        </template>
      </CodeTabs>
    `
  }),
  args: {
    tabs: ['JSON', 'YAML', 'TOML']
  }
}

export const TwoTabs: Story = {
  render: (args) => ({
    components: { CodeTabs },
    setup() {
      return { args }
    },
    template: `
      <CodeTabs v-bind="args">
        <template #tab-0>
          <div class="text-white">
            <h4 class="mb-2 font-semibold">Development Setup</h4>
            <pre class="text-sm font-mono">npm install
npm run dev</pre>
          </div>
        </template>
        <template #tab-1>
          <div class="text-white">
            <h4 class="mb-2 font-semibold">Production Build</h4>
            <pre class="text-sm font-mono">npm run build
npm run preview</pre>
          </div>
        </template>
      </CodeTabs>
    `
  }),
  args: {
    tabs: ['Development', 'Production']
  }
}
