<template>
  <div class="py-3">
    <button
      :id="`accordion-header-${title}`"
      :aria-expanded="isOpen"
      :aria-controls="`accordion-panel-${title}`"
      class="flex w-full justify-between font-semibold text-left focus:outline-none focus-visible:ring-2 focus-visible:ring-blue-400 rounded"
      @click="handleToggle"
    >
      <span class="font-bold text-lg">{{ title }}</span>
      <span class="text-xl" aria-hidden="true">{{ isOpen ? '−' : '+' }}</span>
    </button>
    <div
      v-if="isOpen"
      :id="`accordion-panel-${title}`"
      :aria-labelledby="`accordion-header-${title}`"
      class="pt-2 text-vp-text-2"
      role="region"
    >
      <slot/>
    </div>
  </div>
</template>

<script lang="ts" setup>
import {ref, watch, computed} from 'vue'

interface Props {
  title: string
  defaultOpen?: boolean
  isOpen?: boolean
}

const props = withDefaults(defineProps<Props>(), {
  defaultOpen: false,
  isOpen: undefined
})

const emit = defineEmits<{
  (e: 'toggle'): void
}>()

const internalOpen = ref(props.defaultOpen)

const isOpen = computed(() => {
  return props.isOpen !== undefined ? props.isOpen : internalOpen.value
})

watch(() => props.isOpen, (newValue) => {
  if (newValue !== undefined) {
    internalOpen.value = newValue
  }
})

function handleToggle() {
  if (props.isOpen === undefined) {
    internalOpen.value = !internalOpen.value
  }
  emit('toggle')
}
</script>
