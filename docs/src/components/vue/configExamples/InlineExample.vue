<template>
  <div class="my-6 p-4 border border-border-1 rounded-lg bg-surface-1">
    <div class="text-sm text-muted mb-2">Example: {{ slug }}</div>
    <div class="text-text-2">
      <!-- Placeholder for inline example content -->
      <p class="italic">Example content for "{{ slug }}" will be rendered here.</p>
    </div>
  </div>
</template>

<script setup lang="ts">
defineProps<{
  slug: string;
}>();
</script>
