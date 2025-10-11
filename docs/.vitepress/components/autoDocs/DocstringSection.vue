<script lang="ts" setup>

const {title} = defineProps<{
    title: string
}>();
</script>

<template>
    <h4 class="text-sm font-semibold mb-3 uppercase tracking-wider text-vp-text-2">{{ title }}</h4>
    <div class="flex flex-col gap-5 p-2">
        <slot/>
    </div>
</template>

<style scoped>

</style>
