<template>
  <span :class="[baseClass, variantClass]"><slot/></span>
</template>

<script lang="ts" setup>
import { computed } from 'vue'

type Kind = 'primary' | 'secondary' | 'success' | 'warning' | 'danger'
const { type = 'secondary' } = defineProps<{ type?: Kind }>()

const baseClass =
  'inline-flex items-center gap-1 rounded-full px-3 py-1 text-xs font-semibold leading-tight ring-1 ring-inset shadow-sm transition-colors duration-150'

const variantClass = computed(() => {
  switch (type) {
    case 'primary':
      return 'bg-primary text-white ring-primary/70'
    case 'success':
      return 'bg-emerald-500 text-emerald-50 ring-emerald-400'
    case 'warning':
      return 'bg-amber-400 text-amber-950 ring-amber-300'
    case 'danger':
      return 'bg-rose-500 text-white ring-rose-400'
    default:
      return 'bg-surface-lighter text-text-dim ring-white/10'
  }
})
</script>
