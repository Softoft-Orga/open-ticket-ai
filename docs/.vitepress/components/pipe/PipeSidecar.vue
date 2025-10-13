<template>
    <div class="pipe-sidecar bg-vp-bg-soft border border-vp-border rounded-lg overflow-hidden">
        <!-- Header Section -->
        <div class="bg-vp-bg p-6 border-b border-vp-border">
            <div class="flex items-start justify-between">
                <div class="flex-1">
                    <h2 class="text-2xl font-bold text-vp-text-1 mb-2">{{ sidecar._title }}</h2>
                    <p class="text-vp-text-2 mb-3">{{ sidecar._summary }}</p>
                    <div class="flex flex-wrap gap-2">
                        <span class="inline-flex items-center px-3 py-1 rounded-full text-xs font-medium bg-vp-brand text-white">
                            {{ sidecar._category }}
                        </span>
                        <span class="inline-flex items-center px-3 py-1 rounded-full text-xs font-medium bg-vp-bg-soft border border-vp-border text-vp-text-2">
                            {{ sidecar._version }}
                        </span>
                    </div>
                </div>
                <div v-if="$slots.actions" class="ml-4">
                    <slot name="actions" />
                </div>
            </div>
        </div>

        <!-- Content Section -->
        <div class="p-6 space-y-6">
            <!-- Metadata Section -->
            <section>
                <h3 class="text-lg font-semibold text-vp-text-1 mb-3">Metadata</h3>
                <dl class="grid grid-cols-1 gap-3 text-sm">
                    <div>
                        <dt class="font-medium text-vp-text-2">Class</dt>
                        <dd class="mt-1 text-vp-text-1 font-mono text-xs bg-vp-bg p-2 rounded">
                            {{ sidecar._class }}
                        </dd>
                    </div>
                    <div>
                        <dt class="font-medium text-vp-text-2">Extends</dt>
                        <dd class="mt-1 text-vp-text-1 font-mono text-xs bg-vp-bg p-2 rounded">
                            {{ sidecar._extends }}
                        </dd>
                    </div>
                </dl>
            </section>

            <!-- Inputs Section -->
            <section>
                <h3 class="text-lg font-semibold text-vp-text-1 mb-3">Inputs</h3>
                <div class="bg-vp-bg p-4 rounded-lg space-y-3">
                    <div>
                        <span class="font-medium text-vp-text-2 text-sm">Placement:</span>
                        <span class="ml-2 text-vp-text-1">{{ sidecar._inputs.placement }}</span>
                    </div>
                    <div v-if="sidecar._inputs.alongside">
                        <span class="font-medium text-vp-text-2 text-sm">Alongside:</span>
                        <span class="ml-2 text-vp-text-1">{{ sidecar._inputs.alongside.join(', ') }}</span>
                    </div>
                    <div v-if="sidecar._inputs.params">
                        <div class="font-medium text-vp-text-2 text-sm mb-2">Parameters:</div>
                        <dl class="ml-4 space-y-2">
                            <div v-for="(desc, param) in sidecar._inputs.params" :key="param" class="flex">
                                <dt class="font-mono text-xs text-vp-brand font-semibold min-w-[160px]">
                                    {{ param }}:
                                </dt>
                                <dd class="text-vp-text-1 text-sm">{{ desc }}</dd>
                            </div>
                        </dl>
                    </div>
                </div>
            </section>

            <!-- Defaults Section -->
            <section v-if="sidecar._defaults && Object.keys(sidecar._defaults).length > 0">
                <h3 class="text-lg font-semibold text-vp-text-1 mb-3">Defaults</h3>
                <div class="bg-vp-bg p-4 rounded-lg">
                    <dl class="space-y-2">
                        <div v-for="(value, key) in sidecar._defaults" :key="key" class="flex">
                            <dt class="font-mono text-xs text-vp-brand font-semibold min-w-[160px]">
                                {{ key }}:
                            </dt>
                            <dd class="text-vp-text-1 text-sm">{{ value }}</dd>
                        </div>
                    </dl>
                </div>
            </section>

            <!-- Output Section -->
            <section>
                <h3 class="text-lg font-semibold text-vp-text-1 mb-3">Output</h3>
                <div class="bg-vp-bg p-4 rounded-lg space-y-3">
                    <div>
                        <span class="font-medium text-vp-text-2 text-sm">Description:</span>
                        <p class="mt-1 text-vp-text-1">{{ sidecar._output.description }}</p>
                    </div>
                    <div>
                        <span class="font-medium text-vp-text-2 text-sm">State Enum:</span>
                        <div class="mt-2 flex flex-wrap gap-2">
                            <span
                                v-for="state in sidecar._output.state_enum"
                                :key="state"
                                class="inline-flex items-center px-2 py-1 rounded text-xs font-mono"
                                :class="getStateClass(state)"
                            >
                                {{ state }}
                            </span>
                        </div>
                    </div>
                    <div v-if="sidecar._output.payload_schema_ref">
                        <span class="font-medium text-vp-text-2 text-sm">Payload Schema:</span>
                        <span class="ml-2 text-vp-text-1 font-mono text-xs">
                            {{ sidecar._output.payload_schema_ref }}
                        </span>
                    </div>
                    
                    <!-- Output Examples -->
                    <div v-if="sidecar._output.examples">
                        <div class="font-medium text-vp-text-2 text-sm mb-2">Examples:</div>
                        <div class="space-y-2">
                            <AccordionItem
                                v-for="(example, state) in sidecar._output.examples"
                                :key="state"
                                :title="state"
                            >
                                <pre class="text-xs overflow-x-auto bg-vp-bg-soft p-3 rounded"><code>{{ JSON.stringify(example, null, 2) }}</code></pre>
                            </AccordionItem>
                        </div>
                    </div>
                </div>
            </section>

            <!-- Errors Section -->
            <section>
                <h3 class="text-lg font-semibold text-vp-text-1 mb-3">Errors</h3>
                <div class="space-y-4">
                    <div v-if="sidecar._errors.fail" class="bg-red-50 dark:bg-red-950/20 p-4 rounded-lg border border-red-200 dark:border-red-800">
                        <h4 class="font-semibold text-red-900 dark:text-red-300 mb-2 text-sm">Fail (Pipeline Stops)</h4>
                        <ul class="space-y-2">
                            <li v-for="(error, idx) in sidecar._errors.fail" :key="idx" class="text-sm">
                                <span class="font-mono text-xs text-red-700 dark:text-red-400 font-semibold">
                                    {{ error.code }}:
                                </span>
                                <span class="ml-2 text-red-800 dark:text-red-300">{{ error.when }}</span>
                            </li>
                        </ul>
                    </div>
                    
                    <div v-if="sidecar._errors.break" class="bg-orange-50 dark:bg-orange-950/20 p-4 rounded-lg border border-orange-200 dark:border-orange-800">
                        <h4 class="font-semibold text-orange-900 dark:text-orange-300 mb-2 text-sm">Break (Pipeline Interrupted)</h4>
                        <ul class="space-y-2">
                            <li v-for="(error, idx) in sidecar._errors.break" :key="idx" class="text-sm">
                                <span class="font-mono text-xs text-orange-700 dark:text-orange-400 font-semibold">
                                    {{ error.code }}:
                                </span>
                                <span class="ml-2 text-orange-800 dark:text-orange-300">{{ error.when }}</span>
                            </li>
                        </ul>
                    </div>
                    
                    <div v-if="sidecar._errors.continue" class="bg-yellow-50 dark:bg-yellow-950/20 p-4 rounded-lg border border-yellow-200 dark:border-yellow-800">
                        <h4 class="font-semibold text-yellow-900 dark:text-yellow-300 mb-2 text-sm">Continue (Skipped, Pipeline Continues)</h4>
                        <ul class="space-y-2">
                            <li v-for="(error, idx) in sidecar._errors.continue" :key="idx" class="text-sm">
                                <span class="font-mono text-xs text-yellow-700 dark:text-yellow-400 font-semibold">
                                    {{ error.code }}:
                                </span>
                                <span class="ml-2 text-yellow-800 dark:text-yellow-300">{{ error.when }}</span>
                            </li>
                        </ul>
                    </div>
                </div>
            </section>

            <!-- Engine Support Section -->
            <section>
                <h3 class="text-lg font-semibold text-vp-text-1 mb-3">Engine Support</h3>
                <div class="bg-vp-bg p-4 rounded-lg">
                    <dl class="space-y-2">
                        <div class="flex items-center">
                            <dt class="font-medium text-vp-text-2 text-sm min-w-[160px]">On Failure:</dt>
                            <dd>
                                <span
                                    class="inline-flex items-center px-2 py-1 rounded text-xs font-semibold"
                                    :class="sidecar._engine_support.on_failure ? 'bg-green-100 dark:bg-green-900/30 text-green-800 dark:text-green-300' : 'bg-gray-100 dark:bg-gray-800 text-gray-600 dark:text-gray-400'"
                                >
                                    {{ sidecar._engine_support.on_failure ? 'Supported' : 'Not Supported' }}
                                </span>
                            </dd>
                        </div>
                        <div class="flex items-center">
                            <dt class="font-medium text-vp-text-2 text-sm min-w-[160px]">On Success:</dt>
                            <dd>
                                <span
                                    class="inline-flex items-center px-2 py-1 rounded text-xs font-semibold"
                                    :class="sidecar._engine_support.on_success ? 'bg-green-100 dark:bg-green-900/30 text-green-800 dark:text-green-300' : 'bg-gray-100 dark:bg-gray-800 text-gray-600 dark:text-gray-400'"
                                >
                                    {{ sidecar._engine_support.on_success ? 'Supported' : 'Not Supported' }}
                                </span>
                            </dd>
                        </div>
                    </dl>
                </div>
            </section>

            <!-- Examples Section -->
            <section>
                <h3 class="text-lg font-semibold text-vp-text-1 mb-3">Usage Examples</h3>
                <div class="space-y-3">
                    <AccordionItem
                        v-for="(example, name) in sidecar._examples"
                        :key="name"
                        :title="capitalizeFirst(name)"
                    >
                        <pre class="text-xs overflow-x-auto bg-vp-bg-soft p-4 rounded border border-vp-border"><code>{{ example }}</code></pre>
                    </AccordionItem>
                </div>
            </section>
        </div>
    </div>
</template>

<script lang="ts" setup>
import AccordionItem from '../core/accordion/AccordionItem.vue'
import type { PipeSidecar } from './pipeSidecar.types'

defineProps<{
    sidecar: PipeSidecar
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

const capitalizeFirst = (str: string): string => {
    return str.charAt(0).toUpperCase() + str.slice(1)
}
</script>

<style scoped>
.pipe-sidecar {
    max-width: 100%;
}
</style>
