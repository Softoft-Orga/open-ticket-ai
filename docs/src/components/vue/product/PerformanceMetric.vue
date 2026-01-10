<template>
  <div class="bg-surface-dark border border-surface-lighter rounded-2xl p-6 hover:border-primary/30 transition-all">
    <div class="text-sm text-text-dim mb-2 font-semibold uppercase tracking-wider">{{ label }}</div>
    <div class="text-2xl font-bold text-white">{{ value }}</div>
  </div>
</template>

<script setup lang="ts">
defineProps<{
  label: string;
  value: string;
}>();
</script>
