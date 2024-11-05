/** @type {import('tailwindcss').Config} */
module.exports = {
  content: ["./views/**/*.{html,js,ejs}"],
  theme: {
    extend: {
      keyframes: {
        animation: {
          blob: "blob 3s infinite",
        },
        blob: {
          "0%, 100%": {
            transform: "scale(1)",
          },
          "50%": {
            transform: "scale(1.4)",
          },

          "66%": {
            transform: "scale(1.2)",
          },
          "100%": {
            transform: "scale(1)",
          },
        },
      },

    },
  },
  plugins: [],
}

