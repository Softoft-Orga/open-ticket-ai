<template>
  <span :class="[baseClass, variantClass]"><slot/></span>
</template>

<script lang="ts" setup>
import { computed } from 'vue'
import type { Tone } from '../design-system/tokens'

// Badge supports brand colors (primary, secondary) plus semantic tones
type BadgeType = 'primary' | 'secondary' | Tone
const { type = 'secondary' } = defineProps<{ type?: BadgeType }>()

const baseClass =
  'inline-flex items-center gap-1 rounded-full px-3 py-1 text-xs font-semibold leading-tight ring-1 ring-inset shadow-sm transition-colors duration-150'

const variantClass = computed(() => {
  switch (type) {
    case 'primary':
      return 'bg-primary text-white ring-primary/50 hover:bg-primary-dark'
    case 'success':
      return 'bg-emerald-600 text-white ring-emerald-500/50 hover:bg-emerald-700'
    case 'warning':
      return 'bg-amber-500 text-white ring-amber-400/50 hover:bg-amber-600'
    case 'danger':
      return 'bg-rose-600 text-white ring-rose-500/50 hover:bg-rose-700'
    default:
      return 'bg-surface-lighter text-white ring-border-dark hover:bg-surface-dark'
  }
})
</script>
