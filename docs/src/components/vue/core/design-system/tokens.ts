/**
 * Shared design-system token types and constants for Vue components
 * 
 * These types align with Tailwind color tokens defined in tailwind.config.cjs:
 * - Variant: UI component style variants (primary, secondary, outline, ghost)
 * - Size: Component sizing (sm, md, lg)
 * - Tone: Semantic colors for status/alerts (info, success, warning, danger)
 * - Radius: Border radius options (md, lg, xl, 2xl)
 * - Elevation: Shadow/depth levels (none, sm, md, lg)
 */

// Button and general component variants
export type Variant = 'primary' | 'secondary' | 'outline' | 'ghost'
export const VARIANTS = ['primary', 'secondary', 'outline', 'ghost'] as const

// Component sizing
export type Size = 'sm' | 'md' | 'lg'
export const SIZES = ['sm', 'md', 'lg'] as const

// Semantic tones (align with Tailwind color tokens: info, success, warning, danger)
export type Tone = 'info' | 'success' | 'warning' | 'danger'
export const TONES = ['info', 'success', 'warning', 'danger'] as const

// Optional future tokens (for radius and elevation)
export type Radius = 'md' | 'lg' | 'xl' | '2xl'
export const RADII = ['md', 'lg', 'xl', '2xl'] as const

export type Elevation = 'none' | 'sm' | 'md' | 'lg'
export const ELEVATIONS = ['none', 'sm', 'md', 'lg'] as const
