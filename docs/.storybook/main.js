import {dirname, resolve} from 'node:path';
import {fileURLToPath} from 'node:url';
import {mergeConfig} from 'vite';
import vue from '@vitejs/plugin-vue';

const __dirname = dirname(fileURLToPath(import.meta.url));

export default {
    core: {builder: '@storybook/builder-vite'},
    framework: {name: '@storybook/vue3-vite'},
    stories: ['../stories/**/*.stories.@(js|ts|mdx)'],
    addons: [
        '@storybook/addon-docs',
        '@storybook/addon-a11y',
        '@storybook/addon-onboarding',
        '@storybook/addon-vitest'
    ],
    async viteFinal(config) {
        return mergeConfig(config, {
            plugins: [vue()],
            resolve: {
                alias: {
                    '@': resolve(__dirname, '../src'),
                    '@data': resolve(__dirname, '../data')
                },
                extensions: ['.mjs', '.js', '.ts', '.jsx', '.tsx', '.json', '.vue']
            }
        });
    }
};
