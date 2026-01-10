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
                'secondary': '#1fd5ff',
                'secondary-light': '#63e3ff',
                'secondary-dark': '#0f8ec7',
                'info': '#3cc8ff',
                'info-faint': '#133047',
                'success': '#16dba0',
                'success-dark': '#0f9c73',
                'warning': '#f7b733',
                'warning-dark': '#c47f00',
                'danger': '#ff4f6d',
                'danger-dark': '#c5304b',
                'muted': '#6f5a7c'
            },
            backgroundImage: {
                'cyber-gradient': 'linear-gradient(135deg, rgba(166,13,242,0.1) 0%, rgba(28,16,34,0) 100%)',
                'glow-radial': 'radial-gradient(circle at center, rgba(166,13,242,0.15) 0%, rgba(15,8,20,0) 70%)',
                'glass-gradient': 'linear-gradient(180deg, rgba(255, 255, 255, 0.04) 0%, rgba(255, 255, 255, 0.02) 100%)'
            },
            borderRadius: {
                'xl': '1rem',
                '2xl': '1.5rem',
                '3xl': '2rem',
            },
            boxShadow: {
                'card': '0 4px 6px -1px rgba(0, 0, 0, 0.3), 0 2px 4px -1px rgba(0, 0, 0, 0.2)',
                'glow': '0 0 20px rgba(100, 108, 255, 0.4), 0 0 40px rgba(100, 108, 255, 0.2)',
                'neon-cyan': '0 0 20px rgba(31, 213, 255, 0.35), 0 0 40px rgba(31, 213, 255, 0.2)'
            },
            maxWidth: {
                'content': '1200px',
                'copy': '780px'
            },
            spacing: {
                'section': '4.5rem'
            },
            scale: {
                '102': '1.02',
            }
        }
    },
    plugins: [
        require('@tailwindcss/typography'),
    ],
}
