<!-- Cell.vue -->
<template>
  <component :is="tag" :class="['px-4', dense ? 'py-2' : 'py-3', alignClass, header ? 'text-slate-200 font-semibold' : 'text-slate-300']">
    <slot />
  </component>
</template>

<script setup lang="ts">
import { computed, inject, withDefaults } from 'vue'

type Align = 'left' | 'center' | 'right'

const props = withDefaults(defineProps<{ header?: boolean; align?: Align }>(), {
  header: false,
  align: 'left'
})

const dense = inject('tableDense', false) as boolean
const tag = computed(() => (props.header ? 'th' : 'td'))
const alignClass = computed(() => (props.align === 'center' ? 'text-center' : props.align === 'right' ? 'text-right' : 'text-left'))
</script>
