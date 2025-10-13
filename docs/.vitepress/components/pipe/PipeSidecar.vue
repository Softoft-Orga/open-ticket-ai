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
            <MetadataSection :sidecar-class="sidecar._class" :extends_="sidecar._extends" />
            <InputsSection :inputs="sidecar._inputs" />
            <DefaultsSection :defaults="sidecar._defaults" />
            <OutputSection :output="sidecar._output" />
            <ErrorsSection :errors="sidecar._errors" />
            <EngineSupportSection :engine-support="sidecar._engine_support" />
            <ExamplesSection :examples="sidecar._examples" />
        </div>
    </div>
</template>

<script lang="ts" setup>
import MetadataSection from './sections/MetadataSection.vue'
import InputsSection from './sections/InputsSection.vue'
import DefaultsSection from './sections/DefaultsSection.vue'
import OutputSection from './sections/OutputSection.vue'
import ErrorsSection from './sections/ErrorsSection.vue'
import EngineSupportSection from './sections/EngineSupportSection.vue'
import ExamplesSection from './sections/ExamplesSection.vue'
import type { PipeSidecar } from './pipeSidecar.types'

defineProps<{
    sidecar: PipeSidecar
}>()
</script>

<style scoped>
.pipe-sidecar {
    max-width: 100%;
}
</style>
