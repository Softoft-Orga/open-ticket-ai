<template>
  <a
    :href="to"
    class="text-primary underline transition-colors hover:text-primary-light"
  >
    <slot />
  </a>
</template>

<script setup lang="ts">
defineProps<{
  to: string;
}>();
</script>
