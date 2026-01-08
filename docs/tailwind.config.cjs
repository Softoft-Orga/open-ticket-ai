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
                'primary': '#646cff',
                'background-dark': '#0a0e1a',
                'surface-dark': '#1a0f20',
                'border-dark': '#3c2249',
            },
            backgroundImage: {
                'glow-radial': 'radial-gradient(circle at center, rgba(100, 108, 255, 0.15) 0%, rgba(10, 14, 26, 0) 70%)',
            },
            fontFamily: {
                'display': ['Space Grotesk', 'system-ui', 'sans-serif'],
            }
        }
    },
    plugins: [],
}
