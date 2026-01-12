// @ts-check
import eslint from '@eslint/js';
import tseslint from 'typescript-eslint';
import pluginVue from 'eslint-plugin-vue';
import pluginAstro from 'eslint-plugin-astro';
import globals from 'globals';

export default [
  {
    ignores: [
      '**/node_modules/**',
      '**/dist/**',
      '**/.astro/**',
      '**/storybook-static/**',
      '**/coverage/**',
      '**/.storybook/cache/**',
      '**/build/**',
      '**/.vitepress/dist/**',
      '**/.vitepress/cache/**',
      '**/public/**',
      '**/open-ticket-ai-platform-prototype/**',
    ],
  },

  eslint.configs.recommended,
  
  ...tseslint.configs.recommended.map(config => ({
    ...config,
    files: ['**/*.ts', '**/*.mts', '**/*.tsx', '**/*.vue'],
  })),
  
  ...pluginVue.configs['flat/recommended'],
  ...pluginAstro.configs.recommended,

  {
    files: ['**/*.vue'],
    languageOptions: {
      parserOptions: {
        parser: tseslint.parser,
        ecmaVersion: 'latest',
        sourceType: 'module',
      },
    },
    rules: {
      'vue/multi-word-component-names': 'off',
    },
  },

  {
    files: ['**/*.js', '**/*.mjs', '**/*.ts', '**/*.vue', '**/*.astro'],
    languageOptions: {
      ecmaVersion: 'latest',
      sourceType: 'module',
      globals: {
        ...globals.browser,
      },
    },
  },

  {
    files: ['**/*.cjs'],
    languageOptions: {
      ecmaVersion: 'latest',
      sourceType: 'commonjs',
      globals: {
        ...globals.node,
      },
    },
  },
];
