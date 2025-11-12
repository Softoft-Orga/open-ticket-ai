import {computed, onBeforeUnmount, onMounted, reactive, ref, watch} from "vue";
import {
    type FilterOptions,
    type LibrariesIoResult,
    PER_PAGE_OPTIONS,
    type Plugin,
    type PyPIResponse,
    RECENT_MONTH_FILTERS,
    SORT_OPTIONS,
    type SortOption,
} from "../components/marketplace/pluginModels";
import {
    applyFiltersAndSort,
    filterByQuery,
    type LibrariesPluginDetails,
    mapLibrariesIoPackage,
    mapPyPIPackage,
    mergePluginData,
    type PyPIPluginDetails,
} from "../components/marketplace/pluginUtils";

const LIBRARIES_IO_ENDPOINT = "https://libraries.io/api/search";
const PYPI_ENDPOINT = "https://pypi.org/pypi";
const PYPI_CONCURRENCY = 5;
const LIBRARIES_API_KEY = "18471256fa1f391576e081b21d89598d";
const LIBRARIES_PAGE_SIZE = 100;
const SEARCH_PREFIX = "otai";
const MAX_LIBRARIES_PAGES = 10;

export function usePluginsMarketplace() {
    const query = ref("");
    const perPage = ref<typeof PER_PAGE_OPTIONS[number]>(PER_PAGE_OPTIONS[0]);
    const page = ref(1);
    const sort = ref<SortOption>("name");
    const filters = reactive<FilterOptions>({
        hasRepository: false,
        hasHomepage: false,
        updatedWithinMonths: null,
    });

    const plugins = ref<Plugin[]>([]);
    const isLoading = ref(false);
    const errorMessage = ref<string | null>(null);
    const hasLoaded = ref(false);

    const abortController = ref<AbortController | null>(null);
    const pyPiCache = new Map<string, PyPIPluginDetails | null>();

    const filteredPlugins = computed(() =>
        applyFiltersAndSort(filterByQuery(plugins.value, query.value), filters, sort.value),
    );
    const totalResults = computed(() => filteredPlugins.value.length);
    const totalPages = computed(() => {
        if (totalResults.value === 0) {
            return 1;
        }
        return Math.max(1, Math.ceil(totalResults.value / perPage.value));
    });
    const visiblePlugins = computed(() => {
        const start = (page.value - 1) * perPage.value;
        const end = start + perPage.value;
        return filteredPlugins.value.slice(start, end);
    });
    const filtersApplied = computed(
        () => filters.hasHomepage || filters.hasRepository || filters.updatedWithinMonths !== null,
    );
    const hasMoreResults = computed(() => page.value < totalPages.value);
    const dateFormatter = computed(() => new Intl.DateTimeFormat(undefined, {dateStyle: "medium"}));

    const isInitializing = ref(true);

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

    function buildSearchUrl(currentPage: number): string {
        const url = new URL(LIBRARIES_IO_ENDPOINT);
        url.searchParams.set("q", SEARCH_PREFIX);
        url.searchParams.set("platforms", "PyPI");
        url.searchParams.set("per_page", String(LIBRARIES_PAGE_SIZE));
        url.searchParams.set("page", String(currentPage));
        url.searchParams.set("api_key", LIBRARIES_API_KEY);
        return url.toString();
    }

    async function loadPyPiPackage(name: string, signal: AbortSignal): Promise<PyPIPluginDetails | null> {
        if (pyPiCache.has(name)) {
            return pyPiCache.get(name) ?? null;
        }
        try {
            const response = await fetch(`${PYPI_ENDPOINT}/${encodeURIComponent(name)}/json`, {
                signal,
                headers: {Accept: "application/json"},
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
            {length: Math.min(PYPI_CONCURRENCY, packages.length)},
            () => worker(),
        );
        await Promise.all(workers);
        return results;
    }

    async function fetchAllPlugins(): Promise<void> {
        abortController.value?.abort();
        const controller = new AbortController();
        abortController.value = controller;

        isLoading.value = true;
        errorMessage.value = null;
        hasLoaded.value = false;

        try {
            const aggregatedPlugins: Plugin[] = [];
            const seenNames = new Set<string>();
            for (let currentPage = 1; currentPage <= MAX_LIBRARIES_PAGES; currentPage += 1) {
                const response = await fetch(buildSearchUrl(currentPage), {
                    signal: controller.signal,
                    headers: {Accept: "application/json"},
                });

                if (response.status === 401 || response.status === 403) {
                    plugins.value = [];
                    errorMessage.value = "Libraries.io API request was rejected. Please verify the configured key.";
                    return;
                }

                if (response.status === 429) {
                    plugins.value = [];
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

                if (libraryPackages.length === 0) {
                    break;
                }

                const pyPiResults = await fetchPyPiDetails(libraryPackages, controller.signal);
                for (const pkg of libraryPackages) {
                    if (seenNames.has(pkg.name)) {
                        continue;
                    }
                    seenNames.add(pkg.name);
                    aggregatedPlugins.push(mergePluginData(pkg, pyPiResults.get(pkg.name) ?? null));
                }

                if (libraryPackages.length < LIBRARIES_PAGE_SIZE) {
                    break;
                }
            }

            plugins.value = aggregatedPlugins;
            hasLoaded.value = true;
        } catch (error) {
            if (error instanceof DOMException && error.name === "AbortError") {
                return;
            }
            plugins.value = [];
            errorMessage.value =
                error instanceof Error ? error.message : "Something went wrong while fetching plugins.";
        } finally {
            if (abortController.value === controller) {
                isLoading.value = false;
                if (!errorMessage.value) {
                    hasLoaded.value = true;
                }
            }
        }
    }

    function search(): void {
        page.value = 1;
    }

    function goToPreviousPage(): void {
        if (page.value === 1) {
            return;
        }
        page.value -= 1;
    }

    function goToNextPage(): void {
        if (!hasMoreResults.value) {
            return;
        }
        page.value += 1;
    }

    function clearFilters(): void {
        filters.hasHomepage = false;
        filters.hasRepository = false;
        filters.updatedWithinMonths = null;
        page.value = 1;
    }

    function updateFilters(partial: Partial<FilterOptions>): void {
        Object.assign(filters, partial);
        page.value = 1;
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
        if (current !== previous && !isInitializing.value) {
            page.value = 1;
        }
    });

    watch(query, () => {
        if (!isInitializing.value) {
            page.value = 1;
        }
    });

    watch(sort, () => {
        if (!isInitializing.value) {
            page.value = 1;
        }
    });

    watch(filteredPlugins, () => {
        if (page.value > totalPages.value) {
            page.value = totalPages.value;
        }
    });

    onMounted(() => {
        loadFromUrl();
        syncToUrl();
        isInitializing.value = false;
        void fetchAllPlugins();
    });

    onBeforeUnmount(() => {
        abortController.value?.abort();
    });

    return {
        query,
        perPage,
        page,
        sort,
        filters,
        plugins,
        filteredPlugins,
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
        perPageOptions: PER_PAGE_OPTIONS,
        sortOptions: SORT_OPTIONS,
        recentUpdateFilters: RECENT_MONTH_FILTERS,
    } as const;
}
