import type { Config } from "tailwindcss";

const config: Config = {
  content: [
    "./src/pages/**/*.{js,ts,jsx,tsx,mdx}",
    "./src/components/**/*.{js,ts,jsx,tsx,mdx}",
    "./src/app/**/*.{js,ts,jsx,tsx,mdx}",
  ],
  theme: {
    extend: {
      colors: {
        background: "var(--background)",
        foreground: "var(--foreground)",
      },
      fontSize: {
        sm: '0.800rem',
        base: '1rem',
        xl: '1.250rem',
        '2xl': '1.563rem',
        '3xl': '1.954rem',
        '4xl': '2.442rem',
        '5xl': '3.053rem',
      },
      fontFamily: {
        heading: 'Figtree',
        body: 'Figtree',
      },
      fontWeight: {
        normal: '400',
        bold: '700',
      },
    },
  },
  plugins: [],
};
export default config;
