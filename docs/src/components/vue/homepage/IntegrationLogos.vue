<template>
  <section class="w-full px-4 md:px-10 lg:px-20 xl:px-40 py-16 bg-surface-dark/30">
    <div class="w-full max-w-7xl mx-auto">
      <div class="flex flex-col items-center gap-8">
        <h3 class="text-sm font-bold text-gray-400 uppercase tracking-wider">
          {{ title }}
        </h3>
        <div class="flex flex-wrap items-center justify-center gap-12 md:gap-16">
          <div
            v-for="integration in integrations"
            :key="integration.name"
            class="flex items-center gap-3 px-4 py-2 rounded-lg bg-surface-dark/50 border border-border-dark hover:border-primary/30 transition-colors"
          >
            <div class="w-6 h-6 rounded-full bg-primary/20 flex items-center justify-center">
              <CheckCircleIcon class="w-4 h-4 text-primary" />
            </div>
            <span class="text-gray-300 font-medium">{{ integration.name }}</span>
          </div>
        </div>
        <p
          v-if="moreText"
          class="text-gray-500 text-sm"
        >
          {{ moreText }}
        </p>
      </div>
    </div>
  </section>
</template>

<script setup lang="ts">
import { CheckCircleIcon } from '@heroicons/vue/24/solid';

interface Integration {
  name: string;
}

withDefaults(
  defineProps<{
    title?: string;
    integrations: Integration[];
    moreText?: string;
  }>(),
  {
    title: 'WORKS WITH',
    moreText: 'More on request'
  }
);
</script>
