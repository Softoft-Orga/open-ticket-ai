/**
 * Astro middleware for browser language-based redirect
 * Redirects first-time visitors to their preferred locale if not English
 */
import { defineMiddleware } from 'astro:middleware';
import { getPreferredLocale } from './lib/i18nLinks';

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
