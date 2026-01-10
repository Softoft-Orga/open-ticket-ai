<template>
  <Card
    background="surface-dark"
    padding="default"
    class="rounded-2xl transition-all duration-300 hover:border-primary/30 hover:shadow-glow hover:-translate-y-0.5"
  >
    <div class="text-sm text-text-dim mb-2 font-semibold uppercase tracking-wider">{{ label }}</div>
    <div class="text-2xl font-bold text-white">{{ value }}</div>
  </Card>
</template>

<script setup lang="ts">
import Card from '../core/basic/Card.vue';

defineProps<{
  label: string;
  value: string;
}>();
</script>
