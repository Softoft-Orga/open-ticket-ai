import { describe, expect, it } from "vitest";
import {
  applyFiltersAndSort,
  filterByQuery,
  filterPlugins,
  mapLibrariesIoPackage,
  mapPyPIPackage,
  mergePluginData,
  sortPlugins,
} from "../../.vitepress/components/marketplace/pluginUtils";
import type {
  LibrariesIoResult,
  Plugin,
  PyPIResponse,
} from "../../.vitepress/components/marketplace/pluginModels";

describe("plugin mapping", () => {
  it("maps Libraries.io packages with fallbacks", () => {
    const payload: LibrariesIoResult = {
      name: "otai-sample",
      latest_release_number: "1.2.3",
      latest_release_published: "2024-10-01T10:15:00Z",
      description: "Test description",
      homepage: "https://example.com",
      repository_url: "https://github.com/example/otai-sample",
      project_url: "https://pypi.org/project/otai-sample/",
      normalized_licenses: ["MIT"],
      stars: 42,
    };

    const result = mapLibrariesIoPackage(payload);

    expect(result).toEqual({
      name: "otai-sample",
      latestVersion: "1.2.3",
      description: "Test description",
      homepage: "https://example.com",
      repositoryUrl: "https://github.com/example/otai-sample",
      projectUrl: "https://pypi.org/project/otai-sample/",
      starCount: 42,
      lastReleaseDate: "2024-10-01T10:15:00.000Z",
      normalizedLicenses: ["MIT"],
    });
  });

  it("maps PyPI metadata and extracts latest release details", () => {
    const payload: PyPIResponse = {
      info: {
        version: "2.0.0",
        summary: "PyPI summary",
        home_page: "https://docs.example.com",
        project_url: "https://pypi.org/project/otai-sample/",
        project_urls: {
          Source: "https://github.com/example/otai-sample",
        },
        author: "Open Ticket AI",
        license: "Apache-2.0",
      },
      releases: {
        "2.0.0": [
          {
            filename: "otai-sample-2.0.0.tar.gz",
            url: "https://files.pythonhosted.org/otai-sample-2.0.0.tar.gz",
            python_version: "py3",
            packagetype: "sdist",
            upload_time_iso_8601: "2024-11-01T12:00:00Z",
          },
        ],
      },
      urls: [
        {
          filename: "otai-sample-2.0.0-py3-none-any.whl",
          url: "https://files.pythonhosted.org/otai-sample-2.0.0-py3-none-any.whl",
          python_version: "py3",
          packagetype: "bdist_wheel",
          upload_time_iso_8601: "2024-11-01T13:00:00Z",
        },
      ],
    };

    const result = mapPyPIPackage(payload);

    expect(result).toEqual({
      version: "2.0.0",
      summary: "PyPI summary",
      homepage: "https://docs.example.com",
      projectUrl: "https://pypi.org/project/otai-sample/",
      repositoryUrl: "https://github.com/example/otai-sample",
      author: "Open Ticket AI",
      license: "Apache-2.0",
      releaseFiles: [
        {
          filename: "otai-sample-2.0.0-py3-none-any.whl",
          url: "https://files.pythonhosted.org/otai-sample-2.0.0-py3-none-any.whl",
          pythonVersion: "py3",
          uploadedAt: "2024-11-01T13:00:00.000Z",
          packageType: "bdist_wheel",
        },
      ],
      lastReleaseDate: "2024-11-01T13:00:00.000Z",
    });
  });

  it("merges Libraries.io and PyPI data with sensible fallbacks", () => {
    const libraries = mapLibrariesIoPackage({
      name: "otai-sample",
      latest_release_number: "1.0.0",
      latest_release_published: "2023-06-01T09:00:00Z",
      description: "Libraries description",
      project_url: null,
      repository_url: null,
      homepage: null,
      stars: 5,
      normalized_licenses: ["MIT"],
    } as LibrariesIoResult);

    const plugin = mergePluginData(libraries, null);

    expect(plugin).toEqual({
      name: "otai-sample",
      version: "1.0.0",
      summary: "Libraries description",
      homepage: null,
      pypiUrl: "https://pypi.org/project/otai-sample/",
      repositoryUrl: null,
      lastReleaseDate: "2023-06-01T09:00:00.000Z",
      starCount: 5,
      author: null,
      license: "MIT",
      releaseFiles: [],
    });
  });
});

describe("plugin sorting and filtering", () => {
  const now = new Date();
  const recent = new Date(now.getTime());
  recent.setMonth(recent.getMonth() - 2);
  const stale = new Date(2000, 0, 1);

  const basePlugins: Plugin[] = [
    {
      name: "otai-alpha",
      version: "1.0.0",
      summary: "Alpha plugin",
      homepage: "https://alpha.example.com",
      pypiUrl: "https://pypi.org/project/otai-alpha/",
      repositoryUrl: "https://github.com/example/otai-alpha",
      lastReleaseDate: recent.toISOString(),
      starCount: 50,
      author: "Alpha",
      license: "MIT",
      releaseFiles: [],
    },
    {
      name: "otai-beta",
      version: "0.5.0",
      summary: "Beta plugin",
      homepage: null,
      pypiUrl: "https://pypi.org/project/otai-beta/",
      repositoryUrl: null,
      lastReleaseDate: stale.toISOString(),
      starCount: 10,
      author: "Beta",
      license: null,
      releaseFiles: [],
    },
  ];

  it("filters plugins by repository, homepage, and recency", () => {
    const filtered = filterPlugins(basePlugins, {
      hasRepository: true,
      hasHomepage: true,
      updatedWithinMonths: 6,
    });

    expect(filtered).toHaveLength(1);
    expect(filtered[0]?.name).toBe("otai-alpha");
  });

  it("sorts plugins by stars and release date", () => {
    const byStars = sortPlugins(basePlugins, "stars");
    expect(byStars[0]?.name).toBe("otai-alpha");

    const byRelease = sortPlugins(basePlugins, "lastRelease");
    expect(byRelease[0]?.name).toBe("otai-alpha");

    const byName = sortPlugins(basePlugins, "name");
    expect(byName.map((plugin) => plugin.name)).toEqual(["otai-alpha", "otai-beta"]);
  });

  it("applies filters and sorting together", () => {
    const filtered = applyFiltersAndSort(basePlugins, {
      hasRepository: false,
      hasHomepage: false,
      updatedWithinMonths: null,
    }, "name");

    expect(filtered.map((plugin) => plugin.name)).toEqual(["otai-alpha", "otai-beta"]);
  });

  it("filters plugins by query against name and summary", () => {
    const byName = filterByQuery(basePlugins, "beta");
    expect(byName).toHaveLength(1);
    expect(byName[0]?.name).toBe("otai-beta");

    const bySummary = filterByQuery(basePlugins, "alpha plugin");
    expect(bySummary).toHaveLength(1);
    expect(bySummary[0]?.name).toBe("otai-alpha");

    const empty = filterByQuery(basePlugins, "");
    expect(empty).toHaveLength(basePlugins.length);
  });
});
