import { tv, type VariantProps } from 'tailwind-variants'

/**
 * Alert recipe - Alert/notification component
 * 
 * Provides consistent alert styling with tone-based colors and variants.
 * Use for informational messages, warnings, errors, and success messages.
 */
export const alert = tv({
  base: 'flex items-start gap-3 p-4 rounded-lg border transition-colors duration-200',
  variants: {
    variant: {
      solid: 'border-transparent',
      soft: 'border-transparent',
      outline: 'bg-transparent'
    },
    tone: {
      neutral: '',
      primary: '',
      success: '',
      warning: '',
      danger: '',
      info: ''
    }
  },
  compoundVariants: [
    // Solid variant colors
    { variant: 'solid', tone: 'neutral', class: 'bg-surface-lighter text-text-1' },
    { variant: 'solid', tone: 'primary', class: 'bg-primary text-white' },
    { variant: 'solid', tone: 'success', class: 'bg-success text-white' },
    { variant: 'solid', tone: 'warning', class: 'bg-warning text-white' },
    { variant: 'solid', tone: 'danger', class: 'bg-danger text-white' },
    { variant: 'solid', tone: 'info', class: 'bg-info text-white' },
    
    // Soft variant colors
    { variant: 'soft', tone: 'neutral', class: 'bg-surface-dark text-text-1' },
    { variant: 'soft', tone: 'primary', class: 'bg-primary/10 text-primary border-primary/20' },
    { variant: 'soft', tone: 'success', class: 'bg-success/10 text-success border-success/20' },
    { variant: 'soft', tone: 'warning', class: 'bg-warning/10 text-warning border-warning/20' },
    { variant: 'soft', tone: 'danger', class: 'bg-danger/10 text-danger border-danger/20' },
    { variant: 'soft', tone: 'info', class: 'bg-info/10 text-info border-info/20' },
    
    // Outline variant colors
    { variant: 'outline', tone: 'neutral', class: 'border-border-dark text-text-1' },
    { variant: 'outline', tone: 'primary', class: 'border-primary text-primary' },
    { variant: 'outline', tone: 'success', class: 'border-success text-success' },
    { variant: 'outline', tone: 'warning', class: 'border-warning text-warning' },
    { variant: 'outline', tone: 'danger', class: 'border-danger text-danger' },
    { variant: 'outline', tone: 'info', class: 'border-info text-info' }
  ],
  defaultVariants: {
    variant: 'soft',
    tone: 'info'
  }
})

export type AlertVariants = VariantProps<typeof alert>
