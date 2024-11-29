/** @type {import('tailwindcss').Config} */
module.exports = {
    content: ["./templates/**/*.{html,js}", "app.py"],
    theme: {
        extend: {
            // class="animate-fadeOut"
            animation: {
                fadeOut: 'fadeOut 2s ease-in-out forwards',
            },
            keyframes: {
                fadeOut: {
                    '0%': {opacity: 1},
                    '100%': {opacity: 0},
                },
            },
        },
    },
    plugins: [require("daisyui")],
}