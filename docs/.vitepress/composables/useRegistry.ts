import {computed, reactive, readonly, toRefs} from 'vue'
import {useData} from 'vitepress'

export interface ExampleMeta {
    slug: string
    name: string
    tags: string[]
    description: string
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
    const url = `${normalizedBase}examples/registry.json`

    state.isLoading = true
    state.error = null

    try {
        const response = await fetch(url)
        if (!response.ok) {
            throw new Error(`Failed to load registry: ${response.status} ${response.statusText}`)
        }
        const data = await response.json() as ExampleMeta[]
        state.examples = data
    } catch (error) {
        state.error = error as Error
        console.error('Failed to load examples registry', error)
    } finally {
        state.isLoading = false
    }
}

export function useRegistry() {
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
