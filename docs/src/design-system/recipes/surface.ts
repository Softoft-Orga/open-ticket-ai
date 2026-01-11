import { tv, type VariantProps } from 'tailwind-variants'

/**
 * Surface recipe - Container surface styles
 * 
 * Provides consistent surface styling with support for variants, tones, radius,
 * elevation, and interactive states. Use `tint` to control background opacity
 * and reduce the need for large compoundVariants.
 */
export const surface = tv({
  base: 'transition-colors duration-200',
  variants: {
    variant: {
      surface: 'bg-surface-dark border border-border-dark',
      outline: 'bg-transparent border border-border-dark/60',
      subtle: 'bg-surface-lighter border border-border-dark/80'
    },
    tone: {
      neutral: '',
      primary: 'border-primary/50',
      success: 'border-success/50',
      warning: 'border-warning/50',
      danger: 'border-danger/50',
      info: 'border-info/50'
    },
    radius: {
      lg: 'rounded-lg',
      xl: 'rounded-xl',
      '2xl': 'rounded-2xl'
    },
    elevation: {
      none: '',
      sm: 'shadow-sm',
      md: 'shadow-md',
      lg: 'shadow-lg'
    },
    hoverable: {
      false: '',
      true: 'hover:-translate-y-px hover:shadow-lg transition-transform'
    },
    highlighted: {
      false: '',
      true: 'ring-1 ring-primary/40'
    },
    tint: {
      none: '',
      soft: ''
    }
  },
  compoundVariants: [
    // Surface variant with soft tint
    { variant: 'surface', tint: 'soft', tone: 'primary', class: 'bg-primary/5' },
    { variant: 'surface', tint: 'soft', tone: 'success', class: 'bg-success/5' },
    { variant: 'surface', tint: 'soft', tone: 'warning', class: 'bg-warning/5' },
    { variant: 'surface', tint: 'soft', tone: 'danger', class: 'bg-danger/5' },
    { variant: 'surface', tint: 'soft', tone: 'info', class: 'bg-info/5' },
    
    // Subtle variant with soft tint
    { variant: 'subtle', tint: 'soft', tone: 'primary', class: 'bg-primary/10' },
    { variant: 'subtle', tint: 'soft', tone: 'success', class: 'bg-success/10' },
    { variant: 'subtle', tint: 'soft', tone: 'warning', class: 'bg-warning/10' },
    { variant: 'subtle', tint: 'soft', tone: 'danger', class: 'bg-danger/10' },
    { variant: 'subtle', tint: 'soft', tone: 'info', class: 'bg-info/10' }
  ],
  defaultVariants: {
    variant: 'surface',
    tone: 'neutral',
    radius: 'xl',
    elevation: 'none',
    hoverable: false,
    highlighted: false,
    tint: 'none'
  }
})

export type SurfaceVariants = VariantProps<typeof surface>
