import MarketplaceSkeletonCard from '../src/components/vue/marketplace/MarketplaceSkeletonCard.vue'
import type {Meta, StoryObj} from '@storybook/vue3'

const meta: Meta<typeof MarketplaceSkeletonCard> = {
    title: 'Marketplace/MarketplaceSkeletonCard',
    component: MarketplaceSkeletonCard,
    parameters: {
        docs: {
            description: {
                component: 'Skeleton loading state for plugin cards in the marketplace. Shows animated placeholders while data is being fetched.'
            }
        }
    }
}
export default meta

type Story = StoryObj<typeof meta>

export const Default: Story = {
    render: (args) => ({
        components: {MarketplaceSkeletonCard},
        setup() {
            return {args}
        },
        template: '<div class="max-w-md bg-slate-950 p-4"><MarketplaceSkeletonCard v-bind="args" /></div>'
    }),
    parameters: {
        backgrounds: { default: 'dark' }
    }
}

export const MultipleCards: Story = {
    render: (args) => ({
        components: {MarketplaceSkeletonCard},
        setup() {
            return {args}
        },
        template: `
            <div class="bg-slate-950 p-4">
                <div class="grid gap-4 md:grid-cols-2 xl:grid-cols-3">
                    <MarketplaceSkeletonCard v-for="n in 6" :key="n" />
                </div>
            </div>
        `
    }),
    parameters: {
        backgrounds: { default: 'dark' }
    }
}
