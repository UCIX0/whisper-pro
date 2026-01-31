module.exports = {
    content: [
        "./index.html",
        "./src/**/*.{js,ts,jsx,tsx}",
    ],
    theme: {
        extend: {
            colors: {
                // Dark modern palette
                background: "#0a0a0a",
                surface: "#1a1a1a",
                primary: "#6d28d9", // Deep purple
                accent: "#d946ef", // Fuchsia
                success: "#22c55e",
                text: "#e5e5e5",
                subtext: "#a3a3a3"
            },
            fontFamily: {
                sans: ['Inter', 'sans-serif'],
            },
            animation: {
                'glow': 'glow 2s ease-in-out infinite alternate',
            },
            keyframes: {
                glow: {
                    '0%': { boxShadow: '0 0 10px #6d28d9' },
                    '100%': { boxShadow: '0 0 20px #d946ef' }
                }
            }
        },
    },
    plugins: [],
}
