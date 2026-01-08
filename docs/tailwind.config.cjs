// tailwind.config.cjs
module.exports = {
    content: [
        './src/**/*.{astro,js,ts,jsx,tsx,md,mdx}',
        './src/content/docs/**/*.{md,mdx}',
        './stories/**/*.{js,ts,jsx,tsx}',
    ],
    theme: {
        extend: {
            colors: {
                'vp-brand': 'var(--vp-c-brand-1)',
                'vp-brand-1': 'var(--vp-c-brand-1)',
                'vp-brand-2': 'var(--vp-c-brand-2)',
                'vp-brand-3': 'var(--vp-c-brand-3)',
                'vp-brand-soft': 'var(--vp-c-brand-soft)',
                'background-dark': '#0a0b14',
                'surface-dark': '#13141f',
                'surface-lighter': '#1e1f2e',
                'text-dim': '#94a3b8',
                'primary': '#646cff',
                'primary-light': '#747bff',
                'border-dark': '#2d2d48',
            }
        }
    },
    plugins: [],
}
