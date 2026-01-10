<template>
  <div class="bg-surface-dark border border-surface-lighter rounded-2xl p-8 hover:border-primary/30 transition-all">
    <h3 class="text-white font-bold text-xl mb-2 uppercase tracking-wide">{{ title }}</h3>
    <p class="text-text-dim text-sm mb-6">{{ desc }}</p>
    <ul class="space-y-2">
      <li
        v-for="item in items"
        :key="item"
        class="flex items-center gap-3"
      >
        <div class="w-2 h-2 rounded-full bg-primary-light"></div>
        <span class="text-white text-sm font-medium">{{ item }}</span>
      </li>
    </ul>
  </div>
</template>

<script setup lang="ts">
defineProps<{
  title: string;
  desc: string;
  items: string[];
}>();
</script>
