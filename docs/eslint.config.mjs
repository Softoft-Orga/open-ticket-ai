// @ts-check
import eslint from '@eslint/js';
import tseslint from 'typescript-eslint';
import pluginVue from 'eslint-plugin-vue';
import pluginAstro from 'eslint-plugin-astro';
import globals from 'globals';
import prettierConfig from 'eslint-config-prettier';

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
    files: ['**/*.ts', '**/*.mts', '**/*.tsx'],
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
    files: ['src/components/vue/domain/**/*.vue', 'src/**/*.astro'],
    rules: {
      'vue/no-restricted-syntax': [
        'error',
        {
          selector: 'VElement[rawName="button"]',
          message:
            'Use the Button component from vue/core/basic/Button.vue instead of native <button> elements in domain components and Astro pages.',
        },
      ],
    },
  },

  {
    files: [
      'src/components/vue/core/basic/Button.vue',
      'src/components/vue/core/basic/Tabs.vue',
      'src/components/vue/core/navigation/NavBar.vue',
    ],
    rules: {
      'vue/no-restricted-syntax': 'off',
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

  // Must be last to override formatting rules from other configs
  prettierConfig,
];
