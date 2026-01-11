<template>
  <footer class="flex flex-wrap items-center justify-between gap-4 text-sm text-dim">
    <span>Page {{ page }} of {{ totalPages }}</span>
    <div class="flex items-center gap-2">
      <Button
        variant="outline"
        size="sm"
        radius="2xl"
        :disabled="isLoading || page === 1"
        @click="emit('prev')"
      >
        Previous
      </Button>
      <Button
        variant="outline"
        size="sm"
        radius="2xl"
        :disabled="isLoading || !hasMoreResults"
        @click="emit('next')"
      >
        Next
      </Button>
    </div>
  </footer>
</template>

<script lang="ts" setup>
import Button from '../core/basic/Button.vue'

defineProps<{
  readonly page: number;
  readonly hasMoreResults: boolean;
  readonly isLoading: boolean;
  readonly totalPages: number;
}>();

/* eslint-disable no-unused-vars */
const emit = defineEmits<{
  (e: "prev"): void;
  (e: "next"): void;
}>();
</script>
