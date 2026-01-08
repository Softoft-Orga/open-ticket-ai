import {computed, reactive, readonly, toRefs} from 'vue'
import {useData} from 'vitepress'

export interface ExampleMeta {
    slug: string
    name: string
    tags: string[]
    md_description: string
    md_details?: string
    path: string
}

interface RegistryState {
    examples: ExampleMeta[]
    isLoading: boolean
    error: Error | null
}

const state = reactive<RegistryState>({
    examples: [],
    isLoading: false,
    error: null,
})

let hasFetched = false

async function fetchYaml(path: string) {
    if (!path) {
        return ''
    }
    const {site} = useData()

    const base = site.value?.base ?? '/'
    const normalizedBase = base.endsWith('/') ? base : `${base}/`
    const url = path.startsWith('/') ? `${normalizedBase}${path.slice(1)}` : `${normalizedBase}${path}`
    const response = await fetch(url)
    if (!response.ok) {
        throw new Error(`Failed to load example: ${response.status} ${response.statusText}`)
    }
    return await response.text()
}

async function createExampleMarkdownBody(example: ExampleMeta) {
    const yamlContent = await fetchYaml(example.path)
    const body = example.md_details && example.md_details.trim().length > 0
        ? example.md_details
        : example.md_description
    return `
${body}
::: details Yaml Configuration
\`\`\`yaml
${yamlContent}
\´\´\´
:::
`
}

const uniqueTags = computed(() => {
    const tags = new Set<string>()
    for (const example of state.examples) {
        for (const tag of example.tags) {
            tags.add(tag)
        }
    }
    return Array.from(tags).sort((a, b) => a.localeCompare(b))
})

async function loadRegistry() {
    if (hasFetched) {
        return
    }
    hasFetched = true

    const {site} = useData()
    const base = site.value?.base ?? '/'
    const normalizedBase = base.endsWith('/') ? base : `${base}/`
    const url = `${normalizedBase}configExamples/registry.json`

    state.isLoading = true
    state.error = null

    try {
        const response = await fetch(url)
        if (!response.ok) {
            throw new Error(`Failed to load registry: ${response.status} ${response.statusText}`)
        }
        state.examples = await response.json() as ExampleMeta[]
    } catch (error) {
        state.error = error as Error
        console.error('Failed to load configExamples registry', error)
    } finally {
        state.isLoading = false
    }
}

export function useConfigExamplesRegistry() {
    void loadRegistry()

    const stateRefs = toRefs(readonly(state))

    const findBySlug = (slug: string) => {
        return state.examples.find(example => example.slug === slug)
    }

    return {
        ...stateRefs,
        allTags: uniqueTags,
        findBySlug,
    }
}
