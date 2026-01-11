<template>
  <div class="flex items-center gap-2 text-sm text-text-dim">
    <ClockIcon
      class="w-4 h-4"
      aria-hidden="true"
    />
    <span>{{ readingTime }} min read</span>
  </div>
</template>

<script lang="ts" setup>
import { computed } from 'vue'
import { ClockIcon } from '@heroicons/vue/24/outline'

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
