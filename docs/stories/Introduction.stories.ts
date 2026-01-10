import type { Meta, StoryObj } from '@storybook/vue3';

/**
 * Introduction Page - Full Component Documentation
 * 
 * Note: MDX documentation pages have limited/experimental support in Storybook 10.1 with Vue 3.
 * This TypeScript-based documentation page is the recommended approach for Vue 3 projects.
 * 
 * Reference: https://github.com/storybookjs/storybook/issues/30016
 */

const meta: Meta = {
    title: 'Documentation/Introduction',
    tags: ['autodocs'],
    parameters: {
        docs: {
            page: () => `
                <div style="font-family: system-ui, -apple-system, sans-serif; padding: 2rem; max-width: 1200px; line-height: 1.6;">
                    <h1 style="font-size: 2.5rem; margin-bottom: 0.5rem; color: #1a1a1a;">Open Ticket AI Component Library</h1>
                    <p style="font-size: 1.125rem; color: #666; margin-bottom: 2rem;">
                        Complete documentation for all components in the Open Ticket AI design system.
                    </p>

                    <div style="background: #f0f7ff; border-left: 4px solid #0066cc; padding: 1rem 1.5rem; margin-bottom: 2rem; border-radius: 4px;">
                        <p style="margin: 0; color: #004080;">
                            <strong>💡 Navigation Tip:</strong> Use the sidebar on the left to browse components by category. 
                            Click on any component to see its interactive examples, props, and usage guidelines.
                        </p>
                    </div>

                    <h2 style="font-size: 2rem; margin-top: 2.5rem; margin-bottom: 1rem; color: #1a1a1a;">Component Categories</h2>
                    
                    <div style="display: grid; gap: 1.5rem; margin-top: 1.5rem;">
                        <section style="border: 1px solid #e0e0e0; padding: 1.5rem; border-radius: 8px; background: #ffffff;">
                            <h3 style="margin-top: 0; color: #0066cc; font-size: 1.5rem;">Core Components</h3>
                            <p style="color: #666; margin-bottom: 1rem;">Basic building blocks and interactive elements</p>
                            <ul style="columns: 2; column-gap: 2rem; margin: 0; padding-left: 1.5rem;">
                                <li style="margin-bottom: 0.5rem;"><strong>Accordion</strong> - Collapsible content panels</li>
                                <li style="margin-bottom: 0.5rem;"><strong>Badge</strong> - Status and category labels</li>
                                <li style="margin-bottom: 0.5rem;"><strong>Button</strong> - Primary interactive element</li>
                                <li style="margin-bottom: 0.5rem;"><strong>Callout</strong> - Highlighted information boxes</li>
                                <li style="margin-bottom: 0.5rem;"><strong>Card</strong> - Content grouping container</li>
                                <li style="margin-bottom: 0.5rem;"><strong>Input</strong> - Text input field</li>
                                <li style="margin-bottom: 0.5rem;"><strong>Link</strong> - Navigation element</li>
                                <li style="margin-bottom: 0.5rem;"><strong>SelectComponent</strong> - Dropdown selection</li>
                                <li style="margin-bottom: 0.5rem;"><strong>Table</strong> - Data presentation</li>
                                <li style="margin-bottom: 0.5rem;"><strong>Tabs</strong> - Content organization</li>
                                <li style="margin-bottom: 0.5rem;"><strong>TextArea</strong> - Multi-line input</li>
                            </ul>
                        </section>

                        <section style="border: 1px solid #e0e0e0; padding: 1.5rem; border-radius: 8px; background: #ffffff;">
                            <h3 style="margin-top: 0; color: #0066cc; font-size: 1.5rem;">Documentation Components</h3>
                            <p style="color: #666; margin-bottom: 1rem;">Components for content presentation</p>
                            <ul style="margin: 0; padding-left: 1.5rem;">
                                <li style="margin-bottom: 0.5rem;"><strong>Alert</strong> - Contextual messages</li>
                                <li style="margin-bottom: 0.5rem;"><strong>CodeBlock</strong> - Syntax-highlighted code</li>
                                <li style="margin-bottom: 0.5rem;"><strong>CodeTabs</strong> - Multiple code examples</li>
                                <li style="margin-bottom: 0.5rem;"><strong>TableOfContents</strong> - Navigation aid</li>
                            </ul>
                        </section>

                        <section style="border: 1px solid #e0e0e0; padding: 1.5rem; border-radius: 8px; background: #ffffff;">
                            <h3 style="margin-top: 0; color: #0066cc; font-size: 1.5rem;">Layout Components</h3>
                            <p style="color: #666; margin-bottom: 1rem;">Page structure and navigation</p>
                            <ul style="margin: 0; padding-left: 1.5rem;">
                                <li style="margin-bottom: 0.5rem;"><strong>NavBar</strong> - Main navigation header</li>
                                <li style="margin-bottom: 0.5rem;"><strong>FooterComponent</strong> - Page footer</li>
                            </ul>
                        </section>

                        <section style="border: 1px solid #e0e0e0; padding: 1.5rem; border-radius: 8px; background: #ffffff;">
                            <h3 style="margin-top: 0; color: #0066cc; font-size: 1.5rem;">Feature Components</h3>
                            <p style="color: #666; margin-bottom: 1rem;">Product features and capabilities</p>
                            <ul style="columns: 2; column-gap: 2rem; margin: 0; padding-left: 1.5rem;">
                                <li style="margin-bottom: 0.5rem;"><strong>FeatureGrid</strong> - Grid layout for features</li>
                                <li style="margin-bottom: 0.5rem;"><strong>FeatureItem</strong> - Individual feature card</li>
                                <li style="margin-bottom: 0.5rem;"><strong>FeatureShowcase</strong> - Highlighted feature</li>
                                <li style="margin-bottom: 0.5rem;"><strong>IntegrationLogos</strong> - Supported integrations</li>
                                <li style="margin-bottom: 0.5rem;"><strong>PluginCard</strong> - Plugin information</li>
                            </ul>
                        </section>

                        <section style="border: 1px solid #e0e0e0; padding: 1.5rem; border-radius: 8px; background: #ffffff;">
                            <h3 style="margin-top: 0; color: #0066cc; font-size: 1.5rem;">Product & Service Components</h3>
                            <p style="color: #666; margin-bottom: 1rem;">Products, services, and pricing</p>
                            <ul style="columns: 2; column-gap: 2rem; margin: 0; padding-left: 1.5rem;">
                                <li style="margin-bottom: 0.5rem;"><strong>ProductCard</strong> - Product display</li>
                                <li style="margin-bottom: 0.5rem;"><strong>ProductCards</strong> - Multiple products</li>
                                <li style="margin-bottom: 0.5rem;"><strong>ServiceCard</strong> - Service offering</li>
                                <li style="margin-bottom: 0.5rem;"><strong>ServicesGrid</strong> - Service card grid</li>
                                <li style="margin-bottom: 0.5rem;"><strong>ServiceInquiryModal</strong> - Inquiry form</li>
                                <li style="margin-bottom: 0.5rem;"><strong>ServicePackagesComponent</strong> - Package comparison</li>
                                <li style="margin-bottom: 0.5rem;"><strong>SupportPlansComponent</strong> - Support options</li>
                                <li style="margin-bottom: 0.5rem;"><strong>LiteFreeDetail</strong> - Free tier details</li>
                                <li style="margin-bottom: 0.5rem;"><strong>LiteProDetail</strong> - Pro tier details</li>
                                <li style="margin-bottom: 0.5rem;"><strong>ComparisonRow</strong> - Feature comparison</li>
                            </ul>
                        </section>

                        <section style="border: 1px solid #e0e0e0; padding: 1.5rem; border-radius: 8px; background: #ffffff;">
                            <h3 style="margin-top: 0; color: #0066cc; font-size: 1.5rem;">Form Components</h3>
                            <p style="color: #666; margin-bottom: 1rem;">Interactive forms and inputs</p>
                            <ul style="margin: 0; padding-left: 1.5rem;">
                                <li style="margin-bottom: 0.5rem;"><strong>ContactForm</strong> - Contact submission</li>
                                <li style="margin-bottom: 0.5rem;"><strong>WaitlistSignupForm</strong> - Email collection</li>
                            </ul>
                        </section>

                        <section style="border: 1px solid #e0e0e0; padding: 1.5rem; border-radius: 8px; background: #ffffff;">
                            <h3 style="margin-top: 0; color: #0066cc; font-size: 1.5rem;">Demo & Prediction Components</h3>
                            <p style="color: #666; margin-bottom: 1rem;">AI capability demonstrations</p>
                            <ul style="margin: 0; padding-left: 1.5rem;">
                                <li style="margin-bottom: 0.5rem;"><strong>OTAIPredictionDemo</strong> - Single prediction</li>
                                <li style="margin-bottom: 0.5rem;"><strong>MultiTagPredictionDemo</strong> - Multi-tag showcase</li>
                                <li style="margin-bottom: 0.5rem;"><strong>PredictionCard</strong> - Prediction results</li>
                                <li style="margin-bottom: 0.5rem;"><strong>ResultTable</strong> - Tabular results</li>
                                <li style="margin-bottom: 0.5rem;"><strong>PipeSidecar</strong> - Pipeline visualization</li>
                            </ul>
                        </section>

                        <section style="border: 1px solid #e0e0e0; padding: 1.5rem; border-radius: 8px; background: #ffffff;">
                            <h3 style="margin-top: 0; color: #0066cc; font-size: 1.5rem;">Blog Components</h3>
                            <p style="color: #666; margin-bottom: 1rem;">Blog and article components</p>
                            <ul style="margin: 0; padding-left: 1.5rem;">
                                <li style="margin-bottom: 0.5rem;"><strong>AuthorBio</strong> - Author information</li>
                                <li style="margin-bottom: 0.5rem;"><strong>ReadingTime</strong> - Reading time indicator</li>
                                <li style="margin-bottom: 0.5rem;"><strong>RelatedPosts</strong> - Related content</li>
                                <li style="margin-bottom: 0.5rem;"><strong>ShareButtons</strong> - Social sharing</li>
                            </ul>
                        </section>

                        <section style="border: 1px solid #e0e0e0; padding: 1.5rem; border-radius: 8px; background: #ffffff;">
                            <h3 style="margin-top: 0; color: #0066cc; font-size: 1.5rem;">Performance & Metrics</h3>
                            <p style="color: #666; margin-bottom: 1rem;">Performance data display</p>
                            <ul style="margin: 0; padding-left: 1.5rem;">
                                <li style="margin-bottom: 0.5rem;"><strong>PerformanceMetric</strong> - Performance indicators</li>
                                <li style="margin-bottom: 0.5rem;"><strong>FullMetric</strong> - Detailed metric card</li>
                                <li style="margin-bottom: 0.5rem;"><strong>RoiCalculator</strong> - ROI calculation</li>
                                <li style="margin-bottom: 0.5rem;"><strong>StepIndicator</strong> - Multi-step process</li>
                            </ul>
                        </section>

                        <section style="border: 1px solid #e0e0e0; padding: 1.5rem; border-radius: 8px; background: #ffffff;">
                            <h3 style="margin-top: 0; color: #0066cc; font-size: 1.5rem;">Architecture & Taxonomy</h3>
                            <p style="color: #666; margin-bottom: 1rem;">System architecture and taxonomy</p>
                            <ul style="margin: 0; padding-left: 1.5rem;">
                                <li style="margin-bottom: 0.5rem;"><strong>ArchitectureOverview</strong> - System diagram</li>
                                <li style="margin-bottom: 0.5rem;"><strong>TaxonomyCard</strong> - Category display</li>
                                <li style="margin-bottom: 0.5rem;"><strong>TaxonomyRow</strong> - Item row</li>
                                <li style="margin-bottom: 0.5rem;"><strong>TagFilter</strong> - Tag filtering</li>
                            </ul>
                        </section>

                        <section style="border: 1px solid #e0e0e0; padding: 1.5rem; border-radius: 8px; background: #ffffff;">
                            <h3 style="margin-top: 0; color: #0066cc; font-size: 1.5rem;">Marketplace Components</h3>
                            <p style="color: #666; margin-bottom: 1rem;">Marketplace and plugin ecosystem</p>
                            <ul style="margin: 0; padding-left: 1.5rem;">
                                <li style="margin-bottom: 0.5rem;"><strong>MarketplacePagination</strong> - Pagination controls</li>
                                <li style="margin-bottom: 0.5rem;"><strong>MarketplaceSkeletonCard</strong> - Loading placeholder</li>
                                <li style="margin-bottom: 0.5rem;"><strong>LatestNews</strong> - News and updates</li>
                            </ul>
                        </section>
                    </div>

                    <div style="margin-top: 3rem; padding: 2rem; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); border-radius: 12px; color: white;">
                        <h2 style="margin-top: 0; font-size: 1.75rem; color: white;">Design System Principles</h2>
                        <ul style="margin: 1rem 0; padding-left: 1.5rem; line-height: 1.8;">
                            <li style="margin-bottom: 0.75rem;"><strong>Color Palette:</strong> Deep purple/cyan glow with dark surfaces</li>
                            <li style="margin-bottom: 0.75rem;"><strong>Typography:</strong> Inter font family with consistent sizing</li>
                            <li style="margin-bottom: 0.75rem;"><strong>Spacing:</strong> Generous spacing for clarity</li>
                            <li style="margin-bottom: 0.75rem;"><strong>Accessibility:</strong> WCAG 2.1 AA compliant</li>
                            <li style="margin-bottom: 0.75rem;"><strong>Responsiveness:</strong> Mobile-first approach</li>
                        </ul>
                    </div>

                    <h2 style="font-size: 2rem; margin-top: 3rem; margin-bottom: 1rem; color: #1a1a1a;">How to Use This Documentation</h2>
                    <p style="color: #666; margin-bottom: 1rem;">Navigate through the sidebar to explore individual components. Each component page includes:</p>
                    <ul style="color: #666; padding-left: 1.5rem; line-height: 1.8;">
                        <li style="margin-bottom: 0.5rem;">✨ Interactive examples with all variants</li>
                        <li style="margin-bottom: 0.5rem;">🎛️ Customizable controls to test different props</li>
                        <li style="margin-bottom: 0.5rem;">💻 Source code snippets</li>
                        <li style="margin-bottom: 0.5rem;">♿ Accessibility information</li>
                        <li style="margin-bottom: 0.5rem;">📖 Usage guidelines</li>
                    </ul>

                    <div style="margin-top: 2rem; padding: 1.5rem; background: #e8f5e9; border-left: 4px solid #4caf50; border-radius: 4px;">
                        <p style="margin: 0; color: #2e7d32;">
                            <strong>🚀 Getting Started:</strong> Browse the component categories in the sidebar to find what you need. 
                            Each category groups related components for easy discovery.
                        </p>
                    </div>

                    <div style="margin-top: 2rem; padding: 1rem; background: #fff3cd; border-left: 4px solid #ffc107; border-radius: 4px;">
                        <p style="margin: 0; color: #856404; font-size: 0.875rem;">
                            <strong>📌 Technical Note:</strong> This documentation page uses TypeScript instead of MDX because 
                            MDX documentation pages have limited/experimental support in Storybook 10.1 with Vue 3. 
                            See: <a href="https://github.com/storybookjs/storybook/issues/30016" target="_blank" style="color: #856404; text-decoration: underline;">GitHub Issue #30016</a>
                        </p>
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
