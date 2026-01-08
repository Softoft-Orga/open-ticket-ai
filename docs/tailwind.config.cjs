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
            },
            borderRadius: {
                'xl': '1rem',
                '2xl': '1.5rem',
                '3xl': '2rem',
            },
            boxShadow: {
                'card': '0 4px 6px -1px rgba(0, 0, 0, 0.3), 0 2px 4px -1px rgba(0, 0, 0, 0.2)',
                'glow': '0 0 20px rgba(100, 108, 255, 0.4), 0 0 40px rgba(100, 108, 255, 0.2)',
            },
            container: {
                center: true,
                padding: '1.25rem',
                screens: {
                    'sm': '640px',
                    'md': '768px',
                    'lg': '1024px',
                    'xl': '1200px',
                    '2xl': '1200px',
                },
            },
        }
    },
    plugins: [],
}
