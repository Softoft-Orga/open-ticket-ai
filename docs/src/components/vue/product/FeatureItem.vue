<template>
  <Card :variant="variant" padding="lg" hoverable class="rounded-2xl">
    <div class="flex flex-col gap-4">
      <div class="w-12 h-12 rounded-xl bg-primary/10 flex items-center justify-center">
        <span class="text-2xl">{{ icon }}</span>
      </div>
      <h3 class="text-xl font-bold text-white">{{ title }}</h3>
      <p class="text-text-dim text-sm leading-relaxed">{{ desc }}</p>
    </div>
  </Card>
</template>

<script setup lang="ts">
import Card from '../core/basic/Card.vue'
import type { Variant } from '../core/design-system/tokens'

withDefaults(defineProps<{
  icon: string
  title: string
  desc: string
  /**
   * Visual variant from design system tokens
   * @default 'secondary'
   */
  variant?: Variant
}>(), {
  variant: 'secondary'
})
</script>
