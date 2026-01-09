<template>
  <div class="flex items-center gap-2 text-sm text-text-dim">
    <span class="material-symbols-outlined text-base">schedule</span>
    <span>{{ readingTime }} min read</span>
  </div>
</template>

<script lang="ts" setup>
import { computed } from 'vue'

interface Props {
  text?: string
  wordsPerMinute?: number
}

const props = withDefaults(defineProps<Props>(), {
  wordsPerMinute: 200
})

const readingTime = computed(() => {
  if (!props.text) return 1
  
  const words = props.text.trim().split(/\s+/).length
  const minutes = Math.ceil(words / props.wordsPerMinute)
  
  return minutes
})
</script>
