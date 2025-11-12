export interface LibrariesIoResult {
    readonly name: string;
    readonly latest_release_number?: string | null;
    readonly latest_release_published?: string | null;
    readonly description?: string | null;
    readonly homepage?: string | null;
    readonly repository_url?: string | null;
    readonly project_url?: string | null;
    readonly normalized_licenses?: readonly string[];
    readonly stargazers_count?: number | null;
    readonly stars?: number | null;
}

export interface PyPIFileInfo {
    readonly filename: string;
    readonly url: string;
    readonly packagetype?: string | null;
    readonly python_version?: string | null;
    readonly upload_time_iso_8601?: string | null;
}

export interface PyPIResponse {
    readonly info: {
        readonly version?: string | null;
        readonly summary?: string | null;
        readonly home_page?: string | null;
        readonly project_url?: string | null;
        readonly project_urls?: Record<string, string> | null;
        readonly author?: string | null;
        readonly license?: string | null;
    };
    readonly releases?: Record<string, readonly PyPIFileInfo[]>;
    readonly urls?: readonly PyPIFileInfo[];
}

export interface PluginReleaseFile {
    readonly filename: string;
    readonly url: string;
    readonly pythonVersion: string | null;
    readonly uploadedAt: string | null;
    readonly packageType: string | null;
}

export interface Plugin {
    readonly name: string;
    readonly version: string;
    readonly summary: string;
    readonly homepage: string | null;
    readonly pypiUrl: string;
    readonly repositoryUrl: string | null;
    readonly lastReleaseDate: string | null;
    readonly starCount: number;
    readonly author: string | null;
    readonly license: string | null;
    readonly releaseFiles: readonly PluginReleaseFile[];
}

export interface FilterOptions {
    hasRepository: boolean;
    hasHomepage: boolean;
    updatedWithinMonths: number | null;
}

export type SortOption = "relevance" | "stars" | "lastRelease" | "name";

export const PER_PAGE_OPTIONS = [10, 20, 30, 50] as const;

export const SORT_OPTIONS: readonly { readonly label: string; readonly value: SortOption }[] = [
    {label: "Relevance", value: "relevance"},
    {label: "Most stars", value: "stars"},
    {label: "Latest release", value: "lastRelease"},
    {label: "Name", value: "name"},
] as const;

export const RECENT_MONTH_FILTERS: readonly { readonly label: string; readonly value: number }[] = [
    {label: "3 months", value: 3},
    {label: "6 months", value: 6},
    {label: "12 months", value: 12},
];
