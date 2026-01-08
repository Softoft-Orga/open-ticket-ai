<template>
  <span :class="['inline-block rounded-full px-4 py-1.5 text-sm font-semibold border', color]">
    {{ label }}
  </span>
</template>

<script lang="ts" setup>
defineProps<{
  label: string
  color: string
}>()
</script>
