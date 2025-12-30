/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./src/**/*.{js,jsx,ts,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        primary: {
          900: '#0A2540',
          700: '#1E4A7A',
          500: '#3B82F6',
          300: '#93C5FD',
          50: '#EFF6FF',
        },
        verdict: {
          true: '#059669',
          mostly_true: '#84CC16',
          mixed: '#F59E0B',
          mostly_false: '#F97316',
          false: '#DC2626',
          unverifiable: '#6B7280',
        },
      },
      fontFamily: {
        heading: ['Space Grotesk', 'sans-serif'],
        body: ['IBM Plex Sans', 'sans-serif'],
        mono: ['IBM Plex Mono', 'monospace'],
      },
      spacing: {
        'xs': '4px',
        'sm': '8px',
        'md': '16px',
        'lg': '24px',
        'xl': '32px',
        '2xl': '48px',
        '3xl': '64px',
      },
      borderRadius: {
        'sm': '4px',
        'md': '8px',
        'lg': '12px',
        'xl': '16px',
      },
      boxShadow: {
        'sm': '0 1px 2px rgba(0,0,0,0.05)',
        'md': '0 1px 3px rgba(0,0,0,0.1)',
        'lg': '0 4px 6px rgba(0,0,0,0.1)',
        'xl': '0 10px 15px rgba(0,0,0,0.1)',
        'hover': '0 4px 12px rgba(0,0,0,0.15)',
      },
      transitionDuration: {
        'fast': '150ms',
        'normal': '200ms',
        'slow': '300ms',
      },
    },
  },
  plugins: [],
}
