import LatestNews from '../src/components/vue/news/LatestNews.vue'
import type {Meta, StoryObj} from '@storybook/vue3'

const meta: Meta<typeof LatestNews> = {
    title: 'Components/LatestNews',
    component: LatestNews,
    parameters: {
        docs: {
            description: {
                component: 'Displays a grid of latest news articles with images, dates, titles, and descriptions. Fetches data from the useNewsArticles composable.'
            }
        }
    }
}
export default meta

type Story = StoryObj<typeof meta>

export const Default: Story = {
    render: (args) => ({
        components: {LatestNews},
        setup() {
            return {args}
        },
        template: '<LatestNews v-bind="args" />'
    })
}

export const DarkMode: Story = {
    render: (args) => ({
        components: {LatestNews},
        setup() {
            return {args}
        },
        template: '<div class="bg-slate-950 p-8 rounded"><LatestNews v-bind="args" /></div>'
    }),
    parameters: {
        backgrounds: { default: 'dark' }
    }
}
