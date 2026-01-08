<template>
  <button
      :class="[
      'inline-flex items-center font-semibold rounded transition focus:outline-none px-4 py-2',
      variantClasses,
      disabled && 'opacity-50 cursor-not-allowed'
    ]"
      :disabled="disabled"
  >
    <slot/>
  </button>
</template>

<script lang="ts" setup>
import {computed} from 'vue'

interface Props {
  variant?: 'primary' | 'secondary' | 'info' | 'success'
  disabled?: boolean
}

const props = withDefaults(defineProps<Props>(), {
  variant: 'primary',
  disabled: false
})

const variantClasses = computed(() => {
  switch (props.variant) {
    case 'secondary':
      // The old dark: styles are now the default
      return 'border border-gray-600 text-gray-200 hover:bg-gray-700'
    case 'info':
      // The old dark: styles are now the default
      return 'bg-teal-400 text-white hover:bg-teal-500'
    case 'success':
      // The old dark: styles are now the default
      return 'bg-green-500 text-white hover:bg-green-600'
    default: // primary
      // The old dark: styles are now the default
      return 'bg-blue-500 text-white hover:bg-blue-600'
  }
})
</script>
