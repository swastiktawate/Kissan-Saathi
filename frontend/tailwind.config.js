/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        canvas: '#F7F5F0',
        textMain: 'rgb(28 25 23)', // stone-900
        accent: 'rgb(191 219 254)', // blue-200
      }
    },
  },
  plugins: [],
}
