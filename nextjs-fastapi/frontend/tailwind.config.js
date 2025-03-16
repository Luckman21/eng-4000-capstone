
import { heroui } from "@heroui/react";

/** @type {import('tailwindcss').Config} */
export const content = [
  "./node_modules/@heroui/theme/dist/**/*.{js,ts,jsx,tsx}",
];
export const theme = {
  extend: {
    colors: {
      primary: {
        DEFAULT: "#ffbd00", // your new primary color (e.g., Tailwind's blue-700)
      },
    },
  },
};

export const darkMode = "class";
export const plugins = [heroui()];