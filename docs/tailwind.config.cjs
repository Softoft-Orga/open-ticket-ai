// tailwind.config.cjs
module.exports = {
    content: [
        './docs_src/**/*.{vue,js,ts,jsx,tsx,md}',
        './.vitepress/**/*.{vue,js,ts}',
        './stories/**/*.{js,ts,jsx,tsx}',
    ],
    theme: {
        extend: {
            colors: {
                // VitePress theme palettes
                'vp-bg': 'var(--vp-c-bg)',
                'vp-bg-soft': 'var(--vp-c-bg-soft)',
                'vp-bg-invert': 'var(--vp-c-bg-invert)',
                'vp-border': 'var(--vp-c-divider)',

                'vp-text-1': 'var(--vp-c-text-1)',
                'vp-text-2': 'var(--vp-c-text-2)',
                'vp-link': 'var(--vp-c-link)',
                'vp-link-hover': 'var(--vp-c-link-hover)',

                'vp-brand-1': 'var(--vp-c-brand-1)',
                'vp-brand-2': 'var(--vp-c-brand-2)',
                'vp-brand-3': 'var(--vp-c-brand-3)',
                'vp-brand-soft': 'var(--vp-c-brand-soft)',

                'vp-blockquote-bg': 'var(--vp-c-blockquote-bg)',
                'vp-code-bg': 'var(--vp-c-code-bg)',
                'vp-pre-bg': 'var(--vp-c-pre-bg)',
                'vp-table-border': 'var(--vp-c-table-border)',
            },
        },
    },
    plugins: [],
}
