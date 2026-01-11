<template>
  <section class="w-full px-4 md:px-10 lg:px-20 xl:px-40 py-24 bg-background-dark">
    <div class="w-full max-w-7xl mx-auto">
      <div class="mb-16 text-center">
        <h2 class="font-display text-4xl font-bold text-white mb-4">
          {{ title }}
        </h2>
        <p class="text-gray-400 text-lg">
          {{ subtitle }}
        </p>
      </div>
      
      <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
        <ServiceCard
          v-for="service in services"
          :key="service.slug"
          :title="service.title"
          :one-liner="service.oneLiner"
          :description="service.description"
          :outcomes="service.outcomes"
          :starting-price="service.startingPrice"
          :group="service.group"
        />
      </div>
    </div>
  </section>
</template>

<script setup lang="ts">
import ServiceCard from './ServiceCard.vue';

interface Service {
  slug: string;
  title: string;
  oneLiner?: string;
  description: string;
  outcomes?: string[];
  startingPrice?: number;
  group?: string;
}

defineProps<{
  title: string;
  subtitle: string;
  services: Service[];
}>();
</script>
