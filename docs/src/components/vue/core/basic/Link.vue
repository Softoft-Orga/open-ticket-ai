<template>
  <a 
    :href="href"
    :target="target"
    :rel="rel"
    class="text-blue-400 hover:text-blue-300 transition-colors"
  >
    <slot/>
  </a>
</template>

<script lang="ts" setup>
import {computed} from 'vue'

interface Props {
  to?: string
  href?: string
  external?: boolean
  target?: string
  rel?: string
}

const props = withDefaults(defineProps<Props>(), {
  external: false
})

const href = computed(() => {
  if (props.href) {
    return props.href
  }
  if (props.to) {
    return props.to
  }
  return '#'
})

const target = computed(() => {
  if (props.target) return props.target
  if (props.external) return '_blank'
  return undefined
})

const rel = computed(() => {
  if (props.rel) return props.rel
  if (props.external || props.target === '_blank') {
    return 'noopener noreferrer'
  }
  return undefined
})
</script>
