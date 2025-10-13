<template>
    <section v-if="defaults && Object.keys(defaults).length > 0">
        <h3 class="text-lg font-semibold text-vp-text-1 mb-3">Defaults</h3>
        <div class="bg-vp-bg p-4 rounded-lg">
            <dl class="space-y-2">
                <div v-for="(value, key) in defaults" :key="key" class="flex">
                    <dt class="font-mono text-xs text-vp-brand font-semibold min-w-[160px]">
                        {{ key }}:
                    </dt>
                    <dd class="text-vp-text-1 text-sm">{{ value }}</dd>
                </div>
            </dl>
        </div>
    </section>
</template>

<script lang="ts" setup>
defineProps<{
    defaults?: Record<string, any>
}>()
</script>
