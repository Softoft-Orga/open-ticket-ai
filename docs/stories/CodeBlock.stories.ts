import CodeBlock from '../src/components/vue/docs/CodeBlock.vue'
import type { Meta, StoryObj } from '@storybook/vue3'

const meta: Meta<typeof CodeBlock> = {
  title: 'Docs/CodeBlock',
  component: CodeBlock,
  tags: ['autodocs'],
  parameters: {
    docs: {
      description: {
        component: 'Code block component with syntax highlighting support and a copy-to-clipboard button.'
      }
    }
  }
}
export default meta

type Story = StoryObj<typeof meta>

export const JavaScript: Story = {
  render: (args) => ({
    components: { CodeBlock },
    setup() {
      return { args }
    },
    template: `
      <CodeBlock v-bind="args">const greeting = 'Hello, World!';
console.log(greeting);</CodeBlock>
    `
  }),
  args: {
    language: 'javascript',
    title: 'Example Script'
  }
}

export const Python: Story = {
  render: (args) => ({
    components: { CodeBlock },
    setup() {
      return { args }
    },
    template: `
      <CodeBlock v-bind="args">def hello_world():
    print("Hello, World!")
    
hello_world()</CodeBlock>
    `
  }),
  args: {
    language: 'python'
  }
}

export const WithoutHeader: Story = {
  render: (args) => ({
    components: { CodeBlock },
    setup() {
      return { args }
    },
    template: `
      <CodeBlock v-bind="args">npm install open-ticket-ai
npm start</CodeBlock>
    `
  }),
  args: {}
}

export const LongCode: Story = {
  render: (args) => ({
    components: { CodeBlock },
    setup() {
      return { args }
    },
    template: `
      <CodeBlock v-bind="args">import { defineConfig } from 'astro/config';
import vue from '@astrojs/vue';
import mdx from '@astrojs/mdx';

export default defineConfig({
  site: 'https://openticketai.com',
  base: '/',
  outDir: './dist',
  trailingSlash: 'always',
  integrations: [
    vue({
      appEntrypoint: '/src/vue-app.js'
    }),
    mdx(),
  ],
});</CodeBlock>
    `
  }),
  args: {
    language: 'typescript',
    title: 'astro.config.mjs'
  }
}

export const Bash: Story = {
  render: (args) => ({
    components: { CodeBlock },
    setup() {
      return { args }
    },
    template: `
      <CodeBlock v-bind="args">git clone https://github.com/example/repo.git
cd repo
npm install
npm run dev</CodeBlock>
    `
  }),
  args: {
    language: 'bash',
    title: 'Installation Commands'
  }
}
