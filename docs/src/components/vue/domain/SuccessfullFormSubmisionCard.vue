<template>
  <Card class="text-center" elevation="lg" radius="2xl" size="lg" tone="success" variant="surface">
    <div class="py-8 md:py-12">
      <div class="mb-8">
        <div class="inline-flex h-20 w-20 items-center justify-center rounded-full bg-success/20">
          <CheckCircleIcon class="h-12 w-12 text-success" />
        </div>
      </div>

      <h1 class="mb-6 text-3xl font-bold text-white md:text-5xl">
        {{ title }}
      </h1>

      <p class="mx-auto mb-10 max-w-xl text-xl leading-relaxed text-text-1">
        {{ description }}
      </p>

      <div v-if="$slots.default" class="mb-10 text-left">
        <slot />
      </div>

      <div class="flex flex-wrap justify-center gap-4">
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
import { CheckCircleIcon } from '@heroicons/vue/24/outline';
import Card from '../core/basic/Card.vue';
import Button from '../core/basic/Button.vue';

interface Props {
  title: string;
  description: string;
  primaryButtonText?: string;
  primaryButtonHref?: string;
  secondaryButtonText?: string;
  secondaryButtonHref?: string;
}

withDefaults(defineProps<Props>(), {
  primaryButtonText: 'Back to Home',
  primaryButtonHref: '/',
  secondaryButtonText: undefined,
  secondaryButtonHref: undefined,
});
</script>
