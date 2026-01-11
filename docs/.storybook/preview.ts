import type {Preview} from '@storybook/vue3-vite';

const preview: Preview = {
    parameters: {
        controls: {
            matchers: {
                color: /(background|color)$/i,
                date: /Date$/i,
            },
        },
        a11y: {
            config: {
                rules: [],
            },
        },
    },
    tags: ['autodocs'],
};

export default preview;
