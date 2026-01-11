import { tv, type VariantProps } from 'tailwind-variants'
import type { Elevation, Radius, Size, Tone, Variant } from './tokens'
export * from './tokens'

export const card = tv({
  base: 'transition duration-200 text-text-1',
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
    size: {
      sm: 'p-4 gap-3 text-sm',
      md: 'p-6 gap-4 text-base',
      lg: 'p-8 gap-5 text-lg'
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
      true: 'hover:-translate-y-px hover:shadow-lg'
    },
    highlighted: {
      false: '',
      true: 'ring-1 ring-primary/40'
    }
  },
  compoundVariants: [
    { variant: 'surface', tone: 'primary', class: 'bg-primary/5' },
    { variant: 'surface', tone: 'success', class: 'bg-success/5' },
    { variant: 'surface', tone: 'warning', class: 'bg-warning/5' },
    { variant: 'surface', tone: 'danger', class: 'bg-danger/5' },
    { variant: 'surface', tone: 'info', class: 'bg-info/5' },
    { variant: 'subtle', tone: 'primary', class: 'bg-primary/10' },
    { variant: 'subtle', tone: 'success', class: 'bg-success/10' },
    { variant: 'subtle', tone: 'warning', class: 'bg-warning/10' },
    { variant: 'subtle', tone: 'danger', class: 'bg-danger/10' },
    { variant: 'subtle', tone: 'info', class: 'bg-info/10' },
    { variant: 'outline', tone: 'neutral', class: 'border-border-dark' }
  ],
  defaultVariants: {
    variant: 'surface' satisfies Variant,
    tone: 'neutral' satisfies Tone,
    size: 'md' satisfies Size,
    radius: 'xl' satisfies Radius,
    elevation: 'none' satisfies Elevation,
    hoverable: false,
    highlighted: false
  }
})

export type CardVariants = VariantProps<typeof card>
