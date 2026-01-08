<template>
  <div class="bg-surface-dark border border-border-dark p-6 rounded-lg shadow text-text-dim">
    <div v-if="$slots.header" class="mb-4">
      <slot name="header"/>
    </div>
    <div class="mb-4 text-white">
      <slot/>
    </div>
    <div v-if="$slots.footer" class="mt-4 text-text-dim">
      <slot name="footer"/>
    </div>
  </div>
</template>

<script lang="ts" setup>
// Card component with optional header and footer slots
</script>
