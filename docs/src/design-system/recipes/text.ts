import { tv, type VariantProps } from 'tailwind-variants'
import type { Tone } from '../tokens'

type Emphasis = 'normal' | 'dim' | 'strong'

/**
 * Text recipe - Text styles used across components
 * 
 * Provides consistent text styling with tone and emphasis variants.
 * Use for titles, body text, and dimmed text across the design system.
 */
export const text = tv({
  base: 'transition-colors duration-200',
  variants: {
    tone: {
      neutral: 'text-text-1',
      primary: 'text-primary',
      success: 'text-success',
      warning: 'text-warning',
      danger: 'text-danger',
      info: 'text-info'
    } satisfies Record<Tone, string>,
    emphasis: {
      normal: '',
      dim: 'text-text-dim',
      strong: 'font-semibold'
    }
  },
  compoundVariants: [
    // Dim emphasis overrides tone colors with dimmed variants
    { emphasis: 'dim', tone: 'neutral', class: 'text-text-dim' },
    { emphasis: 'dim', tone: 'primary', class: 'text-primary/70' },
    { emphasis: 'dim', tone: 'success', class: 'text-success/70' },
    { emphasis: 'dim', tone: 'warning', class: 'text-warning/70' },
    { emphasis: 'dim', tone: 'danger', class: 'text-danger/70' },
    { emphasis: 'dim', tone: 'info', class: 'text-info/70' }
  ],
  defaultVariants: {
    tone: 'neutral',
    emphasis: 'normal'
  }
})

export type TextVariants = VariantProps<typeof text>
