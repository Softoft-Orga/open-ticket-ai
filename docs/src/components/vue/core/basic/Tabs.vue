<template>
  <div>
    <div 
      class="flex border-b border-vp-border" 
      role="tablist"
      aria-label="Tabs"
    >
      <button
          v-for="(label, idx) in tabs"
          :key="idx"
          :id="`tab-${idx}`"
          :class="[
          'px-4 py-2 -mb-px focus:outline-none focus-visible:ring-2 focus-visible:ring-blue-400',
          activeIndex === idx
            ? 'border-b-2 text-vp-brand border-vp-brand font-semibold'
            : 'text-vp-text-2 hover:text-vp-brand'
        ]"
          :aria-selected="activeIndex === idx"
          :tabindex="activeIndex === idx ? 0 : -1"
          role="tab"
          @click="selectTab(idx)"
          @keydown="handleKeydown($event, idx)"
      >
        {{ label }}
      </button>
    </div>
    <div 
      class="mt-4"
      :id="`tabpanel-${activeIndex}`"
      role="tabpanel"
      :aria-labelledby="`tab-${activeIndex}`"
    >
      <slot :name="`tab-${activeIndex}`"/>
    </div>
  </div>
</template>

<script lang="ts" setup>
import {ref, watch} from 'vue'

interface Props {
  tabs: string[]
  modelValue?: number
}

const props = withDefaults(defineProps<Props>(), {
  modelValue: 0
})

const emit = defineEmits<{
  (e: 'update:modelValue', value: number): void
}>()

const activeIndex = ref(props.modelValue)

watch(() => props.modelValue, (newValue) => {
  activeIndex.value = newValue
})

function selectTab(index: number) {
  activeIndex.value = index
  emit('update:modelValue', index)
}

function handleKeydown(event: KeyboardEvent, currentIndex: number) {
  let newIndex = currentIndex
  
  switch (event.key) {
    case 'ArrowLeft':
      event.preventDefault()
      newIndex = currentIndex > 0 ? currentIndex - 1 : props.tabs.length - 1
      break
    case 'ArrowRight':
      event.preventDefault()
      newIndex = currentIndex < props.tabs.length - 1 ? currentIndex + 1 : 0
      break
    case 'Home':
      event.preventDefault()
      newIndex = 0
      break
    case 'End':
      event.preventDefault()
      newIndex = props.tabs.length - 1
      break
    default:
      return
  }
  
  selectTab(newIndex)
  
  const targetTab = document.getElementById(`tab-${newIndex}`)
  targetTab?.focus()
}
</script>
