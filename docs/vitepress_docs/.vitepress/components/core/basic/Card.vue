<template>
  <div class="bg-vp-bg-soft border border-vp-border p-6 rounded-lg shadow">
    <div v-if="$slots.header" class="mb-4">
      <slot name="header" />
    </div>
    <div class="mb-4">
      <slot />
    </div>
    <div v-if="$slots.footer" class="mt-4">
      <slot name="footer" />
    </div>
  </div>
</template>

<script lang="ts" setup>
// Card component with optional header and footer slots
</script>
