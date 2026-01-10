import MarketplacePagination from '../src/components/vue/marketplace/MarketplacePagination.vue'
import type {Meta, StoryObj} from '@storybook/vue3'

const meta: Meta<typeof MarketplacePagination> = {
    title: 'Marketplace/MarketplacePagination',
    component: MarketplacePagination,
    argTypes: {
        page: {
            control: { type: 'number', min: 1 },
            description: 'Current page number'
        },
        totalPages: {
            control: { type: 'number', min: 1 },
            description: 'Total number of pages'
        },
        hasMoreResults: {
            control: 'boolean',
            description: 'Whether there are more results available'
        },
        isLoading: {
            control: 'boolean',
            description: 'Loading state'
        }
    },
    parameters: {
        docs: {
            description: {
                component: 'Pagination component for navigating through marketplace results. Emits prev and next events.'
            }
        }
    }
}
export default meta

type Story = StoryObj<typeof meta>

export const FirstPage: Story = {
    render: (args) => ({
        components: {MarketplacePagination},
        setup() {
            const handlePrev = () => console.log('Previous clicked')
            const handleNext = () => console.log('Next clicked')
            return {args, handlePrev, handleNext}
        },
        template: '<div class="bg-background-dark p-4"><MarketplacePagination v-bind="args" @prev="handlePrev" @next="handleNext" /></div>'
    }),
    args: {
        page: 1,
        totalPages: 10,
        hasMoreResults: true,
        isLoading: false
    },
    parameters: {
        backgrounds: { default: 'dark' }
    }
}

export const MiddlePage: Story = {
    render: (args) => ({
        components: {MarketplacePagination},
        setup() {
            const handlePrev = () => console.log('Previous clicked')
            const handleNext = () => console.log('Next clicked')
            return {args, handlePrev, handleNext}
        },
        template: '<div class="bg-background-dark p-4"><MarketplacePagination v-bind="args" @prev="handlePrev" @next="handleNext" /></div>'
    }),
    args: {
        page: 5,
        totalPages: 10,
        hasMoreResults: true,
        isLoading: false
    },
    parameters: {
        backgrounds: { default: 'dark' }
    }
}

export const LastPage: Story = {
    render: (args) => ({
        components: {MarketplacePagination},
        setup() {
            const handlePrev = () => console.log('Previous clicked')
            const handleNext = () => console.log('Next clicked')
            return {args, handlePrev, handleNext}
        },
        template: '<div class="bg-background-dark p-4"><MarketplacePagination v-bind="args" @prev="handlePrev" @next="handleNext" /></div>'
    }),
    args: {
        page: 10,
        totalPages: 10,
        hasMoreResults: false,
        isLoading: false
    },
    parameters: {
        backgrounds: { default: 'dark' }
    }
}

export const Loading: Story = {
    render: (args) => ({
        components: {MarketplacePagination},
        setup() {
            const handlePrev = () => console.log('Previous clicked')
            const handleNext = () => console.log('Next clicked')
            return {args, handlePrev, handleNext}
        },
        template: '<div class="bg-background-dark p-4"><MarketplacePagination v-bind="args" @prev="handlePrev" @next="handleNext" /></div>'
    }),
    args: {
        page: 3,
        totalPages: 10,
        hasMoreResults: true,
        isLoading: true
    },
    parameters: {
        backgrounds: { default: 'dark' }
    }
}
