import { tv, type VariantProps } from 'tailwind-variants'
import type { Variant, Tone, Radius, Elevation, Hoverable, Highlighted } from '../tokens'

type Intensity = 'none' | 'soft'

/**
 * Surface recipe - Container surface styles
 * 
 * Provides consistent surface styling with support for variants, tones, radius,
 * elevation, and interactive states. Use `intensity` to control background opacity
 * and reduce the need for large compoundVariants.
 */
export const surface = tv({
  base: 'transition-colors duration-200',
  variants: {
    variant: {
      surface: 'bg-surface-dark border border-border-dark',
      outline: 'bg-transparent border border-border-dark/60',
      subtle: 'bg-surface-lighter border border-border-dark/80'
    } satisfies Record<Variant, string>,
    tone: {
      neutral: '',
      primary: 'border-primary/50',
      success: 'border-success/50',
      warning: 'border-warning/50',
      danger: 'border-danger/50',
      info: 'border-info/50'
    } satisfies Record<Tone, string>,
    radius: {
      lg: 'rounded-lg',
      xl: 'rounded-xl',
      '2xl': 'rounded-2xl'
    } satisfies Record<Radius, string>,
    elevation: {
      none: '',
      sm: 'shadow-sm',
      md: 'shadow-md',
      lg: 'shadow-lg'
    } satisfies Record<Elevation, string>,
    hoverable: {
      false: '',
      true: 'hover:-translate-y-px hover:shadow-lg transition-transform'
    },
    highlighted: {
      false: '',
      true: 'ring-1 ring-primary/40'
    },
    intensity: {
      none: '',
      soft: ''
    }
  },
  compoundVariants: [
    // Surface variant with soft intensity
    { variant: 'surface', intensity: 'soft', tone: 'primary', class: 'bg-primary/5' },
    { variant: 'surface', intensity: 'soft', tone: 'success', class: 'bg-success/5' },
    { variant: 'surface', intensity: 'soft', tone: 'warning', class: 'bg-warning/5' },
    { variant: 'surface', intensity: 'soft', tone: 'danger', class: 'bg-danger/5' },
    { variant: 'surface', intensity: 'soft', tone: 'info', class: 'bg-info/5' },
    
    // Subtle variant with soft intensity
    { variant: 'subtle', intensity: 'soft', tone: 'primary', class: 'bg-primary/10' },
    { variant: 'subtle', intensity: 'soft', tone: 'success', class: 'bg-success/10' },
    { variant: 'subtle', intensity: 'soft', tone: 'warning', class: 'bg-warning/10' },
    { variant: 'subtle', intensity: 'soft', tone: 'danger', class: 'bg-danger/10' },
    { variant: 'subtle', intensity: 'soft', tone: 'info', class: 'bg-info/10' }
  ],
  defaultVariants: {
    variant: 'surface',
    tone: 'neutral',
    radius: 'xl',
    elevation: 'none',
    hoverable: false,
    highlighted: false,
    intensity: 'none'
  }
})

export type SurfaceVariants = VariantProps<typeof surface>
