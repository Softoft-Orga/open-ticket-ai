import Card from '../src/components/vue/core/basic/Card.vue'
import Badge from '../src/components/vue/core/basic/Badge.vue'
import type {Meta, StoryObj} from '@storybook/vue3'
import { VARIANTS, TONES, SIZES, RADII, ELEVATIONS } from '../src/design-system/tokens'

const meta: Meta<typeof Card> = {
    title: 'Core/Card',
    component: Card,
    tags: ['autodocs'],
    argTypes: {
        variant: {
            control: 'select',
            options: VARIANTS,
            description: 'Visual style variant',
        },
        tone: {
            control: 'select',
            options: [undefined, ...TONES],
            description: 'Semantic tone (status color) - overrides variant background',
        },
        size: {
            control: 'select',
            options: SIZES,
            description: 'Card size (affects padding)',
        },
        radius: {
            control: 'select',
            options: RADII,
            description: 'Border radius',
        },
        elevation: {
            control: 'select',
            options: ELEVATIONS,
            description: 'Shadow elevation level',
        },
        hoverable: {
            control: 'boolean',
            description: 'Whether to add hover effect',
        },
    },
    parameters: {
        docs: {
            description: {
                component: 'Flexible card component with multiple slots (image, header, title, default, actions, footer). Uses design system tokens for consistent styling. Supports hover effects, various sizes, and semantic tones.'
            }
        }
    }
}
export default meta

type Story = StoryObj<typeof meta>

