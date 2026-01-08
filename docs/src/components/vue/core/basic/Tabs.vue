<template>
  <div>
    <div 
      class="flex border-b border-vp-border"
      role="tablist"
      :aria-label="ariaLabel"
    >
      <button
          v-for="(label, idx) in tabs"
          :key="idx"
          :id="`tab-${uid}-${idx}`"
          :class="[
          'px-4 py-2 -mb-px focus:outline-none focus-visible:ring-2 focus-visible:ring-vp-brand',
          activeIndex === idx
            ? 'border-b-2 text-vp-brand border-vp-brand'
            : 'text-vp-text-2 hover:text-vp-text-1'
        ]"
          role="tab"
          :aria-selected="activeIndex === idx"
          :aria-controls="`tabpanel-${uid}-${idx}`"
          :tabindex="activeIndex === idx ? 0 : -1"
          @click="selectTab(idx)"
          @keydown="handleKeydown($event, idx)"
      >
        {{ label }}
      </button>
    </div>
    <div 
      v-for="(label, idx) in tabs"
      :key="`panel-${idx}`"
      v-show="activeIndex === idx"
      :id="`tabpanel-${uid}-${idx}`"
      class="mt-4"
      role="tabpanel"
      :aria-labelledby="`tab-${uid}-${idx}`"
      tabindex="0"
    >
      <slot :name="`tab-${idx}`"/>
    </div>
  </div>
</template>

<script lang="ts" setup>
import {ref, computed, watch} from 'vue'

interface Props {
  tabs: string[]
  modelValue?: number
  ariaLabel?: string
}

const props = withDefaults(defineProps<Props>(), {
  modelValue: 0,
  ariaLabel: 'Tabs'
})

const emit = defineEmits<{
  (e: 'update:modelValue', value: number): void
}>()

const uid = Math.random().toString(36).substr(2, 9)
const activeIndex = ref(props.modelValue)

watch(() => props.modelValue, (newVal) => {
  activeIndex.value = newVal
})

const selectTab = (idx: number) => {
  activeIndex.value = idx
  emit('update:modelValue', idx)
}

const handleKeydown = (event: KeyboardEvent, currentIdx: number) => {
  let newIdx = currentIdx
  
  switch (event.key) {
    case 'ArrowLeft':
      event.preventDefault()
      newIdx = currentIdx > 0 ? currentIdx - 1 : props.tabs.length - 1
      break
    case 'ArrowRight':
      event.preventDefault()
      newIdx = currentIdx < props.tabs.length - 1 ? currentIdx + 1 : 0
      break
    case 'Home':
      event.preventDefault()
      newIdx = 0
      break
    case 'End':
      event.preventDefault()
      newIdx = props.tabs.length - 1
      break
    default:
      return
  }
  
  selectTab(newIdx)
  const tabButton = document.getElementById(`tab-${uid}-${newIdx}`)
  tabButton?.focus()
}
</script>
