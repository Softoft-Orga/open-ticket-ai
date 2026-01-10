import type {Preview} from '@storybook/vue3-vite';
import '../src/styles/global.css';

const preview: Preview = {
    parameters: {
        controls: {
            matchers: {
                color: /(background|color)$/i,
                date: /Date$/i,
            },
        },
        a11y: {
            test: 'todo',
        },
        docs: {
            autodocs: 'tag',
        },
    },
    tags: ['autodocs'],
};

export default preview;
