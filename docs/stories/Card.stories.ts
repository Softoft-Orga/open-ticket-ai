import Card from '../src/components/vue/core/basic/Card.vue'
import Badge from '../src/components/vue/core/basic/Badge.vue'
import type {Meta, StoryObj} from '@storybook/vue3'
import { VARIANTS } from '../src/components/vue/core/design-system/tokens'

const meta: Meta<typeof Card> = {
    title: 'Core/Card',
    component: Card,
    tags: ['autodocs'],
    argTypes: {
        background: {
            control: 'select',
            options: ['default', 'surface-dark', 'surface-lighter', 'primary', 'gradient', 'transparent', 'custom'],
            description: 'Background color variant',
        },
        padding: {
            control: 'select',
            options: ['none', 'sm', 'default', 'lg'],
            description: 'Padding size',
        },
        hoverable: {
            control: 'boolean',
            description: 'Whether to add hover effect',
        },
        customBg: {
            control: 'text',
            description: 'Custom background class when background is "custom"',
        },
        variant: {
            control: 'select',
            options: VARIANTS,
            description: 'Design system variant (primary, secondary, outline, ghost) - overrides background when set',
        },
    },
    parameters: {
        docs: {
            description: {
                component: 'Flexible card component with multiple slots (image, header, title, default, actions, footer) and customizable background colors. Supports hover effects and various padding options. Can use design system variants for consistent styling.'
            }
        }
    }
}
export default meta

type Story = StoryObj<typeof meta>

export const Default: Story = {
    args: {
        background: 'default',
        padding: 'default',
    },
    render: (args) => ({
        components: {Card},
        setup() {
            return {args}
        },
        template: '<Card v-bind="args">Simple card content without header or footer.</Card>'
    }),
}

export const WithTitle: Story = {
    args: {
        background: 'default',
        padding: 'default',
    },
    render: (args) => ({
        components: {Card},
        setup() {
            return {args}
        },
        template: `
            <Card v-bind="args">
                <template #title>
                    Card Title
                </template>
                <p>Main card content goes here with a title section above.</p>
            </Card>
        `
    }),
}

export const WithHeader: Story = {
    args: {
        background: 'default',
        padding: 'default',
    },
    render: (args) => ({
        components: {Card},
        setup() {
            return {args}
        },
        template: `
            <Card v-bind="args">
                <template #header>
                    <h3 class="text-lg font-bold">Card Header</h3>
                </template>
                <p>Main card content goes here with a custom header section above.</p>
            </Card>
        `
    }),
}

export const WithImage: Story = {
    args: {
        background: 'default',
        padding: 'default',
    },
    render: (args) => ({
        components: {Card},
        setup() {
            return {args}
        },
        template: `
            <Card v-bind="args">
                <template #image>
                    <div class="h-48 bg-gradient-to-r from-primary to-cyan-glow flex items-center justify-center">
                        <span class="text-2xl font-bold text-white">Image Slot</span>
                    </div>
                </template>
                <template #title>
                    Card with Image
                </template>
                <p>This card demonstrates the image slot, perfect for hero images or thumbnails.</p>
            </Card>
        `
    }),
}

export const WithActions: Story = {
    args: {
        background: 'default',
        padding: 'default',
    },
    render: (args) => ({
        components: {Card},
        setup() {
            return {args}
        },
        template: `
            <Card v-bind="args">
                <template #title>
                    Card with Actions
                </template>
                <p>Main card content with action buttons below.</p>
                <template #actions>
                    <div class="flex gap-2">
                        <button class="px-4 py-2 bg-primary text-white rounded-lg hover:bg-primary-dark transition">
                            Primary Action
                        </button>
                        <button class="px-4 py-2 bg-surface-lighter text-white rounded-lg hover:bg-border-dark transition">
                            Secondary
                        </button>
                    </div>
                </template>
            </Card>
        `
    }),
}

