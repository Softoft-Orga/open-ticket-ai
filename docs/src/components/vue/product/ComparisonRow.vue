<template>
  <div class="grid grid-cols-3 gap-4 py-4 border-b border-border-dark/30 text-sm">
    <div class="text-text-dim font-medium">
      {{ label }}
    </div>
    <div class="text-white text-center">
      {{ v1 }}
    </div>
    <div class="text-white text-center font-bold">
      {{ v2 }}
    </div>
  </div>
</template>

<script setup lang="ts">
defineProps<{
  label: string
  v1: string
  v2: string
}>()
</script>
