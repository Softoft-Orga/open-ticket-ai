import ProductCard from '../src/components/vue/product/ProductCard.vue'
import type {Meta, StoryObj} from '@storybook/vue3'
import type {Product} from '../src/components/vue/product/product.types'

const meta: Meta<typeof ProductCard> = {
    title: 'Product/ProductCard',
    component: ProductCard,
    argTypes: {
        product: {
            control: 'object',
            description: 'Product data including name, price, description, and features'
        }
    },
    parameters: {
        docs: {
            description: {
                component: 'Product card displaying product information with expandable features list. Shows first 5 features by default, with remaining features in an accordion.'
            }
        }
    }
}
export default meta

type Story = StoryObj<typeof meta>

const basicProduct: Product = {
    name: 'Basic Plan',
    price: 29,
    pricePeriod: 'month',
    description: 'Perfect for small teams getting started with AI-powered ticket classification.',
    features: [
        { text: 'Up to 1,000 tickets/month', icon: 'fa-ticket' },
        { text: 'Basic AI classification', icon: 'fa-brain' },
        { text: 'Email support', icon: 'fa-envelope' },
        { text: '7-day retention', icon: 'fa-clock' }
    ]
}

const professionalProduct: Product = {
    name: 'Professional',
    price: 99,
    pricePeriod: 'month',
    description: 'For growing teams that need more power and flexibility in ticket management.',
    features: [
        { text: 'Up to 10,000 tickets/month', icon: 'fa-ticket' },
        { text: 'Advanced AI models', icon: 'fa-brain' },
        { text: 'Priority support', icon: 'fa-headset' },
        { text: '30-day retention', icon: 'fa-clock' },
        { text: 'Custom categories', icon: 'fa-tags' },
        { text: 'API access', icon: 'fa-code' },
        { text: 'Webhook integration', icon: 'fa-link' },
        { text: 'Analytics dashboard', icon: 'fa-chart-line' }
    ]
}

const enterpriseProduct: Product = {
    name: 'Enterprise',
    price: 499,
    pricePeriod: 'month',
    description: 'Complete solution for large organizations with advanced requirements and dedicated support.',
    features: [
        { text: 'Unlimited tickets', icon: 'fa-infinity' },
        { text: 'Custom AI training', icon: 'fa-brain' },
        { text: '24/7 dedicated support', icon: 'fa-phone' },
        { text: 'Unlimited retention', icon: 'fa-database' },
        { text: 'Custom integrations', icon: 'fa-puzzle-piece' },
        { text: 'Advanced security', icon: 'fa-shield-alt' },
        { text: 'SLA guarantees', icon: 'fa-file-contract' },
        { text: 'Multi-language support', icon: 'fa-language' },
        { text: 'White-labeling', icon: 'fa-tag' },
        { text: 'Dedicated account manager', icon: 'fa-user-tie' }
    ]
}

export const Basic: Story = {
    render: (args) => ({
        components: {ProductCard},
        setup() {
            return {args}
        },
        template: '<div class="max-w-sm bg-gray-950 p-4"><ProductCard v-bind="args" /></div>'
    }),
    args: {
        product: basicProduct
    },
    parameters: {
        backgrounds: { default: 'dark' }
    }
}

export const Professional: Story = {
    render: (args) => ({
        components: {ProductCard},
        setup() {
            return {args}
        },
        template: '<div class="max-w-sm bg-gray-950 p-4"><ProductCard v-bind="args" /></div>'
    }),
    args: {
        product: professionalProduct
    },
    parameters: {
        backgrounds: { default: 'dark' }
    }
}

export const Enterprise: Story = {
    render: (args) => ({
        components: {ProductCard},
        setup() {
            return {args}
        },
        template: '<div class="max-w-sm bg-gray-950 p-4"><ProductCard v-bind="args" /></div>'
    }),
    args: {
        product: enterpriseProduct
    },
    parameters: {
        backgrounds: { default: 'dark' }
    }
}

export const Comparison: Story = {
    render: () => ({
        components: {ProductCard},
        setup() {
            return {
                basic: basicProduct,
                professional: professionalProduct,
                enterprise: enterpriseProduct
            }
        },
        template: `
            <div class="bg-gray-950 p-8">
                <div class="grid gap-6 md:grid-cols-2 lg:grid-cols-3">
                    <ProductCard :product="basic" />
                    <ProductCard :product="professional" />
                    <ProductCard :product="enterprise" />
                </div>
            </div>
        `
    }),
    parameters: {
        backgrounds: { default: 'dark' }
    }
}
