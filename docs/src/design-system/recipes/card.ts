import { tv, type VariantProps } from 'tailwind-variants'
import { surface } from './surface'

/**
 * Card recipe - Composable card component
 * 
 * Builds on the surface recipe with additional spacing variants.
 * Use for any card-like container components.
 */
export const card = tv({
  extend: surface,
  base: 'text-text-1',
  variants: {
    size: {
      sm: 'p-4 gap-3 text-sm',
      md: 'p-6 gap-4 text-base',
      lg: 'p-8 gap-5 text-lg'
    }
  },
  defaultVariants: {
    variant: 'surface',
    tone: 'neutral',
    size: 'md',
    radius: 'xl',
    elevation: 'none',
    hoverable: false,
    highlighted: false,
    tint: 'none'
  }
})

export type CardVariants = VariantProps<typeof card>
