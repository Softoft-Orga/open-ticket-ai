<template>
    <section>
        <h3 class="text-lg font-semibold text-vp-text-1 mb-3">Output</h3>
        <div class="bg-vp-bg p-4 rounded-lg space-y-3">
            <div>
                <span class="font-medium text-vp-text-2 text-sm">Description:</span>
                <p class="mt-1 text-vp-text-1">{{ output.description }}</p>
            </div>
            <div>
                <span class="font-medium text-vp-text-2 text-sm">State Enum:</span>
                <div class="mt-2 flex flex-wrap gap-2">
                    <span
                        v-for="state in output.state_enum"
                        :key="state"
                        class="inline-flex items-center px-2 py-1 rounded text-xs font-mono"
                        :class="getStateClass(state)"
                    >
                        {{ state }}
                    </span>
                </div>
            </div>
            <div v-if="output.payload_schema_ref">
                <span class="font-medium text-vp-text-2 text-sm">Payload Schema:</span>
                <span class="ml-2 text-vp-text-1 font-mono text-xs">
                    {{ output.payload_schema_ref }}
                </span>
            </div>
            
            <div v-if="output.examples">
                <div class="font-medium text-vp-text-2 text-sm mb-2">Examples:</div>
                <div class="space-y-2">
                    <AccordionItem
                        v-for="(example, state) in output.examples"
                        :key="state"
                        :title="state"
                    >
                        <pre class="text-xs overflow-x-auto bg-vp-bg-soft p-3 rounded"><code>{{ JSON.stringify(example, null, 2) }}</code></pre>
                    </AccordionItem>
                </div>
            </div>
        </div>
    </section>
</template>

<script lang="ts" setup>
import AccordionItem from '../../core/accordion/AccordionItem.vue'
import type { PipeSidecarOutput } from '../pipeSidecar.types'

defineProps<{
    output: PipeSidecarOutput
}>()

const getStateClass = (state: string): string => {
    switch (state.toLowerCase()) {
        case 'ok':
            return 'bg-green-100 dark:bg-green-900/30 text-green-800 dark:text-green-300'
        case 'failed':
            return 'bg-red-100 dark:bg-red-900/30 text-red-800 dark:text-red-300'
        case 'skipped':
            return 'bg-yellow-100 dark:bg-yellow-900/30 text-yellow-800 dark:text-yellow-300'
        default:
            return 'bg-gray-100 dark:bg-gray-800 text-gray-600 dark:text-gray-400'
    }
}
</script>
