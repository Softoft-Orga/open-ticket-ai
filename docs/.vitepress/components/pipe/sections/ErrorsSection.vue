<template>
    <section>
        <h3 class="text-lg font-semibold text-vp-text-1 mb-3">Errors</h3>
        <div class="space-y-4">
            <div v-if="errors.fail" class="bg-red-50 dark:bg-red-950/20 p-4 rounded-lg border border-red-200 dark:border-red-800">
                <h4 class="font-semibold text-red-900 dark:text-red-300 mb-2 text-sm">Fail (Pipeline Stops)</h4>
                <ul class="space-y-2">
                    <li v-for="(error, idx) in errors.fail" :key="idx" class="text-sm">
                        <span class="font-mono text-xs text-red-700 dark:text-red-400 font-semibold">
                            {{ error.code }}:
                        </span>
                        <span class="ml-2 text-red-800 dark:text-red-300">{{ error.when }}</span>
                    </li>
                </ul>
            </div>
            
            <div v-if="errors.break" class="bg-orange-50 dark:bg-orange-950/20 p-4 rounded-lg border border-orange-200 dark:border-orange-800">
                <h4 class="font-semibold text-orange-900 dark:text-orange-300 mb-2 text-sm">Break (Pipeline Interrupted)</h4>
                <ul class="space-y-2">
                    <li v-for="(error, idx) in errors.break" :key="idx" class="text-sm">
                        <span class="font-mono text-xs text-orange-700 dark:text-orange-400 font-semibold">
                            {{ error.code }}:
                        </span>
                        <span class="ml-2 text-orange-800 dark:text-orange-300">{{ error.when }}</span>
                    </li>
                </ul>
            </div>
            
            <div v-if="errors.continue" class="bg-yellow-50 dark:bg-yellow-950/20 p-4 rounded-lg border border-yellow-200 dark:border-yellow-800">
                <h4 class="font-semibold text-yellow-900 dark:text-yellow-300 mb-2 text-sm">Continue (Skipped, Pipeline Continues)</h4>
                <ul class="space-y-2">
                    <li v-for="(error, idx) in errors.continue" :key="idx" class="text-sm">
                        <span class="font-mono text-xs text-yellow-700 dark:text-yellow-400 font-semibold">
                            {{ error.code }}:
                        </span>
                        <span class="ml-2 text-yellow-800 dark:text-yellow-300">{{ error.when }}</span>
                    </li>
                </ul>
            </div>
        </div>
    </section>
</template>

<script lang="ts" setup>
import type { PipeSidecarErrors } from '../pipeSidecar.types'

defineProps<{
    errors: PipeSidecarErrors
}>()
</script>
