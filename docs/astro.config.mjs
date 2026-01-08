import { defineConfig } from 'astro/config';
import starlight from '@astrojs/starlight';
import vue from '@astrojs/vue';
import mdx from '@astrojs/mdx';
import rehypeMermaid from 'rehype-mermaid';

export default defineConfig({
    site: 'https://open-ticket-ai.com',
    base: '/',
    outDir: './dist',
    trailingSlash: 'always',
    markdown: {
        rehypePlugins: [[rehypeMermaid, {strategy: 'img-svg', dark: true}]],
    },
    integrations: [
        vue(),
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
                    autogenerate: {directory: 'products'},
                },
                {
                    label: 'Guides',
                    autogenerate: {directory: 'guides'},
                },
                {
                    label: 'Users',
                    autogenerate: {directory: 'users'},
                },
                {
                    label: 'Developers',
                    autogenerate: {directory: 'developers'},
                },
                {
                    label: 'Details',
                    autogenerate: {directory: 'details'},
                },
                {
                    label: 'Blog',
                    autogenerate: {directory: 'blog'},
                },
            ],
            customCss: [
                './src/styles/global.css',
                './src/styles/custom.css',
            ],
            components: {
                Head: './src/components/Head.astro',
                Content: './src/components/starlight/Content.astro',
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
        mdx(),

    ],
});
