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
          label: 'Guides',
          items: [
            { slug: 'en/open-ticket-automation/guides/index' },
            { slug: 'en/open-ticket-automation/guides/quick_start' },
            { slug: 'en/open-ticket-automation/guides/first_pipeline' },
            { slug: 'en/open-ticket-automation/guides/plan-ticket-automation-project' },
          ],
        },
        {
          label: 'Users',
          items: [
            { slug: 'en/open-ticket-automation/users/index' },
            { slug: 'en/open-ticket-automation/users/installation' },
            { slug: 'en/open-ticket-automation/users/otobo-znuny-plugin-setup' },
            { slug: 'en/open-ticket-automation/users/pipeline' },
            { slug: 'en/open-ticket-automation/users/plugins' },
            { slug: 'en/open-ticket-automation/users/plugin-marketplace' },
            { slug: 'en/open-ticket-automation/users/config_rendering' },
            { slug: 'en/open-ticket-automation/users/config_examples' },
          ],
        },
        {
          label: 'Developers',
          items: [
            { slug: 'en/open-ticket-automation/developers/index' },
            { slug: 'en/open-ticket-automation/developers/plugin_development' },
            { slug: 'en/open-ticket-automation/developers/pipeline_code' },
            { slug: 'en/open-ticket-automation/developers/ticket_system_integration' },
            { slug: 'en/open-ticket-automation/developers/template_rendering' },
            { slug: 'en/open-ticket-automation/developers/config_rendering' },
            { slug: 'en/open-ticket-automation/developers/services' },
            { slug: 'en/open-ticket-automation/developers/dependency_injection' },
            { slug: 'en/open-ticket-automation/developers/logging' },
            { slug: 'en/open-ticket-automation/developers/testing' },
          ],
        },
        {
          label: 'Details',
          items: [
            { slug: 'en/open-ticket-automation/details/index' },
            { slug: 'en/open-ticket-automation/details/config_reference' },
            { slug: 'en/open-ticket-automation/details/predefined-pipes' },
            { slug: 'en/open-ticket-automation/details/template_rendering' },
          ],
        },
        {
          label: 'Ticket Tagging',
          items: [
            { slug: 'en/ticket-tagging/taxonomy-design' },
            { slug: 'en/ticket-tagging/tag-mapping' },
            { slug: 'en/ticket-tagging/hardware-sizing' },
          ],
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
