<template>
  <div class="flex flex-wrap items-center gap-3">
    <button
      v-for="tag in allTags"
      :key="tag"
      :class="[
        'rounded-full border px-4 py-2 text-sm font-medium transition-all',
        selectedTags.includes(tag)
          ? 'border-primary bg-primary text-white'
          : 'border-surface-lighter bg-surface-dark text-text-dim hover:border-primary/50 hover:text-white'
      ]"
      @click="toggleTag(tag)"
    >
      {{ tag }}
    </button>
  </div>
</template>

<script lang="ts" setup>
import { ref, watch } from 'vue'

interface Props {
  tags: string[]
  modelValue?: string[]
}

const props = withDefaults(defineProps<Props>(), {
  modelValue: () => []
})

const emit = defineEmits<{
  'update:modelValue': [value: string[]]
}>()

const allTags = ref(props.tags)
const selectedTags = ref<string[]>([...props.modelValue])

const toggleTag = (tag: string) => {
  const index = selectedTags.value.indexOf(tag)
  if (index > -1) {
    selectedTags.value.splice(index, 1)
  } else {
    selectedTags.value.push(tag)
  }
  emit('update:modelValue', selectedTags.value)
}

watch(() => props.modelValue, (newValue) => {
  selectedTags.value = [...newValue]
})
</script>
