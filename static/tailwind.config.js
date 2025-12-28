module.exports = {
  content: [
    "../src/**/templates/**/*.html",
    "../src/**/*.py",
    "./node_modules/flowbite/**/*.js",
  ],
  theme: {
    extend: {},
  },
  plugins: [require("flowbite/plugin")],
};
