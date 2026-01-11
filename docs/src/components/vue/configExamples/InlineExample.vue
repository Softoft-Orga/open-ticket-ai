<template>
  <div class="rounded-xl bg-surface-dark border border-border-dark p-6">
    <div class="text-text-dim text-sm">
      Example: {{ slug }}
    </div>
  </div>
</template>

<script setup lang="ts">
defineProps<{
  slug: string;
}>();
</script>
