<template>
    <section>
        <h3 class="text-lg font-semibold text-vp-text-1 mb-3">Engine Support</h3>
        <div class="bg-vp-bg p-4 rounded-lg">
            <dl class="space-y-2">
                <div class="flex items-center">
                    <dt class="font-medium text-vp-text-2 text-sm min-w-[160px]">On Failure:</dt>
                    <dd>
                        <span
                            class="inline-flex items-center px-2 py-1 rounded text-xs font-semibold"
                            :class="engineSupport.on_failure ? 'bg-green-100 dark:bg-green-900/30 text-green-800 dark:text-green-300' : 'bg-gray-100 dark:bg-gray-800 text-gray-600 dark:text-gray-400'"
                        >
                            {{ engineSupport.on_failure ? 'Supported' : 'Not Supported' }}
                        </span>
                    </dd>
                </div>
                <div class="flex items-center">
                    <dt class="font-medium text-vp-text-2 text-sm min-w-[160px]">On Success:</dt>
                    <dd>
                        <span
                            class="inline-flex items-center px-2 py-1 rounded text-xs font-semibold"
                            :class="engineSupport.on_success ? 'bg-green-100 dark:bg-green-900/30 text-green-800 dark:text-green-300' : 'bg-gray-100 dark:bg-gray-800 text-gray-600 dark:text-gray-400'"
                        >
                            {{ engineSupport.on_success ? 'Supported' : 'Not Supported' }}
                        </span>
                    </dd>
                </div>
            </dl>
        </div>
    </section>
</template>

<script lang="ts" setup>
import type { PipeSidecarEngineSupport } from '../pipeSidecar.types'

defineProps<{
    engineSupport: PipeSidecarEngineSupport
}>()
</script>
