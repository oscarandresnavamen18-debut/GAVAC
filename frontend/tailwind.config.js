/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./*.html",
    "./src/**/*.{html,ts}",
    "./src/modules/**/*.{html,ts}"
  ],
  theme: {
    extend: {
      fontFamily: {
        'jakarta': ['"Plus Jakarta Sans"', 'sans-serif'],
      },
      colors: {
        'gavac-primary': '#1A3A32',
        'gavac-bg': '#F7F9F7',
        'gavac-accent': '#2E5A4D',
        'gavac-light': '#E8F1EC',
        'gavac-green': '#1c4d33',
        'gavac-dark': '#0f3324',
      },
      borderRadius: {
        '4xl': '2rem',
        '5xl': '2.5rem',
      }
    },
  },
  plugins: [],
}
