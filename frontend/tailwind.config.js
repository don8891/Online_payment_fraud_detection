/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        navy: {
          50: '#f8fafc',
          100: '#f1f5f9',
          200: '#e2e8f0',
          300: '#cbd5e1',
          400: '#94a3b8',
          500: '#64748b',
          600: '#475569',
          700: '#334155',
          750: '#1e293b',
          800: '#0f172a', // Deep Navy
          900: '#090d16',
        },
        risk: {
          low: '#10b981', // Emerald
          medium: '#f59e0b', // Amber
          high: '#ef4444', // Red
          fraud: '#ef4444',
          safe: '#10b981',
          info: '#3b82f6', // Blue
        }
      },
      fontFamily: {
        sans: ['Inter', 'sans-serif'],
      }
    },
  },
  plugins: [],
}
