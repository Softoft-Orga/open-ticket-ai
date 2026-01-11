/**
 * i18n link utilities for converting canonical internal links to locale-aware URLs
 * This is the single source of truth for link localization across the entire site.
 */

const SUPPORTED_LOCALES = ['en', 'de'] as const;
const DEFAULT_LOCALE = 'en';

export type Locale = typeof SUPPORTED_LOCALES[number];

/**
 * Checks if a URL is external (http/https/mailto/tel)
 */
function isExternalUrl(href: string): boolean {
    return /^(https?:\/\/|mailto:|tel:)/.test(href);
}

/**
 * Checks if a URL is a hash link (#...)
 */
function isHashLink(href: string): boolean {
    return href.startsWith('#');
}

/**
 * Checks if a URL is an internal absolute path starting with "/"
 */
function isInternalAbsolutePath(href: string): boolean {
    return href.startsWith('/') && !isExternalUrl(href);
}

/**
 * Checks if the path already has a locale prefix
 */
function hasLocalePrefix(path: string): boolean {
    const firstSegment = path.split('/').filter(Boolean)[0];
    return SUPPORTED_LOCALES.includes(firstSegment as Locale);
}

/**
 * Converts a canonical internal link to a locale-aware URL
 * 
 * @param href - The canonical href (e.g., "/docs", "/products", "https://example.com", "#hash")
 * @param locale - The current locale (defaults to 'en')
 * @returns The locale-aware URL
 * 
 * Examples:
 * - External URLs: "https://example.com" -> "https://example.com"
 * - Hash links: "#section" -> "#section"
 * - Internal (en): "/docs" -> "/docs"
 * - Internal (de): "/docs" -> "/de/docs"
 * - Already prefixed: "/de/docs" -> "/de/docs" (no change)
 */
export function localizeHref(href: string, locale: Locale = DEFAULT_LOCALE): string {
    // Return unchanged for external URLs
    if (isExternalUrl(href)) {
        return href;
    }

    // Return unchanged for hash links
    if (isHashLink(href)) {
        return href;
    }

    // For internal absolute paths
    if (isInternalAbsolutePath(href)) {
        // If path already has a locale prefix, return as-is
        if (hasLocalePrefix(href)) {
            return href;
        }

        // For default locale (en), no prefix needed
        if (locale === DEFAULT_LOCALE) {
            return href;
        }

        // Add locale prefix for non-default locales
        return `/${locale}${href}`;
    }

    // For relative paths, return as-is (they'll be resolved relative to current page)
    // In practice, we prefer absolute canonical paths
    return href;
}

/**
 * Extract the current locale from a URL path
 * 
 * @param pathname - The pathname to check (e.g., "/de/docs", "/products")
 * @returns The detected locale or default locale
 */
export function getLocaleFromPath(pathname: string): Locale {
    const firstSegment = pathname.split('/').filter(Boolean)[0];
    
    if (SUPPORTED_LOCALES.includes(firstSegment as Locale)) {
        return firstSegment as Locale;
    }
    
    return DEFAULT_LOCALE;
}

/**
 * Get the preferred locale from browser Accept-Language header
 * 
 * @param acceptLanguage - The Accept-Language header value
 * @returns The preferred locale from supported locales, or default locale
 */
export function getPreferredLocale(acceptLanguage: string | null): Locale {
    if (!acceptLanguage) {
        return DEFAULT_LOCALE;
    }

    // Parse Accept-Language header (e.g., "de-DE,de;q=0.9,en-US;q=0.8,en;q=0.7")
    const languages = acceptLanguage
        .split(',')
        .map(lang => {
            const [code, qStr] = lang.trim().split(';');
            const q = qStr ? parseFloat(qStr.split('=')[1]) : 1.0;
            return { code: code.split('-')[0].toLowerCase(), q };
        })
        .sort((a, b) => b.q - a.q);

    // Find first supported locale
    for (const { code } of languages) {
        if (SUPPORTED_LOCALES.includes(code as Locale)) {
            return code as Locale;
        }
    }

    return DEFAULT_LOCALE;
}