export const WithFooter: Story = {
    args: {
        background: 'default',
        padding: 'default',
    },
    render: (args) => ({
        components: {Card},
        setup() {
            return {args}
        },
        template: `
            <Card v-bind="args">
                <p>Main card content with information in the footer.</p>
                <template #footer>
                    <div class="text-sm text-text-dim">Last updated: 2 hours ago</div>
                </template>
            </Card>
        `
    }),
}

export const FullSlots: Story = {
    args: {
        background: 'default',
        padding: 'default',
    },
    render: (args) => ({
        components: {Card},
        setup() {
            return {args}
        },
        template: `
            <Card v-bind="args">
                <template #image>
                    <div class="h-40 bg-gradient-to-br from-primary via-primary-dark to-surface-dark flex items-center justify-center">
                        <span class="text-xl font-bold text-white">Feature Image</span>
                    </div>
                </template>
                <template #header>
                    <div class="flex items-center justify-between">
                        <h3 class="text-sm font-semibold text-text-dim uppercase tracking-wide">Category</h3>
                        <span class="text-xs text-text-dim">New</span>
                    </div>
                </template>
                <template #title>
                    Complete Card Example
                </template>
                <p>This card demonstrates all available slots: image, header, title, content, actions, and footer.</p>
                <template #actions>
                    <div class="flex justify-end gap-2">
                        <button class="px-4 py-2 bg-surface-lighter text-white rounded hover:bg-border-dark transition">
                            Cancel
                        </button>
                        <button class="px-4 py-2 bg-primary text-white rounded hover:bg-primary-dark transition">
                            Confirm
                        </button>
                    </div>
                </template>
                <template #footer>
                    <div class="flex justify-between items-center text-xs">
                        <span>Created: Jan 10, 2026</span>
                        <span>Modified: 5 mins ago</span>
                    </div>
                </template>
            </Card>
        `
    }),
}

// Background Variants
export const BackgroundDefault: Story = {
    args: {
        background: 'default',
        padding: 'default',
    },
    render: (args) => ({
        components: {Card},
        setup() {
            return {args}
        },
        template: `
            <Card v-bind="args">
                <template #title>Default Background</template>
                <p>Uses the default surface-dark background color.</p>
            </Card>
        `
    }),
}

export const BackgroundLighter: Story = {
    args: {
        background: 'surface-lighter',
        padding: 'default',
    },
    render: (args) => ({
        components: {Card},
        setup() {
            return {args}
        },
        template: `
            <Card v-bind="args">
                <template #title>Lighter Background</template>
                <p>Uses the surface-lighter background color for subtle contrast.</p>
            </Card>
        `
    }),
}

export const BackgroundPrimary: Story = {
    args: {
        background: 'primary',
        padding: 'default',
    },
    render: (args) => ({
        components: {Card},
        setup() {
            return {args}
        },
        template: `
            <Card v-bind="args">
                <template #title>Primary Tint</template>
                <p>Uses a subtle primary color tint (10% opacity) for emphasis.</p>
            </Card>
        `
    }),
}

export const BackgroundGradient: Story = {
    args: {
        background: 'gradient',
        padding: 'default',
    },
    render: (args) => ({
        components: {Card},
        setup() {
            return {args}
        },
        template: `
            <Card v-bind="args">
                <template #title>Gradient Background</template>
                <p>Uses the cyber-gradient background for a premium feel.</p>
            </Card>
        `
    }),
}

export const BackgroundTransparent: Story = {
    args: {
        background: 'transparent',
        padding: 'default',
    },
    render: (args) => ({
        components: {Card},
        setup() {
            return {args}
        },
        template: `
            <div class="bg-surface-lighter p-4">
                <Card v-bind="args">
                    <template #title>Transparent Background</template>
                    <p>Transparent background - useful for layering or custom designs.</p>
                </Card>
            </div>
        `
    }),
}

export const BackgroundCustom: Story = {
    args: {
        background: 'custom',
        customBg: 'bg-gradient-to-r from-purple-900/50 to-blue-900/50',
        padding: 'default',
    },
    render: (args) => ({
        components: {Card},
        setup() {
            return {args}
        },
        template: `
            <Card v-bind="args">
                <template #title>Custom Background</template>
                <p>Uses a custom Tailwind class for complete control over the background.</p>
            </Card>
        `
    }),
}

