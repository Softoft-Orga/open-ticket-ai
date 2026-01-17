import type { Organization, WithContext } from 'schema-dts';

/**
 * Get the base Organization schema for Open Ticket AI
 * This represents the company/organization behind the website
 */
export function getOrganizationSchema(): WithContext<Organization> {
  return {
    '@context': 'https://schema.org',
    '@type': 'Organization',
    name: 'Open Ticket AI',
    url: 'https://openticketai.com',
    logo: 'https://openticketai.com/favicon.ico',
    description:
      'Enterprise-grade on-premise AI solution for automated ticket tagging and helpdesk automation. Privacy-focused ticket intelligence without cloud dependency.',
    sameAs: [
      // Add social media links when available
    ],
    contactPoint: {
      '@type': 'ContactPoint',
      contactType: 'Sales',
      availableLanguage: ['en', 'de'],
    },
  };
}
