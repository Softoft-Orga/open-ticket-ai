<template>
  <Card
    class="text-center"
    elevation="lg"
    radius="2xl"
    size="lg"
    tone="success"
    variant="surface"
  >
    <div class="py-8 md:py-12">
      <div class="mb-8">
        <div class="inline-flex items-center justify-center w-20 h-20 rounded-full bg-success/20">
          <CheckCircleIcon class="w-12 h-12 text-success" />
        </div>
      </div>

      <h1 class="text-3xl md:text-5xl font-bold text-white mb-6">
        {{ title }}
      </h1>

      <p class="text-xl text-text-1 mb-10 leading-relaxed max-w-xl mx-auto">
        {{ description }}
      </p>

      <div
        v-if="$slots.default"
        class="mb-10 text-left"
      >
        <slot />
      </div>

      <div class="flex flex-wrap gap-4 justify-center">
        <Button
          v-if="primaryButtonText"
          :href="primaryButtonHref"
          size="lg"
          tone="primary"
          variant="surface"
        >
          {{ primaryButtonText }}
        </Button>
        <Button
          v-if="secondaryButtonText"
          :href="secondaryButtonHref"
          size="lg"
          tone="neutral"
          variant="outline"
        >
          {{ secondaryButtonText }}
        </Button>
      </div>
    </div>
  </Card>
</template>

<script lang="ts" setup>
import { CheckCircleIcon } from '@heroicons/vue/24/outline'
import Card from '../core/basic/Card.vue'
import Button from '../core/basic/Button.vue'

interface Props {
  title: string
  description: string
  primaryButtonText?: string
  primaryButtonHref?: string
  secondaryButtonText?: string
  secondaryButtonHref?: string
}

withDefaults(defineProps<Props>(), {
  primaryButtonText: 'Back to Home',
  primaryButtonHref: '/',
  secondaryButtonText: undefined,
  secondaryButtonHref: undefined
})
</script>

