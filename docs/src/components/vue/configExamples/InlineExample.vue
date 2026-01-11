<template>
  <div class="inline-example bg-surface-dark border border-border-dark rounded-lg p-4 my-4">
    <p class="text-slate-400 text-sm">Config example: {{ slug }}</p>
  </div>
</template>

<script setup lang="ts">
defineProps<{
  slug: string;
}>();
</script>
