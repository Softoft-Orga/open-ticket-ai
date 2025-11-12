<template>
  <footer class="flex flex-wrap items-center justify-between gap-4 text-sm text-slate-300">
    <span>Page {{ page }} of {{ totalPages }}</span>
    <div class="flex items-center gap-2">
      <button
        class="rounded-full border border-slate-700 px-4 py-2 font-medium text-slate-100 transition hover:border-sky-500 hover:text-sky-200 disabled:cursor-not-allowed disabled:opacity-60"
        type="button"
        :disabled="isLoading || page === 1"
        @click="emit('prev')"
      >
        Previous
      </button>
      <button
        class="rounded-full border border-slate-700 px-4 py-2 font-medium text-slate-100 transition hover:border-sky-500 hover:text-sky-200 disabled:cursor-not-allowed disabled:opacity-60"
        type="button"
        :disabled="isLoading || !hasMoreResults"
        @click="emit('next')"
      >
        Next
      </button>
    </div>
  </footer>
</template>

<script lang="ts" setup>
defineProps<{
  readonly page: number;
  readonly hasMoreResults: boolean;
  readonly isLoading: boolean;
  readonly totalPages: number;
}>();

const emit = defineEmits<{
  (e: "prev"): void;
  (e: "next"): void;
}>();
</script>
