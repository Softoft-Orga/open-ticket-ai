<template>
    <div class="space-y-6 text-slate-200">
        <MarketplaceSearchForm
            v-model:perPage="perPage"
            v-model:query="query"
            v-model:sort="sort"
            :filters="filters"
            :filters-applied="filtersApplied"
            :is-loading="isLoading"
            :per-page-options="perPageOptions"
            :recent-update-filters="recentUpdateFilters"
            :sort-options="sortOptions"
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
            v-if="!errorMessage && !isLoading && hasLoaded && totalResults === 0"
            class="rounded-xl border border-slate-700/70 bg-slate-900/60 p-6 text-center text-slate-300"
        >
            No plugins found.
        </section>

        <section v-if="!errorMessage && totalResults > 0" class="space-y-4">
            <header class="flex flex-wrap items-center justify-between gap-4 text-sm text-slate-300">
        <span>
          Showing {{ visiblePlugins.length }} of {{ totalResults }} plugin{{ totalResults === 1 ? '' : 's' }}
          for “{{ query || '' }}” on page {{ page }} of {{ totalPages }}.
        </span>
            </header>
            <div class="grid gap-4 md:grid-cols-2 xl:grid-cols-3">
                <PluginCard
                    v-for="plugin in visiblePlugins"
                    :key="plugin.name"
                    :formatted-date="formatDate(plugin.lastReleaseDate)"
                    :plugin="plugin"
                />
            </div>
        </section>

        <section v-if="isLoading && !hasLoaded" class="grid gap-4 md:grid-cols-2 xl:grid-cols-3">
            <MarketplaceSkeletonCard v-for="n in perPage" :key="`skeleton-${n}`"/>
        </section>

        <MarketplacePagination
            v-if="!errorMessage && hasLoaded && totalResults > 0"
            :has-more-results="hasMoreResults"
            :is-loading="isLoading"
            :page="page"
            :total-pages="totalPages"
            @next="goToNextPage"
            @prev="goToPreviousPage"
        />
    </div>
</template>

<script lang="ts" setup>
import PluginCard from "./PluginCard.vue";
import MarketplacePagination from "./MarketplacePagination.vue";
import MarketplaceSearchForm from "./MarketplaceSearchForm.vue";
import MarketplaceSkeletonCard from "./MarketplaceSkeletonCard.vue";
import {usePluginsMarketplace} from "../../composables/usePluginsMarketplace";

const {
    query,
    perPage,
    page,
    sort,
    filters,
    visiblePlugins,
    totalResults,
    totalPages,
    isLoading,
    errorMessage,
    hasLoaded,
    hasMoreResults,
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
