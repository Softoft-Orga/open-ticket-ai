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
                'primary': '#a60df2',
                'primary-dark': '#7b09b5',
                'primary-light': '#d475fd',
                'link': '#646cff',
                'link-hover': '#747bff',
                'background-dark': '#0f0814',
                'surface-dark': '#1d1023',
                'surface-lighter': '#2d1b36',
                'border-dark': '#3c2249',
                'text-dim': '#b790cb',
                'cyan-glow': '#00f0ff',
            },
            backgroundImage: {
                'cyber-gradient': 'linear-gradient(135deg, rgba(166,13,242,0.1) 0%, rgba(28,16,34,0) 100%)',
                'glow-radial': 'radial-gradient(circle at center, rgba(166,13,242,0.15) 0%, rgba(15,8,20,0) 70%)',
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
    plugins: [
        require('@tailwindcss/typography'),
    ],
}
