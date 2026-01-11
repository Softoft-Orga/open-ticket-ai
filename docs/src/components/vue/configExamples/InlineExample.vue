<template>
  <div class="inline-example">
    <!-- Placeholder component for config examples -->
    <slot>
      <p class="text-slate-400 text-sm">Example: {{ slug }}</p>
    </slot>
  </div>
</template>

<script setup lang="ts">
defineProps<{
  slug?: string;
}>();
</script>
