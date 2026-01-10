<template>
  <div class="flex flex-col gap-2">
    <div class="text-xs font-bold text-text-dim uppercase tracking-widest">{{ label }}</div>
    <div class="text-3xl font-black text-white">{{ value }}</div>
    <div class="text-sm text-cyan-glow italic">{{ sub }}</div>
  </div>
</template>

<script setup lang="ts">
defineProps<{
  label: string
  value: string
  sub: string
}>()
</script>
