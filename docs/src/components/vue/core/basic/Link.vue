<template>
  <a :href="to" class="text-primary hover:text-primary-light transition-colors underline">
    <slot />
  </a>
</template>

<script setup lang="ts">
defineProps<{
  to: string
}>()
</script>