export const Default: Story = {
    args: {
        variant: 'surface',
        size: 'md',
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
        variant: 'surface',
        size: 'md',
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
        variant: 'surface',
        size: 'md',
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
        variant: 'surface',
        size: 'md',
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
        variant: 'surface',
        size: 'md',
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
        variant: 'surface',
        size: 'md',
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
        variant: 'surface',
        size: 'md',
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



// Tone Stories
export const ToneInfo: Story = {
    args: {
        tone: 'info',
        size: 'md',
    },
    render: (args) => ({
        components: {Card},
        setup() {
            return {args}
        },
        template: `
            <Card v-bind="args">
                <template #title>Info Tone</template>
                <p>Informational card with info tone styling.</p>
            </Card>
        `
    }),
}

export const ToneSuccess: Story = {
    args: {
        tone: 'success',
        size: 'md',
    },
    render: (args) => ({
        components: {Card},
        setup() {
            return {args}
        },
        template: `
            <Card v-bind="args">
                <template #title>Success Tone</template>
                <p>Success message with success tone styling.</p>
            </Card>
        `
    }),
}

export const ToneWarning: Story = {
    args: {
        tone: 'warning',
        size: 'md',
    },
    render: (args) => ({
        components: {Card},
        setup() {
            return {args}
        },
        template: `
            <Card v-bind="args">
                <template #title>Warning Tone</template>
                <p>Warning message with warning tone styling.</p>
            </Card>
        `
    }),
}

export const ToneDanger: Story = {
    args: {
        tone: 'danger',
        size: 'md',
    },
    render: (args) => ({
        components: {Card},
        setup() {
            return {args}
        },
        template: `
            <Card v-bind="args">
                <template #title>Danger Tone</template>
                <p>Error or danger message with danger tone styling.</p>
            </Card>
        `
    }),
}

// Size Stories
export const SizeSmall: Story = {
    args: {
        variant: 'surface',
        size: 'sm',
    },
    render: (args) => ({
        components: {Card},
        setup() {
            return {args}
        },
        template: `
            <Card v-bind="args">
                <template #title>Small Size</template>
                <p>Compact card with small padding.</p>
            </Card>
        `
    }),
}

export const SizeMedium: Story = {
    args: {
        variant: 'surface',
        size: 'md',
    },
    render: (args) => ({
        components: {Card},
        setup() {
            return {args}
        },
        template: `
            <Card v-bind="args">
                <template #title>Medium Size</template>
                <p>Default medium-sized card with standard padding.</p>
            </Card>
        `
    }),
}

export const SizeLarge: Story = {
    args: {
        variant: 'surface',
        size: 'lg',
    },
    render: (args) => ({
        components: {Card},
        setup() {
            return {args}
        },
        template: `
            <Card v-bind="args">
                <template #title>Large Size</template>
                <p>Spacious card with large padding for emphasis.</p>
            </Card>
        `
    }),
}

// Radius Stories
export const RadiusMedium: Story = {
    args: {
        variant: 'surface',
        radius: 'md',
    },
    render: (args) => ({
        components: {Card},
        setup() {
            return {args}
        },
        template: `
            <Card v-bind="args">
                <template #title>Medium Radius</template>
                <p>Card with medium border radius.</p>
            </Card>
        `
    }),
}

export const RadiusLarge: Story = {
    args: {
        variant: 'surface',
        radius: 'lg',
    },
    render: (args) => ({
        components: {Card},
        setup() {
            return {args}
        },
        template: `
            <Card v-bind="args">
                <template #title>Large Radius</template>
                <p>Card with large border radius (default).</p>
            </Card>
        `
    }),
}

export const RadiusXLarge: Story = {
    args: {
        variant: 'surface',
        radius: 'xl',
    },
    render: (args) => ({
        components: {Card},
        setup() {
            return {args}
        },
        template: `
            <Card v-bind="args">
                <template #title>Extra Large Radius</template>
                <p>Card with extra large border radius for a softer look.</p>
            </Card>
        `
    }),
}

export const Radius2XLarge: Story = {
    args: {
        variant: 'surface',
        radius: '2xl',
    },
    render: (args) => ({
        components: {Card},
        setup() {
            return {args}
        },
        template: `
            <Card v-bind="args">
                <template #title>2XL Radius</template>
                <p>Card with 2XL border radius for maximum roundness.</p>
            </Card>
        `
    }),
}

// Elevation Stories
export const ElevationNone: Story = {
    args: {
        variant: 'surface',
        elevation: 'none',
    },
    render: (args) => ({
        components: {Card},
        setup() {
            return {args}
        },
        template: `
            <Card v-bind="args">
                <template #title>No Elevation</template>
                <p>Flat card with no shadow.</p>
            </Card>
        `
    }),
}

export const ElevationSmall: Story = {
    args: {
        variant: 'surface',
        elevation: 'sm',
    },
    render: (args) => ({
        components: {Card},
        setup() {
            return {args}
        },
        template: `
            <Card v-bind="args">
                <template #title>Small Elevation</template>
                <p>Card with subtle shadow (default).</p>
            </Card>
        `
    }),
}

export const ElevationMedium: Story = {
    args: {
        variant: 'surface',
        elevation: 'md',
    },
    render: (args) => ({
        components: {Card},
        setup() {
            return {args}
        },
        template: `
            <Card v-bind="args">
                <template #title>Medium Elevation</template>
                <p>Card with medium shadow for more depth.</p>
            </Card>
        `
    }),
}

export const ElevationLarge: Story = {
    args: {
        variant: 'surface',
        elevation: 'lg',
    },
    render: (args) => ({
        components: {Card},
        setup() {
            return {args}
        },
        template: `
            <Card v-bind="args">
                <template #title>Large Elevation</template>
                <p>Card with large shadow for maximum depth and emphasis.</p>
            </Card>
        `
    }),
}

// Interactive
export const Hoverable: Story = {
    args: {
        variant: 'surface',
        size: 'md',
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
        variant: 'surface',
        size: 'md',
        elevation: 'md',
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
        variant: 'secondary',
        size: 'md',
        radius: 'xl',
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
                <Card variant="secondary" size="md" elevation="md" hoverable>
                    <template #title>
                        <h4 class="font-semibold">Accuracy</h4>
                    </template>
                    <p class="text-3xl font-bold text-green-400">95.2%</p>
                </Card>
                <Card variant="secondary" size="md" elevation="md" hoverable>
                    <template #title>
                        <h4 class="font-semibold">Tickets Processed</h4>
                    </template>
                    <p class="text-3xl font-bold text-blue-400">12,543</p>
                </Card>
                <Card variant="secondary" size="md" elevation="md" hoverable>
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
        variant: 'surface',
        size: 'md',
        radius: 'lg',
        elevation: 'sm',
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
                <p class="text-sm text-text-dim mt-2">Try changing the variant, tone, size, radius, elevation, and hoverable properties to see how they affect the card appearance.</p>
            </Card>
        `
    }),
}

// Design System Variant Examples
export const VariantSurface: Story = {
    args: {
        variant: 'surface',
    },
    render: (args) => ({
        components: {Card},
        setup() {
            return {args}
        },
        template: `
            <Card v-bind="args">
                <template #title>Surface Variant</template>
                <p>Uses the surface design system variant with surface-dark background and border.</p>
            </Card>
        `
    }),
}

export const VariantSubtle: Story = {
    args: {
        variant: 'subtle',
    },
    render: (args) => ({
        components: {Card},
        setup() {
            return {args}
        },
        template: `
            <Card v-bind="args">
                <template #title>Subtle Variant</template>
                <p>Uses the subtle design system variant with lighter surface background.</p>
            </Card>
        `
    }),
}

export const VariantOutline: Story = {
    args: {
        variant: 'outline',
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

export const AllDesignVariants: Story = {
    render: () => ({
        components: {Card},
        template: `
            <div class="grid gap-4 md:grid-cols-2 bg-background-dark p-6 rounded-lg">
                <Card variant="surface" hoverable>
                    <template #title>Surface</template>
                    <p>Surface variant - default style</p>
                </Card>
                <Card variant="subtle" hoverable>
                    <template #title>Subtle</template>
                    <p>Subtle variant with lighter background</p>
                </Card>
                <Card variant="outline" hoverable>
                    <template #title>Outline</template>
                    <p>Outline variant - minimal style</p>
                </Card>
            </div>
        `
    }),
}
