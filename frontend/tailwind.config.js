/** @type {import('tailwindcss').Config} */
export default {
  content: ['./index.html', './src/**/*.{js,jsx}'],
  theme: {
    extend: {
      colors: {
        appBg: '#0B0F1A',
        cardBg: '#121826',
        accent: '#3B82F6'
      },
      boxShadow: {
        glass: '0 10px 30px rgba(0, 0, 0, 0.35)'
      },
      backgroundImage: {
        glow: 'radial-gradient(circle at top right, rgba(59,130,246,0.28), transparent 45%), radial-gradient(circle at bottom left, rgba(59,130,246,0.12), transparent 40%)'
      }
    }
  },
  plugins: []
};
