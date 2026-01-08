<template>
  <div :class="['my-4 p-4 border-l-4 rounded', colorClasses]">
    <div class="flex items-start gap-2">
      <span>{{ icon }}</span>
      <div class="flex-1">
        <slot/>
      </div>
    </div>
  </div>
</template>

<script lang="ts" setup>
import {computed} from 'vue'

interface Props {
  type?: 'info' | 'success' | 'warning' | 'danger'
}

const props = withDefaults(defineProps<Props>(), {
  type: 'info'
})

const colorClasses = computed(() => {
  switch (props.type) {
    case 'success':
      return 'bg-primary-light/15 border-primary-light text-primary-light'
    case 'warning':
      return 'bg-amber-500/15 border-amber-400 text-amber-300'
    case 'danger':
      return 'bg-rose-500/15 border-rose-500 text-rose-300'
    default:
      return 'bg-primary/10 border-primary text-primary'
  }
})

const icon = computed(() => {
  switch (props.type) {
    case 'success':
      return '✔'
    case 'warning':
      return '⚠'
    case 'danger':
      return '✖'
    default:
      return 'ℹ'
  }
})
</script>
