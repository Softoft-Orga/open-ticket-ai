import { defineConfig } from 'astro/config';
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
        mdx(),
    ],
});
