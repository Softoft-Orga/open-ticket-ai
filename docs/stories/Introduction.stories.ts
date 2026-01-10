import type { Meta, StoryObj } from '@storybook/vue3';

const meta: Meta = {
    title: 'Documentation/Introduction',
    tags: ['autodocs'],
    parameters: {
        docs: {
            page: () => `
                <div style="font-family: system-ui, -apple-system, sans-serif; padding: 2rem; max-width: 1200px;">
                    <h1>Open Ticket AI Component Library</h1>
                    <p style="font-size: 1.125rem; color: #666; margin-bottom: 2rem;">
                        This is the complete documentation for all components in the Open Ticket AI design system.
                    </p>

                    <h2>Component Categories</h2>
                    
                    <div style="display: grid; gap: 1.5rem; margin-top: 1rem;">
                        <section style="border: 1px solid #e0e0e0; padding: 1.5rem; border-radius: 8px;">
                            <h3 style="margin-top: 0;">Core Components</h3>
                            <p>Basic building blocks and interactive elements:</p>
                            <ul style="columns: 2; column-gap: 2rem;">
                                <li>Accordion - Collapsible content panels</li>
                                <li>Badge - Status and category labels</li>
                                <li>Button - Primary interactive element</li>
                                <li>Callout - Highlighted information boxes</li>
                                <li>Card - Content grouping container</li>
                                <li>Input - Text input field</li>
                                <li>Link - Navigation element</li>
                                <li>SelectComponent - Dropdown selection</li>
                                <li>Table - Data presentation</li>
                                <li>Tabs - Content organization</li>
                                <li>TextArea - Multi-line input</li>
                            </ul>
                        </section>

                        <section style="border: 1px solid #e0e0e0; padding: 1.5rem; border-radius: 8px;">
                            <h3 style="margin-top: 0;">Documentation Components</h3>
                            <p>Components for content presentation:</p>
                            <ul>
                                <li>Alert - Contextual messages</li>
                                <li>CodeBlock - Syntax-highlighted code</li>
                                <li>CodeTabs - Multiple code examples</li>
                                <li>TableOfContents - Navigation aid</li>
                            </ul>
                        </section>

                        <section style="border: 1px solid #e0e0e0; padding: 1.5rem; border-radius: 8px;">
                            <h3 style="margin-top: 0;">Layout Components</h3>
                            <p>Page structure and navigation:</p>
                            <ul>
                                <li>NavBar - Main navigation header</li>
                                <li>FooterComponent - Page footer</li>
                            </ul>
                        </section>

                        <section style="border: 1px solid #e0e0e0; padding: 1.5rem; border-radius: 8px;">
                            <h3 style="margin-top: 0;">Feature Components</h3>
                            <p>Product features and capabilities:</p>
                            <ul style="columns: 2; column-gap: 2rem;">
                                <li>FeatureGrid - Grid layout for features</li>
                                <li>FeatureItem - Individual feature card</li>
                                <li>FeatureShowcase - Highlighted feature</li>
                                <li>IntegrationLogos - Supported integrations</li>
                                <li>PluginCard - Plugin information</li>
                            </ul>
                        </section>

                        <section style="border: 1px solid #e0e0e0; padding: 1.5rem; border-radius: 8px;">
                            <h3 style="margin-top: 0;">Product & Service Components</h3>
                            <p>Products, services, and pricing:</p>
                            <ul style="columns: 2; column-gap: 2rem;">
                                <li>ProductCard - Product display</li>
                                <li>ProductCards - Multiple products</li>
                                <li>ServiceCard - Service offering</li>
                                <li>ServicesGrid - Service card grid</li>
                                <li>ServiceInquiryModal - Inquiry form</li>
                                <li>ServicePackagesComponent - Package comparison</li>
                                <li>SupportPlansComponent - Support options</li>
                                <li>LiteFreeDetail - Free tier details</li>
                                <li>LiteProDetail - Pro tier details</li>
                                <li>ComparisonRow - Feature comparison</li>
                            </ul>
                        </section>

                        <section style="border: 1px solid #e0e0e0; padding: 1.5rem; border-radius: 8px;">
                            <h3 style="margin-top: 0;">Form Components</h3>
                            <p>Interactive forms and inputs:</p>
                            <ul>
                                <li>ContactForm - Contact submission</li>
                                <li>WaitlistSignupForm - Email collection</li>
                            </ul>
                        </section>

                        <section style="border: 1px solid #e0e0e0; padding: 1.5rem; border-radius: 8px;">
                            <h3 style="margin-top: 0;">Demo & Prediction Components</h3>
                            <p>AI capability demonstrations:</p>
                            <ul>
                                <li>OTAIPredictionDemo - Single prediction</li>
                                <li>MultiTagPredictionDemo - Multi-tag showcase</li>
                                <li>PredictionCard - Prediction results</li>
                                <li>ResultTable - Tabular results</li>
                                <li>PipeSidecar - Pipeline visualization</li>
                            </ul>
                        </section>

                        <section style="border: 1px solid #e0e0e0; padding: 1.5rem; border-radius: 8px;">
                            <h3 style="margin-top: 0;">Blog Components</h3>
                            <p>Blog and article components:</p>
                            <ul>
                                <li>AuthorBio - Author information</li>
                                <li>ReadingTime - Reading time indicator</li>
                                <li>RelatedPosts - Related content</li>
                                <li>ShareButtons - Social sharing</li>
                            </ul>
                        </section>

                        <section style="border: 1px solid #e0e0e0; padding: 1.5rem; border-radius: 8px;">
                            <h3 style="margin-top: 0;">Performance & Metrics</h3>
                            <p>Performance data display:</p>
                            <ul>
                                <li>PerformanceMetric - Performance indicators</li>
                                <li>FullMetric - Detailed metric card</li>
                                <li>RoiCalculator - ROI calculation</li>
                                <li>StepIndicator - Multi-step process</li>
                            </ul>
                        </section>

                        <section style="border: 1px solid #e0e0e0; padding: 1.5rem; border-radius: 8px;">
                            <h3 style="margin-top: 0;">Architecture & Taxonomy</h3>
                            <p>System architecture and taxonomy:</p>
                            <ul>
                                <li>ArchitectureOverview - System diagram</li>
                                <li>TaxonomyCard - Category display</li>
                                <li>TaxonomyRow - Item row</li>
                                <li>TagFilter - Tag filtering</li>
                            </ul>
                        </section>

                        <section style="border: 1px solid #e0e0e0; padding: 1.5rem; border-radius: 8px;">
                            <h3 style="margin-top: 0;">Marketplace Components</h3>
                            <p>Marketplace and plugin ecosystem:</p>
                            <ul>
                                <li>MarketplacePagination - Pagination controls</li>
                                <li>MarketplaceSkeletonCard - Loading placeholder</li>
                                <li>LatestNews - News and updates</li>
                            </ul>
                        </section>
                    </div>

                    <h2 style="margin-top: 3rem;">Design System Principles</h2>
                    <div style="background: #f5f5f5; padding: 1.5rem; border-radius: 8px; margin-top: 1rem;">
                        <ul style="margin: 0;">
                            <li><strong>Color Palette:</strong> Deep purple/cyan glow with dark surfaces</li>
                            <li><strong>Typography:</strong> Inter font family with consistent sizing</li>
                            <li><strong>Spacing:</strong> Generous spacing for clarity</li>
                            <li><strong>Accessibility:</strong> WCAG 2.1 AA compliant</li>
                            <li><strong>Responsiveness:</strong> Mobile-first approach</li>
                        </ul>
                    </div>

                    <h2 style="margin-top: 3rem;">How to Use This Documentation</h2>
                    <p>Navigate through the sidebar to explore individual components. Each component page includes:</p>
                    <ul>
                        <li>Interactive examples with all variants</li>
                        <li>Customizable controls to test different props</li>
                        <li>Source code snippets</li>
                        <li>Accessibility information</li>
                        <li>Usage guidelines</li>
                    </ul>

                    <div style="margin-top: 2rem; padding: 1.5rem; background: #e3f2fd; border-left: 4px solid #2196f3; border-radius: 4px;">
                        <strong>Getting Started:</strong> Browse the component categories in the sidebar to find what you need.
                        Each category groups related components for easy discovery.
                    </div>
                </div>
            `,
        },
    },
};

export default meta;

type Story = StoryObj<typeof meta>;

// This empty story is required for the docs page to render
export const Docs: Story = {};
