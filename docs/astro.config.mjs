import { defineConfig } from 'astro/config';
import starlight from '@astrojs/starlight';
import { remarkVitepressContainers } from './remark-vitepress-containers.mjs';
import rehypeMermaid from 'rehype-mermaid';

export default defineConfig({
  site: 'https://open-ticket-ai.com',
  base: '/',
  outDir: './dist',
  markdown: {
    remarkPlugins: [remarkVitepressContainers],
    rehypePlugins: [[rehypeMermaid, { strategy: 'img-svg', dark: true }]],
  },
  integrations: [
    starlight({
      title: 'Open Ticket AI',
      description: 'Open Ticket AI is an open-source, on-premise solution that auto-classifies support tickets by queue and priority—integrates with OTOBO, Znuny, and OTRS.',
      defaultLocale: 'root',
      locales: {
        root: {
          label: 'English',
          lang: 'en',
        },
      },
      social: [
        {
          label: 'GitHub',
          icon: 'github',
          href: 'https://github.com/Softoft-Orga/open-ticket-ai',
        },
      ],
      sidebar: [
        {
          label: 'Products',
          autogenerate: { directory: 'products' },
        },
        {
          label: 'Guides',
          autogenerate: { directory: 'guides' },
        },
        {
          label: 'Users',
          autogenerate: { directory: 'users' },
        },
        {
          label: 'Developers',
          autogenerate: { directory: 'developers' },
        },
        {
          label: 'Details',
          autogenerate: { directory: 'details' },
        },
        {
          label: 'Blog',
          autogenerate: { directory: 'blog' },
        },
      ],
      customCss: [
        './src/styles/custom.css',
      ],
      components: {
        Head: './src/components/Head.astro',
      },
      pagefind: true,
      lastUpdated: true,
      editLink: {
        baseUrl: 'https://github.com/Softoft-Orga/open-ticket-ai/edit/dev/docs/src/content/docs/',
      },
      expressiveCode: {
        themes: ['github-dark'],
      },
    }),
  ],
});
