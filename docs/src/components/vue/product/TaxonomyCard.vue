<template>
  <Card 
    background="surface-dark" 
    padding="lg" 
    hoverable
    class="rounded-2xl"
  >
    <h3 class="text-white font-bold text-xl mb-2 uppercase tracking-wide">
      {{ title }}
    </h3>
    <p class="text-text-dim text-sm mb-6">
      {{ desc }}
    </p>
    <ul class="space-y-2">
      <li
        v-for="item in items"
        :key="item"
        class="flex items-center gap-3"
      >
        <div class="w-2 h-2 rounded-full bg-primary-light" />
        <span class="text-white text-sm font-medium">{{ item }}</span>
      </li>
    </ul>
  </Card>
</template>

<script setup lang="ts">
import Card from '../core/basic/Card.vue';

defineProps<{
  title: string;
  desc: string;
  items: string[];
}>();
</script>