// Padding Variants
export const PaddingNone: Story = {
    args: {
        background: 'default',
        padding: 'none',
    },
    render: (args) => ({
        components: {Card},
        setup() {
            return {args}
        },
        template: `
            <Card v-bind="args">
                <template #title>No Padding</template>
                <p>Card with no padding - useful for full-bleed content like images.</p>
            </Card>
        `
    }),
}

export const PaddingSmall: Story = {
    args: {
        background: 'default',
        padding: 'sm',
    },
    render: (args) => ({
        components: {Card},
        setup() {
            return {args}
        },
        template: `
            <Card v-bind="args">
                <template #title>Small Padding</template>
                <p>Compact card with reduced padding.</p>
            </Card>
        `
    }),
}

export const PaddingLarge: Story = {
    args: {
        background: 'default',
        padding: 'lg',
    },
    render: (args) => ({
        components: {Card},
        setup() {
            return {args}
        },
        template: `
            <Card v-bind="args">
                <template #title>Large Padding</template>
                <p>Spacious card with extra padding for emphasis.</p>
            </Card>
        `
    }),
}

// Interactive
export const Hoverable: Story = {
    args: {
        background: 'default',
        padding: 'default',
        hoverable: true,
    },
    render: (args) => ({
        components: {Card},
        setup() {
            return {args}
        },
        template: `
            <Card v-bind="args">
                <template #title>Hoverable Card</template>
                <p>Hover over this card to see the glow effect and border color change.</p>
            </Card>
        `
    }),
}

// Complex Examples
export const WithRichContent: Story = {
    args: {
        background: 'default',
        padding: 'default',
    },
    render: (args) => ({
        components: {Card, Badge},
        setup() {
            return {args}
        },
        template: `
            <Card v-bind="args">
                <template #header>
                    <div class="flex items-center justify-between">
                        <h3 class="text-lg font-bold">AI Classification Result</h3>
                        <Badge type="success">Completed</Badge>
                    </div>
                </template>
                <div class="space-y-2">
                    <p><strong>Category:</strong> Technical Support</p>
                    <p><strong>Confidence:</strong> 94.5%</p>
                    <p><strong>Processing Time:</strong> 120ms</p>
                    <p class="text-sm text-gray-400">Ticket classified using AI model v2.1.0</p>
                </div>
                <template #footer>
                    <div class="flex justify-between items-center">
                        <span class="text-xs text-gray-500">Processed: 2024-01-15 10:30:00</span>
                        <button class="text-primary hover:text-primary-light text-sm transition">View Details</button>
                    </div>
                </template>
            </Card>
        `
    }),
}

export const ProductCard: Story = {
    args: {
        background: 'surface-lighter',
        padding: 'none',
        hoverable: true,
    },
    render: (args) => ({
        components: {Card, Badge},
        setup() {
            return {args}
        },
        template: `
            <Card v-bind="args">
                <template #image>
                    <div class="h-48 bg-gradient-to-br from-primary to-cyan-glow flex items-center justify-center">
                        <span class="text-3xl">🎯</span>
                    </div>
                </template>
                <template #header>
                    <div class="flex items-center justify-between">
                        <Badge type="info">Featured</Badge>
                        <span class="text-sm text-text-dim">$99/mo</span>
                    </div>
                </template>
                <template #title>
                    Premium AI Classification
                </template>
                <div class="space-y-2">
                    <p class="text-sm">Advanced ticket classification with 99% accuracy.</p>
                    <ul class="text-sm space-y-1 text-text-dim">
                        <li>✓ Unlimited tickets</li>
                        <li>✓ Custom categories</li>
                        <li>✓ Priority support</li>
                    </ul>
                </div>
                <template #actions>
                    <button class="w-full px-4 py-2 bg-primary text-white rounded-lg hover:bg-primary-dark transition">
                        Get Started
                    </button>
                </template>
                <template #footer>
                    <p class="text-xs text-center text-text-dim">30-day money-back guarantee</p>
                </template>
            </Card>
        `
    }),
}

