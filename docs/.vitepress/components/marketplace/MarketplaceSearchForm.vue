<template>
  <section class="rounded-2xl border border-slate-800 bg-slate-900/70 p-6 shadow-lg shadow-slate-900/40">
    <div class="grid gap-4 md:grid-cols-2 lg:grid-cols-3">
      <label class="flex flex-col gap-2">
        <span class="text-sm font-semibold text-slate-200">Search loaded plugins</span>
        <input
          v-model="queryModel"
          type="text"
          autocomplete="off"
          placeholder="Filter by name or summary"
          class="w-full rounded-lg border border-slate-700 bg-slate-950/60 px-3 py-2 text-sm text-slate-100 placeholder:text-slate-500 focus:border-sky-500 focus:outline-none focus:ring-1 focus:ring-sky-500"
          @keyup.enter="emit('search')"
        >
      </label>

      <label class="flex flex-col gap-2">
        <span class="text-sm font-semibold text-slate-200">Results per page</span>
        <select
          v-model.number="perPageModel"
          class="w-full rounded-lg border border-slate-700 bg-slate-950/60 px-3 py-2 text-sm text-slate-100 focus:border-sky-500 focus:outline-none focus:ring-1 focus:ring-sky-500"
        >
          <option v-for="option in perPageOptions" :key="option" :value="option">
            {{ option }}
          </option>
        </select>
      </label>

      <label class="flex flex-col gap-2">
        <span class="text-sm font-semibold text-slate-200">Sort by</span>
        <select
          v-model="sortModel"
          class="w-full rounded-lg border border-slate-700 bg-slate-950/60 px-3 py-2 text-sm text-slate-100 focus:border-sky-500 focus:outline-none focus:ring-1 focus:ring-sky-500"
        >
          <option v-for="option in sortOptions" :key="option.value" :value="option.value">
            {{ option.label }}
          </option>
        </select>
      </label>

      <fieldset class="flex flex-col gap-2">
        <span class="text-sm font-semibold text-slate-200">Filters</span>
        <div class="flex flex-wrap gap-4 text-sm text-slate-200">
          <label class="flex items-center gap-2">
            <input
              :checked="filters.hasRepository"
              type="checkbox"
              class="h-4 w-4 rounded border-slate-600 bg-slate-900/80 text-sky-500 focus:ring-sky-500"
              @change="handleCheckbox($event, 'hasRepository')"
            >
            Has repository
          </label>
          <label class="flex items-center gap-2">
            <input
              :checked="filters.hasHomepage"
              type="checkbox"
              class="h-4 w-4 rounded border-slate-600 bg-slate-900/80 text-sky-500 focus:ring-sky-500"
              @change="handleCheckbox($event, 'hasHomepage')"
            >
            Has homepage
          </label>
          <label class="flex items-center gap-2">
            Updated within
            <select
              :value="filters.updatedWithinMonths ?? ''"
              class="rounded-lg border border-slate-700 bg-slate-950/60 px-2 py-1 text-xs text-slate-100 focus:border-sky-500 focus:outline-none focus:ring-1 focus:ring-sky-500"
              @change="handleRecentChange"
            >
              <option value="">Any time</option>
              <option
                v-for="option in recentUpdateFilters"
                :key="option.value"
                :value="option.value"
              >
                {{ option.label }}
              </option>
            </select>
          </label>
        </div>
      </fieldset>

      <div class="flex items-end">
        <button
          class="inline-flex items-center justify-center gap-2 rounded-full bg-sky-600 px-4 py-2 text-sm font-semibold text-white transition hover:bg-sky-500 disabled:cursor-not-allowed disabled:opacity-60"
          type="button"
          :disabled="isLoading"
          @click="emit('search')"
        >
          <span v-if="!isLoading">Search</span>
          <span v-else class="flex items-center gap-2">
            <span class="h-4 w-4 animate-spin rounded-full border-2 border-sky-300/40 border-t-sky-100" aria-hidden="true" />
            Searching…
          </span>
        </button>
      </div>
    </div>

    <div v-if="filtersApplied" class="mt-4 flex items-center gap-3 text-sm text-slate-300">
      <span>Active filters applied.</span>
      <button
        class="rounded-full border border-slate-600 px-3 py-1 text-xs font-medium text-slate-200 transition hover:bg-slate-800"
        type="button"
        @click="emit('clear-filters')"
      >
        Clear filters
      </button>
    </div>
  </section>
</template>

<script lang="ts" setup>
import type { FilterOptions, SortOption } from "./pluginModels";

const queryModel = defineModel<string>("query");
const perPageModel = defineModel<number>("perPage");
const sortModel = defineModel<SortOption>("sort");

defineProps<{
  readonly filters: FilterOptions;
  readonly perPageOptions: readonly number[];
  readonly sortOptions: readonly { readonly label: string; readonly value: SortOption }[];
  readonly recentUpdateFilters: readonly { readonly label: string; readonly value: number }[];
  readonly isLoading: boolean;
  readonly filtersApplied: boolean;
}>();

const emit = defineEmits<{
  (e: "search"): void;
  (e: "clear-filters"): void;
  (e: "update-filters", value: Partial<FilterOptions>): void;
}>();

function handleCheckbox(event: Event, key: "hasRepository" | "hasHomepage"): void {
  const target = event.target as HTMLInputElement;
  emit("update-filters", { [key]: target.checked } as Partial<FilterOptions>);
}

function handleRecentChange(event: Event): void {
  const target = event.target as HTMLSelectElement;
  const value = target.value ? Number(target.value) : null;
  emit("update-filters", { updatedWithinMonths: value });
}
</script>
