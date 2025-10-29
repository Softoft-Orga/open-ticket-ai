import {reactive, readonly, toRefs} from 'vue'
import type {PipeSidecar} from '../components/pipe/pipeSidecar.types'

export type SidecarType = 'pipe' | 'service' | 'trigger'

export interface SidecarEntry {
    name: string
    type: SidecarType
    path: string
    data: PipeSidecar
}

const state = reactive({
    sidecars: new Map<string, SidecarEntry>(),
    isLoading: false,
    error: null as Error | null,
})

let hasFetched = false

async function fetchAndProcessSidecars() {
    if (hasFetched) {
        return
    }
    hasFetched = true

    state.isLoading = true
    try {
        // Fetch the sidecar index/manifest (to be created)
        const response = await fetch('/assets/sidecars.json')
        if (!response.ok) {
            throw new Error(`Failed to fetch sidecars: ${response.statusText}`)
        }
        const sidecarsData: SidecarEntry[] = await response.json()

        const tempSidecars = new Map<string, SidecarEntry>()

        for (const entry of sidecarsData) {
            const key = `${entry.type}:${entry.name}`
            tempSidecars.set(key, entry)
        }

        state.sidecars = tempSidecars
    } catch (e) {
        state.error = e as Error
        console.error('Failed to load sidecars:', e)
    } finally {
        state.isLoading = false
    }
}

export function useSidecars() {
    fetchAndProcessSidecars()

    const getSidecar = (type: SidecarType, name: string): SidecarEntry | undefined => {
        return state.sidecars.get(`${type}:${name}`)
    }

    const filterByType = (type: SidecarType): SidecarEntry[] => {
        return Array.from(state.sidecars.values()).filter(entry => entry.type === type)
    }

    const filterByCategory = (category: string): SidecarEntry[] => {
        return Array.from(state.sidecars.values()).filter(
            entry => entry.data._category === category
        )
    }

    const getAllSidecars = (): SidecarEntry[] => {
        return Array.from(state.sidecars.values())
    }

    return {
        ...toRefs(readonly(state)),
        getSidecar,
        filterByType,
        filterByCategory,
        getAllSidecars,
    }
}
