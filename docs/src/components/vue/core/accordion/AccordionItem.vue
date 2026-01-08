<template>
  <div class="py-3">
    <button
      :id="`accordion-header-${uid}`"
      type="button"
      class="flex w-full justify-between font-semibold text-left focus:outline-none focus-visible:ring-2 focus-visible:ring-vp-brand rounded"
      :aria-expanded="computedOpen"
      :aria-controls="`accordion-panel-${uid}`"
      @click="handleToggle"
    >
      <span class="font-bold text-lg">{{ title }}</span>
      <span aria-hidden="true">{{ computedOpen ? '–' : '+' }}</span>
    </button>
    <div
      v-show="computedOpen"
      :id="`accordion-panel-${uid}`"
      class="pt-2 text-vp-text-2"
      role="region"
      :aria-labelledby="`accordion-header-${uid}`"
    >
      <slot/>
    </div>
  </div>
</template>

<script lang="ts" setup>
import {ref, computed, watch} from 'vue'

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

const uid = Math.random().toString(36).substr(2, 9)
const internalOpen = ref(props.defaultOpen)

const computedOpen = computed(() => {
  return props.isOpen !== undefined ? props.isOpen : internalOpen.value
})

watch(() => props.isOpen, (newVal) => {
  if (newVal !== undefined) {
    internalOpen.value = newVal
  }
})

const handleToggle = () => {
  if (props.isOpen === undefined) {
    internalOpen.value = !internalOpen.value
  }
  emit('toggle')
}
</script>
</script>
