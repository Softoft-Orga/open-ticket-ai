import { tv, type VariantProps } from 'tailwind-variants'

/**
 * Badge recipe - Small label/tag component
 * 
 * Supports solid, soft, and outline variants with tone-based colors.
 * Used for status indicators, labels, and tags.
 */
export const badge = tv({
  base: 'inline-flex items-center justify-center font-medium transition-colors duration-200 whitespace-nowrap',
  variants: {
    variant: {
      solid: 'border border-transparent',
      soft: 'border border-transparent',
      outline: 'border bg-transparent'
    },
    tone: {
      neutral: '',
      primary: '',
      success: '',
      warning: '',
      danger: '',
      info: ''
    },
    size: {
      sm: 'px-2 py-0.5 text-xs gap-1 rounded-md',
      md: 'px-2.5 py-1 text-sm gap-1.5 rounded-lg'
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
    { variant: 'soft', tone: 'primary', class: 'bg-primary/10 text-primary' },
    { variant: 'soft', tone: 'success', class: 'bg-success/10 text-success' },
    { variant: 'soft', tone: 'warning', class: 'bg-warning/10 text-warning' },
    { variant: 'soft', tone: 'danger', class: 'bg-danger/10 text-danger' },
    { variant: 'soft', tone: 'info', class: 'bg-info/10 text-info' },
    
    // Outline variant colors
    { variant: 'outline', tone: 'neutral', class: 'border-border-dark text-text-1' },
    { variant: 'outline', tone: 'primary', class: 'border-primary text-primary' },
    { variant: 'outline', tone: 'success', class: 'border-success text-success' },
    { variant: 'outline', tone: 'warning', class: 'border-warning text-warning' },
    { variant: 'outline', tone: 'danger', class: 'border-danger text-danger' },
    { variant: 'outline', tone: 'info', class: 'border-info text-info' }
  ],
  defaultVariants: {
    variant: 'solid',
    tone: 'primary',
    size: 'md'
  }
})

export type BadgeVariants = VariantProps<typeof badge>
