<template>
  <span :class="['px-2 py-1 rounded-full text-sm font-semibold', typeClass]">
    <slot/>
  </span>
</template>

<script lang="ts" setup>
import {computed} from 'vue'

interface Props {
    type?: 'primary' | 'secondary' | 'success' | 'warning' | 'danger'
}

const props = withDefaults(defineProps<Props>(), {
    type: 'secondary'
})

const typeClass = computed(() => {
    switch (props.type) {
        case 'primary':
            return 'bg-vp-brand-1 text-white'
        case 'success':
            return 'bg-green-600 text-black'
        case 'warning':
            return 'bg-yellow-500 text-black'
        case 'danger':
            return 'bg-pink-600 text-white'
        default:
            return 'bg-[var(--vp-c-bg-soft)] text-[var(--vp-c-text-1)]'
    }
})
</script>
