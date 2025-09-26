// Composable: useFooterPages
// Purpose: Build footer sections from VitePress page frontmatter at build-time.
// - Includes only pages with `footerSection` set in frontmatter
// - Derives labels via i18n key -> explicit label -> frontmatter.title -> page.title -> humanized filename
// - Generates locale-prefixed hrefs using vue-i18n current locale
//
// Example frontmatter:
// ---
// title: Installation & Setup
// footerSection: Solutions
// footerOrder: 20
// footerLabelKey: 'footer.install'  // optional i18n key (uses t('footer.install'))
// footerLabel: 'Install & Setup'     // optional explicit label
// navKey: 'nav.install'              // optional fallback i18n key
// ---
//
// Usage in components:
// const { sections, map, withLocale } = useFooterPages()
// <a :href="withLocale(item.href)">{{ item.label }}</a>

import { computed, type ComputedRef } from 'vue'
import { useI18n } from 'vue-i18n'

// ---- Interfaces ----
export interface FooterItemConfig {
  footerSection?: string
  footerLabelKey?: string
  footerLabel?: string
  footerOrder?: number
  navKey?: string
  title?: string
}

export interface FooterItem {
  href: string
  label: string
  order: number
  // raw page data if a consumer needs it
  page?: VitePressPageData
}

export interface FooterSectionInterface {
  title: string
  items: FooterItem[]
}

// Minimal shape of VitePress page data embedded in modules as `__pageData`
export interface VitePressPageData {
  relativePath: string
  title?: string
  frontmatter?: Record<string, any> & FooterItemConfig
}

export interface UseFooterPagesOptions {
  /** Override the glob used to find .md files, relative to this file */
  glob?: string
  /** Optional explicit list to order sections. Unlisted sections follow alphabetically. */
  sectionsOrder?: string[]
}

// ---- Implementation ----
export function useFooterPages(options: UseFooterPagesOptions = {}) {
  const { locale, t } = useI18n()

  const globPattern = options.glob ?? '../../**/*.md'
  // `eager: true` bakes the data at build time. Works in VitePress theme/runtime.
  const pageModules = import.meta.glob(globPattern, { eager: true }) as Record<string, any>

  function parsePage(mod: any): VitePressPageData | null {
    try {
      const data = JSON.parse(mod.__pageData)
      if (!data || typeof data !== 'object') return null
      if (typeof data.relativePath !== 'string') return null
      data.frontmatter = data.frontmatter && typeof data.frontmatter === 'object' ? data.frontmatter : {}
      return data as VitePressPageData
    } catch {
      return null
    }
  }

  const pages = Object.values(pageModules)
    .map(parsePage)
    .filter((p): p is VitePressPageData => !!p && typeof p.relativePath === 'string')

  function routeFromRelative(rel: string): string {
    // Remove trailing index.md or .md and ensure folder-style url
    let p = '/' + rel
      .replace(/(^|\/)index\.md$/, '$1')
      .replace(/\.md$/, '/')
    return p.replace(/\/+/, '/')
  }

  function humanizePath(rel: string): string {
    const base = rel.split('/').pop()?.replace(/\.md$/, '') ?? ''
    return base.replace(/[-_]+/g, ' ').replace(/\b\w/g, (c) => c.toUpperCase())
  }

  // Map of section -> items
  const map: ComputedRef<Record<string, FooterItem[]>> = computed(() => {
    const dict: Record<string, FooterItem[]> = {}
    for (const p of pages) {
      const fm = (p.frontmatter ?? {}) as FooterItemConfig
      const section = fm.footerSection
      if (!section) continue

      // Label resolution: i18n key -> explicit label -> titles -> filename
      const i18nKey = fm.footerLabelKey || fm.navKey
      const labelFromI18n = i18nKey ? t(i18nKey) : ''
      const label = String(
        labelFromI18n || fm.footerLabel || fm.title || p.title || humanizePath(p.relativePath)
      )

      const href = routeFromRelative(p.relativePath)
      const order = typeof fm.footerOrder === 'number' ? fm.footerOrder : 999

      if (!dict[section]) dict[section] = []
      dict[section].push({ href, label, order, page: p })
    }

    // Stable sorting inside each section
    for (const key of Object.keys(dict)) {
      dict[key].sort((a, b) => (a.order - b.order) || a.label.localeCompare(b.label))
    }
    return dict
  })

  const sections: ComputedRef<FooterSectionInterface[]> = computed(() => {
    const order = options.sectionsOrder ?? []
    const all = Object.keys(map.value)
    const ordered: string[] = [
      ...order.filter((k) => map.value[k]),
      ...all.filter((k) => !order.includes(k)).sort()
    ]
    return ordered.map((title) => ({ title, items: map.value[title] }))
  })

  const langCode = computed(() => (locale.value || 'en').split('-')[0])
  const withLocale = (path: string) => `/${langCode.value}${path}`.replace('//', '/')

  return { sections, map, withLocale }
}
