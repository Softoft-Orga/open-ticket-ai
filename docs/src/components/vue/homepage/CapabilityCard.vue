<template>
  <div class="flex flex-col gap-4 p-8 bg-surface-dark/50 border border-border-dark rounded-2xl hover:border-primary/50 transition-all duration-300 group">
    <div class="flex items-center gap-3">
      <span class="material-symbols-outlined text-4xl text-primary group-hover:scale-110 transition-transform">{{ icon }}</span>
    </div>
    <h3 class="text-2xl font-bold text-white">{{ title }}</h3>
    <p class="text-gray-400 text-base leading-relaxed">{{ desc }}</p>
  </div>
</template>

<script setup lang="ts">
defineProps<{
  icon: string;
  title: string;
  desc: string;
}>();
</script>
