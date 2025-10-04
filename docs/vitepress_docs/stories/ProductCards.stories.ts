import ProductCards from '../.vitepress/components/product/ProductCards.vue'
import type {Meta, StoryObj} from '@storybook/vue3'

const meta: Meta<typeof ProductCards> = {
    title: 'Components/ProductCards',
    component: ProductCards,
}
export default meta

type Story = StoryObj<typeof meta>

const sampleProducts = [
    {
        name: 'Basic',
        price: 10,
        description: 'Basic plan',
        features: [{text: 'Feature 1', icon: '⭐'}]
    },
    {
        name: 'Pro',
        price: 20,
        description: 'Pro plan',
        features: [{text: 'Feature 2', icon: '🚀'}],
        featured: true
    }
]

export const Default: Story = {
    render: (args) => ({
        components: {ProductCards},
        setup() {
            return {args}
        },
        template: '<ProductCards v-bind="args" />'
    }),
    args: {
        products: sampleProducts,
        title: 'Our Plans'
    }
}
