<template>
    <div class="relative w-full">
        <div v-if="icon" :class="iconContainerClasses">
            <component :is="icon" :class="iconClasses" />
        </div>
        <textarea
            ref="textareaRef"
            :disabled="disabled"
            :placeholder="placeholder"
            :value="modelValue"
            :class="[
                'w-full border bg-surface-dark text-white placeholder-text-dim transition-all duration-200',
                'focus:outline-none focus:ring-2 focus:ring-primary/50 focus:border-primary/50',
                'focus:shadow-[0_0_20px_rgba(166,13,242,0.2)]',
                'disabled:opacity-50 disabled:cursor-not-allowed',
                'border-border-dark hover:border-primary/30',
                autoResize ? 'resize-none' : 'resize-y',
                sizeClasses,
                icon ? iconPaddingClasses : ''
            ]"
            :rows="rows"
            @input="onInput"
        />
    </div>
</template>

<script lang="ts" setup>
import { computed, ref, watch, nextTick, onMounted } from 'vue'
import type { Component } from 'vue'
import type { Size } from '../design-system/tokens'

const props = withDefaults(defineProps<{
  modelValue?: string
  placeholder?: string
  disabled?: boolean
  icon?: Component
  size?: Size
  autoResize?: boolean
}>(), {
  modelValue: '',
  placeholder: '',
  disabled: false,
  size: 'md',
  autoResize: true,
})

const emit = defineEmits<{
  (e: 'update:modelValue', value: string): void
}>()

const textareaRef = ref<HTMLTextAreaElement | null>(null)
const rows = computed(() => props.autoResize ? 1 : 4)

const sizeClasses = computed(() => {
  switch (props.size) {
    case 'sm':
      return 'py-2 px-3 text-sm rounded-lg min-h-[80px]'
    case 'lg':
      return 'py-4 px-5 text-lg rounded-xl min-h-[120px]'
    default: // md
      return 'py-3 px-4 text-base rounded-xl min-h-[100px]'
  }
})

const iconContainerClasses = computed(() => {
  switch (props.size) {
    case 'sm':
      return 'absolute top-2 left-3 pointer-events-none z-10'
    case 'lg':
      return 'absolute top-4 left-5 pointer-events-none z-10'
    default: // md
      return 'absolute top-3 left-4 pointer-events-none z-10'
  }
})

const iconClasses = computed(() => {
  switch (props.size) {
    case 'sm':
      return 'w-4 h-4 text-text-dim'
    case 'lg':
      return 'w-6 h-6 text-text-dim'
    default: // md
      return 'w-5 h-5 text-text-dim'
  }
})

const iconPaddingClasses = computed(() => {
  switch (props.size) {
    case 'sm':
      return 'pl-10 pr-3'
    case 'lg':
      return 'pl-12 pr-5'
    default: // md
      return 'pl-11 pr-4'
  }
})

function onInput(event: Event) {
  const value = (event.target as HTMLTextAreaElement).value
  emit('update:modelValue', value)
  
  if (props.autoResize) {
    adjustHeight()
  }
}

function adjustHeight() {
  if (!textareaRef.value) return
  
  // Reset height to auto to get the correct scrollHeight
  textareaRef.value.style.height = 'auto'
  
  // Set height based on scrollHeight with a max of 400px
  const newHeight = Math.min(textareaRef.value.scrollHeight, 400)
  textareaRef.value.style.height = `${newHeight}px`
}

// Watch for external changes to modelValue
watch(() => props.modelValue, async () => {
  if (props.autoResize) {
    await nextTick()
    adjustHeight()
  }
})

// Initial height adjustment
onMounted(() => {
  if (props.autoResize && props.modelValue) {
    nextTick(() => {
      adjustHeight()
    })
  }
})
</script>
