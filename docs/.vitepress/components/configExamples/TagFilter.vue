<template>
  <div class="flex flex-wrap gap-2">
    <button
      v-for="tag in tagsWithAll"
      :key="tag"
      :class="buttonClass(tag)"
      type="button"
      @click="() => emit('update:selected', tag)"
    >
      {{ tag }}
    </button>
  </div>
</template>

<script lang="ts" setup>
import {computed} from 'vue'

const props = defineProps<{ tags: string[]; selected: string }>()
const emit = defineEmits<{ 'update:selected': [value: string] }>()

const tagsWithAll = computed(() => ['All', ...props.tags])

function buttonClass(tag: string) {
  const isActive = tag === props.selected
  return [
    'rounded-full border px-4 py-1 text-xs font-medium transition focus:outline-none focus-visible:ring-2 focus-visible:ring-[color:var(--vp-c-brand-1)]',
    isActive
      ? 'bg-[color:var(--vp-c-brand-1)] text-white border-transparent shadow-sm'
      : 'bg-[color:var(--vp-c-bg-soft)] text-[color:var(--vp-c-text-2)] border-[color:var(--vp-c-divider)] hover:text-[color:var(--vp-c-text-1)]'
  ]
}
</script>
