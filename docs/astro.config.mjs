import { defineConfig } from 'astro/config';
import vue from '@astrojs/vue';
import mdx from '@astrojs/mdx';
import rehypeMermaid from 'rehype-mermaid';
import astroBrokenLinksChecker from 'astro-broken-links-checker';
import icon from 'astro-icon';
import sitemap from '@astrojs/sitemap';
import starlight from '@astrojs/starlight';

export default defineConfig({
  site: 'https://openticketai.com',
  base: '/',
  outDir: './dist',
  trailingSlash: 'always',
  image: {
    // Configure image service with Sharp for optimization
    service: {
      entrypoint: 'astro/assets/services/sharp',
      config: {
        limitInputPixels: false, // Allow processing of large images
      },
    },
    domains: ['astro.build'],
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
    rehypePlugins: [[rehypeMermaid, { strategy: 'img-svg', dark: true }]],
  },
  vite: {
    define: {
      __VUE_PROD_DEVTOOLS__: 'false',
    },
  },
  integrations: [
    sitemap(),
    icon({
      collections: {
        local: './src/icons',
      },
    }),
    vue({
      appEntrypoint: '/src/vue-app.js',
    }),
    starlight({
      title: 'Open Ticket AI Docs',
      defaultLocale: 'en',
      locales: {
        en: {
          label: 'English',
          lang: 'en',
        },
        de: {
          label: 'Deutsch',
          lang: 'de',
        },
      },
      customCss: ['./src/styles/starlight-custom.css'],
      sidebar: [
        {
          label: 'Getting Started',
          items: [
            { label: 'Overview', link: '/en/docs/' },
          ],
        },
        {
          label: 'Open Ticket Automation',
          autogenerate: { directory: 'en/docs/open-ticket-automation' },
        },
        {
          label: 'Ticket Tagging',
          autogenerate: { directory: 'en/docs/ticket-tagging' },
        },
      ],
    }),
    mdx(),
    astroBrokenLinksChecker({
      logFilePath: 'broken-links.log',
      checkExternalLinks: false,
      throwError: false,
    }),
  ],
});
