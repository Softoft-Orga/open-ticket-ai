<template>
  <span :class="[baseClass, variantClass]"><slot/></span>
</template>

<script lang="ts" setup>
import { computed } from 'vue'

type Kind = 'primary' | 'secondary' | 'success' | 'warning' | 'danger'
const { type = 'secondary' } = defineProps<{ type?: Kind }>()

const baseClass =
  'inline-flex items-center rounded-full px-2 py-0.5 text-xs font-medium ring-1'

const variantClass = computed(() => {
  switch (type) {
    case 'primary':
      return 'bg-primary text-white ring-primary-dark'
    case 'success':
      return 'bg-primary-light text-background-dark ring-primary'
    case 'warning':
      return 'bg-amber-400 text-background-dark ring-amber-300'
    case 'danger':
      return 'bg-rose-600 text-white ring-rose-500'
    default:
      return 'bg-surface-dark text-text-dim ring-border-dark'
  }
})
</script>
