import { computed, onBeforeUnmount, onMounted, reactive, ref, watch } from "vue";
import {
  PER_PAGE_OPTIONS,
  RECENT_MONTH_FILTERS,
  SORT_OPTIONS,
  type FilterOptions,
  type LibrariesIoResult,
  type Plugin,
  type PyPIResponse,
  type SortOption,
} from "./pluginModels";
import {
  applyFiltersAndSort,
  mapLibrariesIoPackage,
  mapPyPIPackage,
  mergePluginData,
  type LibrariesPluginDetails,
  type PyPIPluginDetails,
} from "./pluginUtils";

const LIBRARIES_IO_ENDPOINT = "https://libraries.io/api/search";
const PYPI_ENDPOINT = "https://pypi.org/pypi";
const PYPI_CONCURRENCY = 5;

export function usePluginsMarketplace() {
  const query = ref("otai-");
  const apiKey = ref("");
  const perPage = ref<typeof PER_PAGE_OPTIONS[number]>(PER_PAGE_OPTIONS[0]);
  const page = ref(1);
  const sort = ref<SortOption>("relevance");
  const filters = reactive<FilterOptions>({
    hasRepository: false,
    hasHomepage: false,
    updatedWithinMonths: null,
  });

  const plugins = ref<Plugin[]>([]);
  const isLoading = ref(false);
  const errorMessage = ref<string | null>(null);
  const hasSearched = ref(false);
  const lastPageCount = ref(0);

  const abortController = ref<AbortController | null>(null);
  const pyPiCache = new Map<string, PyPIPluginDetails | null>();

  const filteredPlugins = computed(() => applyFiltersAndSort(plugins.value, filters, sort.value));
  const filtersApplied = computed(
    () => filters.hasHomepage || filters.hasRepository || filters.updatedWithinMonths !== null,
  );
  const hasMoreResults = computed(() => lastPageCount.value === perPage.value);
  const canSearch = computed(() => Boolean(apiKey.value.trim()) && !isLoading.value);
  const dateFormatter = computed(() => new Intl.DateTimeFormat(undefined, { dateStyle: "medium" }));

  function formatDate(iso: string | null): string {
    if (!iso) {
      return "Unknown";
    }
    const date = new Date(iso);
    if (Number.isNaN(date.getTime())) {
      return "Unknown";
    }
    return dateFormatter.value.format(date);
  }

  function buildSearchUrl(): string {
    const url = new URL(LIBRARIES_IO_ENDPOINT);
    url.searchParams.set("q", query.value.trim() || "otai-");
    url.searchParams.set("platforms", "PyPI");
    url.searchParams.set("per_page", String(perPage.value));
    url.searchParams.set("page", String(page.value));
    url.searchParams.set("api_key", apiKey.value.trim());
    return url.toString();
  }

  async function loadPyPiPackage(name: string, signal: AbortSignal): Promise<PyPIPluginDetails | null> {
    if (pyPiCache.has(name)) {
      return pyPiCache.get(name) ?? null;
    }
    try {
      const response = await fetch(`${PYPI_ENDPOINT}/${encodeURIComponent(name)}/json`, {
        signal,
        headers: { Accept: "application/json" },
      });
      if (response.status === 404) {
        pyPiCache.set(name, null);
        return null;
      }
      if (!response.ok) {
        throw new Error(`PyPI request failed with status ${response.status}`);
      }
      const data = (await response.json()) as PyPIResponse;
      const details = mapPyPIPackage(data) ?? null;
      pyPiCache.set(name, details);
      return details;
    } catch (error) {
      if (error instanceof DOMException && error.name === "AbortError") {
        throw error;
      }
      pyPiCache.set(name, null);
      return null;
    }
  }

  async function fetchPyPiDetails(
    packages: readonly LibrariesPluginDetails[],
    signal: AbortSignal,
  ): Promise<Map<string, PyPIPluginDetails | null>> {
    const results = new Map<string, PyPIPluginDetails | null>();
    let index = 0;

    const worker = async (): Promise<void> => {
      while (index < packages.length) {
        const current = index;
        index += 1;
        if (current >= packages.length) {
          return;
        }
        const name = packages[current].name;
        try {
          const details = await loadPyPiPackage(name, signal);
          results.set(name, details);
        } catch (error) {
          if (error instanceof DOMException && error.name === "AbortError") {
            throw error;
          }
          results.set(name, null);
        }
      }
    };

    const workers = Array.from(
      { length: Math.min(PYPI_CONCURRENCY, packages.length) },
      () => worker(),
    );
    await Promise.all(workers);
    return results;
  }

  async function executeSearch(): Promise<void> {
    if (!apiKey.value.trim()) {
      errorMessage.value = "Please provide a Libraries.io API key.";
      return;
    }

    abortController.value?.abort();
    const controller = new AbortController();
    abortController.value = controller;

    isLoading.value = true;
    errorMessage.value = null;
    hasSearched.value = true;

    try {
      const response = await fetch(buildSearchUrl(), {
        signal: controller.signal,
        headers: { Accept: "application/json" },
      });

      if (response.status === 401 || response.status === 403) {
        plugins.value = [];
        lastPageCount.value = 0;
        errorMessage.value = "Libraries.io API key is missing or invalid.";
        return;
      }

      if (response.status === 429) {
        plugins.value = [];
        lastPageCount.value = 0;
        errorMessage.value = "Libraries.io rate limit reached. Please wait and try again.";
        return;
      }

      if (!response.ok) {
        throw new Error(`Libraries.io request failed with status ${response.status}`);
      }

      const payload = (await response.json()) as unknown;
      if (!Array.isArray(payload)) {
        throw new Error("Unexpected Libraries.io response structure.");
      }

      const libraryPackages = (payload as LibrariesIoResult[]).map((entry) => mapLibrariesIoPackage(entry));
      lastPageCount.value = libraryPackages.length;

      if (libraryPackages.length === 0) {
        plugins.value = [];
        return;
      }

      const pyPiResults = await fetchPyPiDetails(libraryPackages, controller.signal);
      plugins.value = libraryPackages.map((pkg) => mergePluginData(pkg, pyPiResults.get(pkg.name) ?? null));
    } catch (error) {
      if (error instanceof DOMException && error.name === "AbortError") {
        return;
      }
      plugins.value = [];
      lastPageCount.value = 0;
      errorMessage.value =
        error instanceof Error ? error.message : "Something went wrong while fetching plugins.";
    } finally {
      if (abortController.value === controller) {
        isLoading.value = false;
      }
    }
  }

  function search(): void {
    page.value = 1;
    void executeSearch();
  }

  function goToPreviousPage(): void {
    if (page.value === 1) {
      return;
    }
    page.value -= 1;
    void executeSearch();
  }

  function goToNextPage(): void {
    if (!hasMoreResults.value) {
      return;
    }
    page.value += 1;
    void executeSearch();
  }

  function clearFilters(): void {
    filters.hasHomepage = false;
    filters.hasRepository = false;
    filters.updatedWithinMonths = null;
  }

  function updateFilters(partial: Partial<FilterOptions>): void {
    Object.assign(filters, partial);
  }

  function syncToUrl(): void {
    if (typeof window === "undefined") {
      return;
    }
    const params = new URLSearchParams(window.location.search);
    params.set("query", query.value);
    params.set("page", String(page.value));
    params.set("perPage", String(perPage.value));
    params.set("sort", sort.value);
    if (filters.hasRepository) {
      params.set("hasRepo", "1");
    } else {
      params.delete("hasRepo");
    }
    if (filters.hasHomepage) {
      params.set("hasHomepage", "1");
    } else {
      params.delete("hasHomepage");
    }
    if (filters.updatedWithinMonths !== null) {
      params.set("updatedWithinMonths", String(filters.updatedWithinMonths));
    } else {
      params.delete("updatedWithinMonths");
    }
    const newUrl = `${window.location.pathname}?${params.toString()}`;
    window.history.replaceState(null, "", newUrl);
  }

  function loadFromUrl(): void {
    if (typeof window === "undefined") {
      return;
    }
    const params = new URLSearchParams(window.location.search);
    const urlQuery = params.get("query");
    const urlPage = params.get("page");
    const urlPerPage = params.get("perPage");
    const urlSort = params.get("sort") as SortOption | null;
    const urlHasRepo = params.get("hasRepo");
    const urlHasHomepage = params.get("hasHomepage");
    const urlUpdatedWithinMonths = params.get("updatedWithinMonths");

    if (urlQuery) {
      query.value = urlQuery;
    }
    if (urlPage) {
      const parsed = Number.parseInt(urlPage, 10);
      if (!Number.isNaN(parsed) && parsed > 0) {
        page.value = parsed;
      }
    }
    if (urlPerPage) {
      const parsed = Number.parseInt(urlPerPage, 10);
      if (PER_PAGE_OPTIONS.includes(parsed as typeof PER_PAGE_OPTIONS[number])) {
        perPage.value = parsed as typeof PER_PAGE_OPTIONS[number];
      }
    }
    if (urlSort && SORT_OPTIONS.some((option) => option.value === urlSort)) {
      sort.value = urlSort;
    }
    filters.hasRepository = urlHasRepo === "1";
    filters.hasHomepage = urlHasHomepage === "1";
    if (urlUpdatedWithinMonths) {
      const parsed = Number.parseInt(urlUpdatedWithinMonths, 10);
      filters.updatedWithinMonths = Number.isNaN(parsed) ? null : parsed;
    }
  }

  watch(
    [
      query,
      page,
      perPage,
      sort,
      () => filters.hasRepository,
      () => filters.hasHomepage,
      () => filters.updatedWithinMonths,
    ],
    () => {
      syncToUrl();
    },
  );

  watch(perPage, (current, previous) => {
    if (current !== previous) {
      page.value = 1;
      if (hasSearched.value) {
        void executeSearch();
      }
    }
  });

  onMounted(() => {
    loadFromUrl();
    syncToUrl();
  });

  onBeforeUnmount(() => {
    abortController.value?.abort();
  });

  return {
    query,
    apiKey,
    perPage,
    page,
    sort,
    filters,
    plugins,
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
    perPageOptions: PER_PAGE_OPTIONS,
    sortOptions: SORT_OPTIONS,
    recentUpdateFilters: RECENT_MONTH_FILTERS,
  } as const;
}
