<template>
  <a 
    :href="href"
    :target="computedTarget"
    :rel="computedRel"
    :class="[
      'text-vp-brand hover:text-vp-brand-dark underline-offset-2',
      underline ? 'underline' : 'hover:underline'
    ]"
  >
    <slot/>
  </a>
</template>

<script lang="ts" setup>
import {computed} from 'vue'
import {useData} from 'vitepress'

interface Props {
  to?: string
  href?: string
  external?: boolean
  target?: string
  rel?: string
  underline?: boolean
}

const props = withDefaults(defineProps<Props>(), {
  underline: false
})

const {lang} = useData()

const href = computed(() => {
  if (props.href) return props.href
  if (props.to) {
    if (props.external || props.to.startsWith('http')) {
      return props.to
    }
    return `/${lang.value}${props.to}`
  }
  return '#'
})

const isExternal = computed(() => {
  return props.external || (typeof props.href === 'string' && props.href.startsWith('http')) || (typeof props.to === 'string' && props.to.startsWith('http'))
})

const computedTarget = computed(() => {
  if (props.target) return props.target
  return isExternal.value ? '_blank' : undefined
})

const computedRel = computed(() => {
  if (props.rel) return props.rel
  return isExternal.value ? 'noopener noreferrer' : undefined
})
</script>
