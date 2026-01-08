import {
  type FilterOptions,
  type LibrariesIoResult,
  type Plugin,
  type PluginReleaseFile,
  type PyPIFileInfo,
  type PyPIResponse,
  type SortOption,
} from "./pluginModels";

export interface LibrariesPluginDetails {
  readonly name: string;
  readonly latestVersion: string | null;
  readonly description: string;
  readonly homepage: string | null;
  readonly repositoryUrl: string | null;
  readonly projectUrl: string | null;
  readonly starCount: number;
  readonly lastReleaseDate: string | null;
  readonly normalizedLicenses: readonly string[];
}

export interface PyPIPluginDetails {
  readonly version: string | null;
  readonly summary: string | null;
  readonly homepage: string | null;
  readonly projectUrl: string | null;
  readonly repositoryUrl: string | null;
  readonly author: string | null;
  readonly license: string | null;
  readonly releaseFiles: readonly PluginReleaseFile[];
  readonly lastReleaseDate: string | null;
}

const FALLBACK_SUMMARY = "No description available.";

const REPOSITORY_KEYS = ["Source", "Homepage", "Repository", "Code", "source", "repository"];

function coalesceString(value: string | null | undefined): string | null {
  if (value === null || value === undefined) {
    return null;
  }
  const trimmed = value.trim();
  return trimmed.length === 0 ? null : trimmed;
}

function normaliseDate(input: string | null | undefined): string | null {
  if (!input) {
    return null;
  }
  const date = new Date(input);
  if (Number.isNaN(date.getTime())) {
    return null;
  }
  return date.toISOString();
}

function extractLatestUploadDate(files: readonly PyPIFileInfo[] | undefined): string | null {
  if (!files || files.length === 0) {
    return null;
  }
  const timestamps = files
    .map((file) => file.upload_time_iso_8601)
    .filter((value): value is string => Boolean(value));
  if (timestamps.length === 0) {
    return null;
  }
  const latestTimestamp = timestamps.reduce((latest, current) =>
    new Date(current).getTime() > new Date(latest).getTime() ? current : latest,
  );
  return normaliseDate(latestTimestamp);
}

function buildReleaseFiles(files: readonly PyPIFileInfo[] | undefined): readonly PluginReleaseFile[] {
  if (!files) {
    return [];
  }
  return files
    .map((file) => ({
      filename: file.filename,
      url: file.url,
      pythonVersion: file.python_version ?? null,
      uploadedAt: normaliseDate(file.upload_time_iso_8601),
      packageType: file.packagetype ?? null,
    }))
    .sort((a, b) => {
      if (!a.uploadedAt && !b.uploadedAt) {
        return 0;
      }
      if (!a.uploadedAt) {
        return 1;
      }
      if (!b.uploadedAt) {
        return -1;
      }
      return new Date(b.uploadedAt).getTime() - new Date(a.uploadedAt).getTime();
    });
}

export function mapLibrariesIoPackage(pkg: LibrariesIoResult): LibrariesPluginDetails {
  return {
    name: pkg.name,
    latestVersion: coalesceString(pkg.latest_release_number ?? null),
    description: coalesceString(pkg.description ?? null) ?? FALLBACK_SUMMARY,
    homepage: coalesceString(pkg.homepage ?? null),
    repositoryUrl: coalesceString(pkg.repository_url ?? null),
    projectUrl: coalesceString(pkg.project_url ?? null),
    starCount: pkg.stars ?? pkg.stargazers_count ?? 0,
    lastReleaseDate: normaliseDate(pkg.latest_release_published ?? null),
    normalizedLicenses: pkg.normalized_licenses ?? [],
  };
}

function pickRepositoryUrl(projectUrls: Record<string, string> | null | undefined): string | null {
  if (!projectUrls) {
    return null;
  }
  for (const key of REPOSITORY_KEYS) {
    const url = projectUrls[key];
    if (url) {
      return url;
    }
  }
  const firstUrl = Object.values(projectUrls)[0];
  return firstUrl ?? null;
}

