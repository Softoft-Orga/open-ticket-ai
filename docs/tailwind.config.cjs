// tailwind.config.cjs
module.exports = {
    content: [
        './src/**/*.{astro,js,ts,jsx,tsx,md,mdx}',
        './src/content/docs/**/*.{md,mdx}',
        './stories/**/*.{js,ts,jsx,tsx}',
    ],
    darkMode: 'class',
    theme: {
        extend: {
            colors: {
                "primary": "#a60df2",
                "primary-dark": "#7b09b5",
                "primary-light": "#d475fd",
                "background-dark": "#0f0814",
                "surface-dark": "#1d1023",
                "surface-lighter": "#2d1b36",
                "border-dark": "#3c2249",
                "text-dim": "#b790cb",
                "cyan-glow": "#00f0ff",
            },
            fontFamily: {
                "display": ["Space Grotesk", "sans-serif"],
                "body": ["Noto Sans", "sans-serif"],
            },
            backgroundImage: {
                'cyber-gradient': 'linear-gradient(135deg, rgba(166,13,242,0.1) 0%, rgba(28,16,34,0) 100%)',
                'glow-radial': 'radial-gradient(circle at center, rgba(166,13,242,0.15) 0%, rgba(15,8,20,0) 70%)',
            }
        }
    },
    plugins: [],
}