export const Grid: Story = {
    render: () => ({
        components: {Card},
        template: `
            <div class="grid gap-4 md:grid-cols-2 lg:grid-cols-3">
                <Card background="surface-lighter" hoverable>
                    <template #title>
                        <h4 class="font-semibold">Accuracy</h4>
                    </template>
                    <p class="text-3xl font-bold text-green-400">95.2%</p>
                </Card>
                <Card background="surface-lighter" hoverable>
                    <template #title>
                        <h4 class="font-semibold">Tickets Processed</h4>
                    </template>
                    <p class="text-3xl font-bold text-blue-400">12,543</p>
                </Card>
                <Card background="surface-lighter" hoverable>
                    <template #title>
                        <h4 class="font-semibold">Avg Response Time</h4>
                    </template>
                    <p class="text-3xl font-bold text-purple-400">85ms</p>
                </Card>
            </div>
        `
    }),
}

export const Playground: Story = {
    args: {
        background: 'default',
        padding: 'default',
        hoverable: false,
    },
    render: (args) => ({
        components: {Card},
        setup() {
            return {args}
        },
        template: `
            <Card v-bind="args">
                <template #title>
                    Interactive Playground
                </template>
                <p>Use the controls panel to experiment with different card configurations.</p>
                <p class="text-sm text-text-dim mt-2">Try changing the background, padding, and hoverable properties to see how they affect the card appearance.</p>
            </Card>
        `
    }),
}

// Design System Variant Examples
export const VariantPrimary: Story = {
    args: {
        variant: 'primary',
        padding: 'default',
    },
    render: (args) => ({
        components: {Card},
        setup() {
            return {args}
        },
        template: `
            <Card v-bind="args">
                <template #title>Primary Variant</template>
                <p>Uses the primary design system variant with primary/10 background and primary/30 border.</p>
            </Card>
        `
    }),
}

export const VariantSecondary: Story = {
    args: {
        variant: 'secondary',
        padding: 'default',
    },
    render: (args) => ({
        components: {Card},
        setup() {
            return {args}
        },
        template: `
            <Card v-bind="args">
                <template #title>Secondary Variant</template>
                <p>Uses the secondary design system variant with subtle dark background.</p>
            </Card>
        `
    }),
}

export const VariantOutline: Story = {
    args: {
        variant: 'outline',
        padding: 'default',
    },
    render: (args) => ({
        components: {Card},
        setup() {
            return {args}
        },
        template: `
            <Card v-bind="args">
                <template #title>Outline Variant</template>
                <p>Uses the outline design system variant with transparent background and visible border.</p>
            </Card>
        `
    }),
}

export const VariantGhost: Story = {
    args: {
        variant: 'ghost',
        padding: 'default',
    },
    render: (args) => ({
        components: {Card},
        setup() {
            return {args}
        },
        template: `
            <Card v-bind="args">
                <template #title>Ghost Variant</template>
                <p>Uses the ghost design system variant with fully transparent background and border.</p>
            </Card>
        `
    }),
}

export const AllDesignVariants: Story = {
    render: () => ({
        components: {Card},
        template: `
            <div class="grid gap-4 md:grid-cols-2 bg-background-dark p-6 rounded-lg">
                <Card variant="primary" hoverable>
                    <template #title>Primary</template>
                    <p>Primary variant with emphasis</p>
                </Card>
                <Card variant="secondary" hoverable>
                    <template #title>Secondary</template>
                    <p>Secondary variant - default style</p>
                </Card>
                <Card variant="outline" hoverable>
                    <template #title>Outline</template>
                    <p>Outline variant - minimal style</p>
                </Card>
                <Card variant="ghost" hoverable>
                    <template #title>Ghost</template>
                    <p>Ghost variant - transparent</p>
                </Card>
            </div>
        `
    }),
}
