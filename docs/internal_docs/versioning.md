# Open Ticket AI — Versioning Policy (Product & Docs)

**Effective:** 11.10.2025
**Starting line:** `1.0.0`

---

## 1) Semantic Versioning (Product)

We use **SemVer**: `MAJOR.MINOR.PATCH`.

* **MAJOR (1 → 2):** Breaking changes. Requires migration notes.
* **MINOR (1.1 → 1.2):** Backward-compatible features. May introduce deprecations.
* **PATCH (1.1.1 → 1.1.2):** Bug/security fixes only.

**Pre-releases:** `1.1.0-alpha.N`, `-beta.N`, `-rc.N` for public testing.

**Support window**

* **Current major (vN):** All fixes and features.
* **Previous major (vN-1):** Security/critical fixes for **6 months** after vN ships.
* **Older:** End-of-life (EOL).

**Deprecations**

* Announced in `CHANGELOG.md` under **Deprecated**.
* Remain available for the rest of the current **major**.
* Removed in the **next major**.
* Each deprecation links to a migration note.

---

## 2) Branching, Tags & Release Channels

**Git**

* Tags: every release gets a tag (e.g., `v1.0.0`).
* Long-lived branches:

  * `latest` → current stable line (what users should install now)
  * `next` → pre-releases toward the next minor/major
  * `v1`, `v2`, … → maintenance branches for each major

**Flow**

* Develop features on short-lived branches → merge into `next`.
* Stabilize → tag `1.1.0-rc.N` on `next`.
* Release → fast-forward `latest` to the new stable tag, and if it’s a **new major**, create/advance `vN`.
* Backports → cherry-pick into the relevant `vN` branch and tag patch releases there.

---

## 3) Documentation Versioning (VitePress + Netlify)

**Goals**

* One docs site **per major** (`v1`, `v2`, …).
* Root domain always shows **latest stable**.
* Older docs stay accessible but aren’t indexed.

**Domains**

* **Latest:** [https://open-ticket-ai.com](https://open-ticket-ai.com)
* **Next (pre-releases):** [https://next.open-ticket-ai.com](https://next.open-ticket-ai.com)
* **Pinned majors:** [https://v1.open-ticket-ai.com](https://v1.open-ticket-ai.com), [https://v2.open-ticket-ai.com](https://v2.open-ticket-ai.com), …

These are powered by **Netlify Branch Deploys + Branch Subdomains**.
Branches map as:

* `latest` → `open-ticket-ai.com`
* `next` → `next.open-ticket-ai.com`
* `v1` → `v1.open-ticket-ai.com`
* `v2` → `v2.open-ticket-ai.com`
* …

**Indexing & SEO**

* Only **latest** publishes a sitemap.
* Non-latest sites add `<meta name="robots" content="noindex,follow">`.
* Canonical URLs point to the matching host of that version.
* Internal links are **relative** so the same path works across versions.

**Version switcher UX**

* Navbar dropdown lists: `latest, v3, v2, v1, next`.
* Changing version preserves the current path and navigates to the corresponding subdomain.
* User preference is stored in `localStorage`.
* Optional: if a visitor opens `open-ticket-ai.com` and has a stored preference for `vN`, auto-redirect.

**Content rules per version**

* **Major changes:** live only on that major’s site (e.g., new command semantics).
* **Minor updates:** document on **latest**; for older majors, add small notes if necessary.
* **Patches:** no separate docs site; fix typos/examples inline.

---

## 4) How we communicate changes in docs

Inside pages we annotate feature availability with terse badges:

* **Added in 1.1**
* **Changed in 1.2**
* **Deprecated in 1.4**
* **Removed in 2.0**
* **Available since 1.5**

Use short in-line labels near the relevant heading or option. For longer explanations, include a **Migration** section at the bottom of the page. Each deprecation in the product changelog links to its doc’s migration note.

---

## 5) Changelog & Releases

* Repository-root `CHANGELOG.md` tracks **product** changes per SemVer with sections: **Added**, **Changed**, **Deprecated**, **Removed**, **Fixed**, **Security**.
* Each **docs** site also has a `/changelog/` page summarizing user-visible changes relevant to that major.
* Every release tag is generated from the changelog; release notes link to migration guides when needed.

---

## 6) Minimal implementation details

**Netlify**

* Enable Branch Deploys and map branch subdomains for `latest`, `next`, and each `vN`.
* Environment variable `VITE_DOCS_VERSIONS=latest,v3,v2,v1,next` to feed the switcher.
* Build command points to VitePress build; publish the generated `dist`.

**VitePress**

* Read `process.env.BRANCH || process.env.HEAD` at build time to compute `docsVersion` (`latest`, `next`, or `vN`).
* Only set `sitemap` on `latest`.
* On non-latest, inject a `noindex,follow` meta tag.
* Version switcher maps subdomain by selected version and keeps `location.pathname + search + hash`.

---

## 7) Examples

* **1.0.0** ships:

  * Branches: `latest` and `v1` are identical; both deployed.
  * Users see latest at [https://open-ticket-ai.com](https://open-ticket-ai.com) and pinned at [https://v1.open-ticket-ai.com](https://v1.open-ticket-ai.com)

* **1.1.0** ships:

  * Docs remain on **latest** only; pages add badges like **Added in 1.1**.

* **2.0.0** ships:

  * Create `v2` branch and deploy [https://v2.open-ticket-ai.com](https://v2.open-ticket-ai.com)
  * Move `latest` to point to `v2`.
  * `v1` enters maintenance for 6 months with security-only patches.

---

## 8) Quick FAQ

* **Do we ever show patch versions in the URL?** No. Patch changes don’t get their own docs site.
* **Where do pre-releases live?** On `next` ([https://next.open-ticket-ai.com](https://next.open-ticket-ai.com)).
* **How long are old majors available?** Indefinitely to read; supported for 6 months after a new major.
* **When can we remove deprecated features?** Only in the next **major**.

---

**Canonical docs:** [https://open-ticket-ai.com](https://open-ticket-ai.com)
**Versioned docs:** [https://v1.open-ticket-ai.com](https://v1.open-ticket-ai.com), [https://next.open-ticket-ai.com](https://next.open-ticket-ai.com)
