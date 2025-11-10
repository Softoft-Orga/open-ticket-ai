<template>
  <div class="space-y-6 text-slate-200">
    <MarketplaceSearchForm
      v-model:query="query"
      v-model:apiKey="apiKey"
      v-model:perPage="perPage"
      v-model:sort="sort"
      :filters="filters"
      :per-page-options="perPageOptions"
      :sort-options="sortOptions"
      :recent-update-filters="recentUpdateFilters"
      :can-search="canSearch"
      :is-loading="isLoading"
      :filters-applied="filtersApplied"
      @search="search"
      @clear-filters="clearFilters"
      @update-filters="updateFilters"
    />

    <section
      v-if="errorMessage"
      class="rounded-xl border border-red-500/50 bg-red-500/10 p-4 text-sm text-red-200"
    >
      {{ errorMessage }}
    </section>

    <section
      v-if="!errorMessage && !isLoading && hasSearched && filteredPlugins.length === 0"
      class="rounded-xl border border-slate-700/70 bg-slate-900/60 p-6 text-center text-slate-300"
    >
      No plugins found. Try searching for ‘otai-’.
    </section>

    <section v-if="!errorMessage && filteredPlugins.length > 0" class="space-y-4">
      <header class="flex flex-wrap items-center justify-between gap-4 text-sm text-slate-300">
        <span>
          Showing {{ filteredPlugins.length }} plugin{{ filteredPlugins.length === 1 ? '' : 's' }}
          for “{{ query || 'otai-' }}” on page {{ page }}.
        </span>
      </header>
      <div class="grid gap-4 md:grid-cols-2 xl:grid-cols-3">
        <PluginCard
          v-for="plugin in filteredPlugins"
          :key="plugin.name"
          :plugin="plugin"
          :formatted-date="formatDate(plugin.lastReleaseDate)"
        />
      </div>
    </section>

    <section v-if="isLoading" class="grid gap-4 md:grid-cols-2 xl:grid-cols-3">
      <MarketplaceSkeletonCard v-for="n in perPage" :key="`skeleton-${n}`" />
    </section>

    <MarketplacePagination
      v-if="!errorMessage && hasSearched"
      :page="page"
      :has-more-results="hasMoreResults"
      :is-loading="isLoading"
      @prev="goToPreviousPage"
      @next="goToNextPage"
    />
  </div>
</template>

<script lang="ts" setup>
import PluginCard from "./PluginCard.vue";
import MarketplacePagination from "./MarketplacePagination.vue";
import MarketplaceSearchForm from "./MarketplaceSearchForm.vue";
import MarketplaceSkeletonCard from "./MarketplaceSkeletonCard.vue";
import { usePluginsMarketplace } from "./usePluginsMarketplace";

const {
  query,
  apiKey,
  perPage,
  page,
  sort,
  filters,
  filteredPlugins,
  isLoading,
  errorMessage,
  hasSearched,
  hasMoreResults,
  canSearch,
  filtersApplied,
  formatDate,
  search,
  goToPreviousPage,
  goToNextPage,
  clearFilters,
  updateFilters,
  perPageOptions,
  sortOptions,
  recentUpdateFilters,
} = usePluginsMarketplace();
</script>
