<template>
    <div class="divide-y divide-vp-border">
        <AccordionItem v-for="(it, i) in items" :key="i" :title="it.title">
            {{ it.content }}
        </AccordionItem>
    </div>
</template>

<script lang="ts" setup>
import AccordionItem from './AccordionItem.vue'
interface Item {
    title: string
    content?: string
}

const {items = []} = defineProps<{
    items?: Item[],
}>()
</script>
