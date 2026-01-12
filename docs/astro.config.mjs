import { defineConfig } from 'astro/config';
import vue from '@astrojs/vue';
import mdx from '@astrojs/mdx';
import rehypeMermaid from 'rehype-mermaid';
import astroBrokenLinksChecker from 'astro-broken-links-checker';

export default defineConfig({
    site: 'https://openticketai.com',
    base: '/',
    outDir: './dist',
    trailingSlash: 'always',
    i18n: {
        locales: ['en', 'de'],
        defaultLocale: 'en',
        routing: {
            prefixDefaultLocale: false,
        },
    },
    image: {
        // Configure image service with Sharp for optimization
        service: {
            entrypoint: 'astro/assets/services/sharp',
            config: {
                limitInputPixels: false, // Allow processing of large images
            },
        },
        // Authorized domains for remote image optimization
        domains: ['astro.build', 'doc.otobo.org', 'softoft.sirv.com'],
        // Remote image patterns for external images
        remotePatterns: [
            {
                protocol: 'https',
                hostname: '**.githubusercontent.com',
            },
            {
                protocol: 'https',
                hostname: '**.sirv.com',
            },
        ],
    },
    markdown: {
        rehypePlugins: [[rehypeMermaid, {strategy: 'img-svg', dark: true}]],
    },
    vite: {
        define: {
            '__VUE_PROD_DEVTOOLS__': 'false',
        },
    },
    integrations: [
        vue({
            appEntrypoint: '/src/vue-app.js'
        }),
        mdx(),
        astroBrokenLinksChecker({
            logFilePath: 'broken-links.log',
            checkExternalLinks: false,
            throwError: false,
        }),
    ],
});
