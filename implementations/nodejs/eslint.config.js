export default [
  {
    files: ["src/**/*.js", "tests/**/*.js", "bin/**/*.js"],
    languageOptions: {
      ecmaVersion: 2022,
      sourceType: "module",
    },
    rules: {
      "max-len": ["error", { "code": 100 }],
    },
  },
]; 