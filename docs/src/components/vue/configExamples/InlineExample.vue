<script setup lang="ts">
defineProps<{
  slug: string;
}>();
</script>

<template>
  <div class="bg-surface-dark border border-border-dark rounded-xl p-6 my-6">
    <div class="text-text-2 text-sm">
      <!-- Placeholder for InlineExample component -->
      <!-- TODO: Implement actual config example rendering for slug: {{ slug }} -->
      <p class="text-muted italic">Config example: {{ slug }}</p>
    </div>
  </div>
</template>
