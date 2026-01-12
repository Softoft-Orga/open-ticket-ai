import { tv, type VariantProps } from 'tailwind-variants'
import type { Tone } from '../tokens'

/**
 * Focus ring recipe - Focus ring styles for interactive elements
 * 
 * Provides consistent focus ring styling with tone-based colors.
 * Use for buttons, inputs, and other interactive components.
 */
export const focusRing = tv<{
  tone: Tone
}>({
  base: 'focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-offset-2 focus-visible:ring-offset-background-dark transition-shadow',
  variants: {
    tone: {
      neutral: 'focus-visible:ring-border-dark',
      primary: 'focus-visible:ring-primary',
      success: 'focus-visible:ring-success',
      warning: 'focus-visible:ring-warning',
      danger: 'focus-visible:ring-danger',
      info: 'focus-visible:ring-info'
    }
  },
  defaultVariants: {
    tone: 'primary'
  }
})

export type FocusRingVariants = VariantProps<typeof focusRing>
