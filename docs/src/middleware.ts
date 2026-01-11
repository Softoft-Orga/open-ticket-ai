/**
 * Astro middleware for browser language-based redirect
 * Redirects first-time visitors to their preferred locale if not English
 */
import { defineMiddleware } from 'astro:middleware';

// Supported locales (must match astro.config.mjs)
const SUPPORTED_LOCALES = ['en', 'de'] as const;
type Locale = typeof SUPPORTED_LOCALES[number];

/**
 * Get the preferred locale from browser Accept-Language header
 */
function getPreferredLocale(acceptLanguage: string | null): Locale {
    if (!acceptLanguage) {
        return 'en';
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

    return 'en';
}

export const onRequest = defineMiddleware(async (context, next) => {
    const { request, url, redirect } = context;
    const { pathname } = url;

    // Only handle root path "/"
    if (pathname === '/') {
        // Get preferred locale from Accept-Language header
        const acceptLanguage = request.headers.get('accept-language');
        const preferredLocale = getPreferredLocale(acceptLanguage);

        // If preferred locale is not the default (en), redirect to locale-prefixed URL
        if (preferredLocale !== 'en') {
            return redirect(`/${preferredLocale}/`, 302);
        }
    }

    // For all other paths, continue as normal
    return next();
});
