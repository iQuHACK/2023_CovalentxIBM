/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./src/**/*.{js,ts,jsx,tsx}"
  ],
  theme: {
    extend: {
      fontFamily: {
        'bitcount': ['bitcount-prop-single-circle', 'sans-serif']
      }
    },
  },
  plugins: [],
}
