<template>
  <a :href="href">
    <slot/>
  </a>
</template>

<script lang="ts" setup>
import {computed} from 'vue'
// Import the official helper from VitePress
import {useData} from 'vitepress'

const {lang} = useData()
const props = defineProps<{
  to: string
}>()

// Use the withBase helper to create the final URL
const href = computed(() => `/${lang.value}${props.to}`)
</script>
