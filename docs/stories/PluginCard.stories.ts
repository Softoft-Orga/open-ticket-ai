import PluginCard from '../src/components/vue/marketplace/PluginCard.vue'
import type {Meta, StoryObj} from '@storybook/vue3'
import type {Plugin} from '../src/components/vue/marketplace/pluginModels'

const meta: Meta<typeof PluginCard> = {
    title: 'Marketplace/PluginCard',
    component: PluginCard,
    argTypes: {
        plugin: {
            control: 'object',
            description: 'Plugin data object'
        },
        formattedDate: {
            control: 'text',
            description: 'Formatted release date string'
        }
    },
    parameters: {
        docs: {
            description: {
                component: 'Card component displaying plugin information including name, version, summary, stats, and installation command.'
            }
        }
    }
}
export default meta

type Story = StoryObj<typeof meta>

const samplePlugin: Plugin = {
    name: 'otai-classifier-example',
    version: '1.2.3',
    summary: 'An example classifier plugin for Open Ticket AI that demonstrates integration patterns and best practices.',
    homepage: 'https://example.com',
    pypiUrl: 'https://pypi.org/project/otai-classifier-example/',
    repositoryUrl: 'https://github.com/example/otai-classifier-example',
    lastReleaseDate: '2024-01-15T10:30:00Z',
    starCount: 127,
    author: 'Example Developer',
    license: 'MIT',
    releaseFiles: []
}

const minimalPlugin: Plugin = {
    name: 'minimal-plugin',
    version: '0.1.0',
    summary: 'A minimal plugin with no extra metadata.',
    homepage: null,
    pypiUrl: 'https://pypi.org/project/minimal-plugin/',
    repositoryUrl: null,
    lastReleaseDate: '2023-12-01T00:00:00Z',
    starCount: 5,
    author: null,
    license: null,
    releaseFiles: []
}

export const Default: Story = {
    render: (args) => ({
        components: {PluginCard},
        setup() {
            return {args}
        },
        template: '<div class="max-w-md bg-slate-950 p-4"><PluginCard v-bind="args" /></div>'
    }),
    args: {
        plugin: samplePlugin,
        formattedDate: '15 Jan 2024'
    },
    parameters: {
        backgrounds: { default: 'dark' }
    }
}

export const MinimalMetadata: Story = {
    render: (args) => ({
        components: {PluginCard},
        setup() {
            return {args}
        },
        template: '<div class="max-w-md bg-slate-950 p-4"><PluginCard v-bind="args" /></div>'
    }),
    args: {
        plugin: minimalPlugin,
        formattedDate: '1 Dec 2023'
    },
    parameters: {
        backgrounds: { default: 'dark' }
    }
}

export const HighStarCount: Story = {
    render: (args) => ({
        components: {PluginCard},
        setup() {
            return {args}
        },
        template: '<div class="max-w-md bg-slate-950 p-4"><PluginCard v-bind="args" /></div>'
    }),
    args: {
        plugin: {
            ...samplePlugin,
            starCount: 1543,
            summary: 'A very popular plugin with lots of stars and active community support.'
        },
        formattedDate: '2 days ago'
    },
    parameters: {
        backgrounds: { default: 'dark' }
    }
}
