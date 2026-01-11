import {computed, reactive, readonly, toRefs} from 'vue'

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

    state.isLoading = true
    state.error = null

    try {
        // For SSR, we'll handle this differently
        // During build time (SSR), we skip loading the registry
        // It will be loaded on the client side
        if (typeof window === 'undefined') {
            // SSR - skip for now, will load on client
            state.isLoading = false
            return
        }
        
        // Client-side fetch
        const url = `/configExamples/registry.json`
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
