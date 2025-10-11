// .storybook/main.js
const path = require('path');
const {mergeConfig} = require('vite');
const vue = require('@vitejs/plugin-vue');

module.exports = {
    core: {builder: '@storybook/builder-vite'},
    framework: '@storybook/vue3-vite',
    stories: ['../stories/**/*.stories.@(js|ts|mdx)'],
    async viteFinal(config) {
        return mergeConfig(config, {
            plugins: [vue()],
            resolve: {
                alias: {'@': path.resolve(__dirname, '../src')}
            }
        });
    },
};
