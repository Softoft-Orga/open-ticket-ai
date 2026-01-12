<template>
  <span :class="badgeClasses"><slot /></span>
</template>

<script lang="ts" setup>
import { computed } from 'vue'
import { badge } from '../../../../design-system/recipes'
import type { Variant, Tone, Size } from '../../../../design-system/tokens'

interface Props {
  variant?: Variant
  tone?: Tone
  size?: Size
}

const props = withDefaults(defineProps<Props>(), {
  variant: 'surface',
  tone: 'primary',
  size: 'md'
})

const badgeClasses = computed(() => {
  return badge({
    variant: props.variant,
    tone: props.tone,
    size: props.size
  })
})
</script>
