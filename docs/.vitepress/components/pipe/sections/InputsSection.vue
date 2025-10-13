<template>
    <section>
        <h3 class="text-lg font-semibold text-vp-text-1 mb-3">Inputs</h3>
        <div class="bg-vp-bg p-4 rounded-lg space-y-3">
            <div>
                <span class="font-medium text-vp-text-2 text-sm">Placement:</span>
                <span class="ml-2 text-vp-text-1">{{ inputs.placement }}</span>
            </div>
            <div v-if="inputs.alongside">
                <span class="font-medium text-vp-text-2 text-sm">Alongside:</span>
                <span class="ml-2 text-vp-text-1">{{ inputs.alongside.join(', ') }}</span>
            </div>
            <div v-if="inputs.params">
                <div class="font-medium text-vp-text-2 text-sm mb-2">Parameters:</div>
                <dl class="ml-4 space-y-2">
                    <div v-for="(desc, param) in inputs.params" :key="param" class="flex">
                        <dt class="font-mono text-xs text-vp-brand font-semibold min-w-[160px]">
                            {{ param }}:
                        </dt>
                        <dd class="text-vp-text-1 text-sm">{{ desc }}</dd>
                    </div>
                </dl>
            </div>
        </div>
    </section>
</template>

<script lang="ts" setup>
import type { PipeSidecarInput } from '../pipeSidecar.types'

defineProps<{
    inputs: PipeSidecarInput
}>()
</script>
