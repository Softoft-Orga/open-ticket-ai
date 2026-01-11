<template>
  <component
    :is="componentType"
    :class="buttonClasses"
    :disabled="disabled || loading"
    :to="to"
    :href="href"
  >
    <slot />
  </component>
</template>

<script lang="ts" setup>
import { computed } from 'vue'
import { button, type ButtonVariants } from '../../../../design-system/recipes'
import type { Tone, Size, Radius } from '../../../../design-system/tokens'

interface Props {
  variant?: 'solid' | 'outline' | 'ghost'
  size?: Size
  tone?: Tone
  radius?: Radius
  disabled?: boolean
  loading?: boolean
  block?: boolean
  to?: string
  href?: string
}

const props = withDefaults(defineProps<Props>(), {
  variant: 'solid',
  size: 'md',
  tone: 'primary',
  radius: 'xl',
  disabled: false,
  loading: false,
  block: false
})

const componentType = computed(() => {
  if (props.to) return 'router-link'
  if (props.href) return 'a'
  return 'button'
})

const buttonClasses = computed(() => {
  return button({
    variant: props.variant,
    tone: props.tone,
    size: props.size,
    radius: props.radius,
    loading: props.loading,
    disabled: props.disabled,
    block: props.block
  })
})
</script>