export function mapPyPIPackage(response: PyPIResponse | null | undefined): PyPIPluginDetails | null {
  if (!response) {
    return null;
  }
  const projectUrls = response.info.project_urls ?? null;
  const repositoryUrl = coalesceString(pickRepositoryUrl(projectUrls));
  const homepage = coalesceString(response.info.home_page ?? null) ?? coalesceString(projectUrls?.Homepage ?? null);
  const releaseFiles = buildReleaseFiles(response.urls);
  const releaseDateFromUrls = extractLatestUploadDate(response.urls);
  const version = coalesceString(response.info.version ?? null);
  const releasesForVersion = version ? response.releases?.[version] : undefined;
  const releaseDateFromReleases = extractLatestUploadDate(releasesForVersion);

  return {
    version,
    summary: coalesceString(response.info.summary ?? null),
    homepage,
    projectUrl: coalesceString(response.info.project_url ?? null),
    repositoryUrl,
    author: coalesceString(response.info.author ?? null),
    license: coalesceString(response.info.license ?? null),
    releaseFiles,
    lastReleaseDate: releaseDateFromUrls ?? releaseDateFromReleases,
  };
}

export function mergePluginData(
  libraryDetails: LibrariesPluginDetails,
  pyPiDetails: PyPIPluginDetails | null,
): Plugin {
  const version = pyPiDetails?.version ?? libraryDetails.latestVersion ?? "Unknown";
  const summary = pyPiDetails?.summary ?? libraryDetails.description ?? FALLBACK_SUMMARY;
  const homepage = pyPiDetails?.homepage ?? libraryDetails.homepage ?? null;
  const repositoryUrl = pyPiDetails?.repositoryUrl ?? libraryDetails.repositoryUrl ?? null;
  const projectUrl = pyPiDetails?.projectUrl ?? libraryDetails.projectUrl;
  const license = pyPiDetails?.license ?? libraryDetails.normalizedLicenses.at(0) ?? null;
  const lastReleaseDate = pyPiDetails?.lastReleaseDate ?? libraryDetails.lastReleaseDate ?? null;

  return {
    name: libraryDetails.name,
    version,
    summary,
    homepage,
    pypiUrl: projectUrl ?? `https://pypi.org/project/${libraryDetails.name}/`,
    repositoryUrl,
    lastReleaseDate,
    starCount: libraryDetails.starCount,
    author: pyPiDetails?.author ?? null,
    license,
    releaseFiles: pyPiDetails?.releaseFiles ?? [],
  };
}

function isWithinMonths(dateIso: string | null, months: number): boolean {
  if (!dateIso) {
    return false;
  }
  const date = new Date(dateIso);
  if (Number.isNaN(date.getTime())) {
    return false;
  }
  const now = new Date();
  const threshold = new Date(now.getFullYear(), now.getMonth() - months, now.getDate());
  return date >= threshold;
}

export function filterPlugins(plugins: readonly Plugin[], filters: FilterOptions): readonly Plugin[] {
  return plugins.filter((plugin) => {
    if (filters.hasRepository && !plugin.repositoryUrl) {
      return false;
    }
    if (filters.hasHomepage && !plugin.homepage) {
      return false;
    }
    if (filters.updatedWithinMonths !== null && !isWithinMonths(plugin.lastReleaseDate, filters.updatedWithinMonths)) {
      return false;
    }
    return true;
  });
}

export function sortPlugins(plugins: readonly Plugin[], sort: SortOption): readonly Plugin[] {
  const copy = [...plugins];
  switch (sort) {
    case "stars":
      return copy.sort((a, b) => b.starCount - a.starCount);
    case "lastRelease":
      return copy.sort((a, b) => {
        if (!a.lastReleaseDate && !b.lastReleaseDate) {
          return 0;
        }
        if (!a.lastReleaseDate) {
          return 1;
        }
        if (!b.lastReleaseDate) {
          return -1;
        }
        return new Date(b.lastReleaseDate).getTime() - new Date(a.lastReleaseDate).getTime();
      });
    case "name":
      return copy.sort((a, b) => a.name.localeCompare(b.name));
    default:
      return copy;
  }
}

export function filterByQuery(plugins: readonly Plugin[], rawQuery: string): readonly Plugin[] {
  const query = rawQuery.trim().toLowerCase();
  if (!query) {
    return plugins;
  }
  return plugins.filter((plugin) => {
    const name = plugin.name.toLowerCase();
    const summary = plugin.summary.toLowerCase();
    return name.includes(query) || summary.includes(query);
  });
}

export function applyFiltersAndSort(
  plugins: readonly Plugin[],
  filters: FilterOptions,
  sort: SortOption,
): readonly Plugin[] {
  return sortPlugins(filterPlugins(plugins, filters), sort);
}
