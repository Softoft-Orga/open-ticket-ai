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
      return 'bg-indigo-600 text-white ring-indigo-500'
    case 'success':
      return 'bg-emerald-600 text-white ring-emerald-500'
    case 'warning':
      return 'bg-amber-400 text-black ring-amber-300'
    case 'danger':
      return 'bg-rose-600 text-white ring-rose-500'
    default:
      return 'bg-slate-700 text-slate-200 ring-slate-600'
  }
})
</script>
