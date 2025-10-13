<template>
    <section>
        <h3 class="text-lg font-semibold text-vp-text-1 mb-3">Metadata</h3>
        <dl class="grid grid-cols-1 gap-3 text-sm">
            <div>
                <dt class="font-medium text-vp-text-2">Class</dt>
                <dd class="mt-1 text-vp-text-1 font-mono text-xs bg-vp-bg p-2 rounded">
                    {{ sidecarClass }}
                </dd>
            </div>
            <div>
                <dt class="font-medium text-vp-text-2">Extends</dt>
                <dd class="mt-1 text-vp-text-1 font-mono text-xs bg-vp-bg p-2 rounded">
                    {{ extends_ }}
                </dd>
            </div>
        </dl>
    </section>
</template>

<script lang="ts" setup>
defineProps<{
    sidecarClass: string
    extends_: string
}>()
</script>
