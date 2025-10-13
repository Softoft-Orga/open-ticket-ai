<template>
    <section>
        <h3 class="text-lg font-semibold text-vp-text-1 mb-3">Usage Examples</h3>
        <div class="space-y-3">
            <AccordionItem
                v-for="(example, name) in examples"
                :key="name"
                :title="capitalizeFirst(name)"
            >
                <pre class="text-xs overflow-x-auto bg-vp-bg-soft p-4 rounded border border-vp-border"><code>{{ example }}</code></pre>
            </AccordionItem>
        </div>
    </section>
</template>

<script lang="ts" setup>
import AccordionItem from '../../core/accordion/AccordionItem.vue'

defineProps<{
    examples: Record<string, string>
}>()

const capitalizeFirst = (str: string): string => {
    return str.charAt(0).toUpperCase() + str.slice(1)
}
</script>
