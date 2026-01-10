<template>
  <div class="flex flex-col gap-4 p-8 bg-surface-dark/40 border border-border-dark rounded-2xl hover:border-primary/30 transition-all">
    <div class="w-12 h-12 rounded-xl bg-primary/10 flex items-center justify-center">
      <span class="text-2xl">{{ icon }}</span>
    </div>
    <h3 class="text-xl font-bold text-white">{{ title }}</h3>
    <p class="text-text-dim text-sm leading-relaxed">{{ desc }}</p>
  </div>
</template>

<script setup lang="ts">
defineProps<{
  icon: string
  title: string
  desc: string
}>()
</script>
