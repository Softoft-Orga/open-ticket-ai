import { tv, type VariantProps } from 'tailwind-variants'

/**
 * Button recipe - Interactive button component
 * 
 * Supports solid, outline, and ghost variants with tone-based colors.
 * Includes focus ring, loading, disabled, and block states.
 */
export const button = tv({
  base: [
    'inline-flex items-center justify-center font-medium',
    'transition-all duration-200',
    'disabled:opacity-50 disabled:cursor-not-allowed',
    'active:scale-[0.98]',
    'focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-offset-2 focus-visible:ring-offset-background-dark'
  ],
  variants: {
    variant: {
      solid: 'border border-transparent shadow-sm',
      outline: 'border-2 bg-transparent',
      ghost: 'border border-transparent'
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
      sm: 'px-3 py-1.5 text-sm gap-1.5',
      md: 'px-4 py-2 text-base gap-2',
      lg: 'px-6 py-3 text-lg gap-2.5'
    },
    radius: {
      lg: 'rounded-lg',
      xl: 'rounded-xl',
      '2xl': 'rounded-2xl'
    },
    loading: {
      false: '',
      true: 'cursor-wait'
    },
    disabled: {
      false: '',
      true: 'opacity-50 cursor-not-allowed pointer-events-none'
    },
    block: {
      false: '',
      true: 'w-full'
    }
  },
  compoundVariants: [
    // Solid variant colors
    { variant: 'solid', tone: 'neutral', class: 'bg-surface-lighter text-text-1 hover:bg-surface-dark border-border-dark' },
    { variant: 'solid', tone: 'primary', class: 'bg-primary text-white hover:bg-primary-dark' },
    { variant: 'solid', tone: 'success', class: 'bg-success text-white hover:bg-success-dark' },
    { variant: 'solid', tone: 'warning', class: 'bg-warning text-white hover:bg-warning-dark' },
    { variant: 'solid', tone: 'danger', class: 'bg-danger text-white hover:bg-danger-dark' },
    { variant: 'solid', tone: 'info', class: 'bg-info text-white hover:bg-info/90' },
    
    // Outline variant colors
    { variant: 'outline', tone: 'neutral', class: 'border-border-dark text-text-1 hover:bg-surface-dark' },
    { variant: 'outline', tone: 'primary', class: 'border-primary text-primary hover:bg-primary/10' },
    { variant: 'outline', tone: 'success', class: 'border-success text-success hover:bg-success/10' },
    { variant: 'outline', tone: 'warning', class: 'border-warning text-warning hover:bg-warning/10' },
    { variant: 'outline', tone: 'danger', class: 'border-danger text-danger hover:bg-danger/10' },
    { variant: 'outline', tone: 'info', class: 'border-info text-info hover:bg-info/10' },
    
    // Ghost variant colors
    { variant: 'ghost', tone: 'neutral', class: 'text-text-1 hover:bg-surface-dark' },
    { variant: 'ghost', tone: 'primary', class: 'text-primary hover:bg-primary/10' },
    { variant: 'ghost', tone: 'success', class: 'text-success hover:bg-success/10' },
    { variant: 'ghost', tone: 'warning', class: 'text-warning hover:bg-warning/10' },
    { variant: 'ghost', tone: 'danger', class: 'text-danger hover:bg-danger/10' },
    { variant: 'ghost', tone: 'info', class: 'text-info hover:bg-info/10' }
  ],
  defaultVariants: {
    variant: 'solid',
    tone: 'primary',
    size: 'md',
    radius: 'xl',
    loading: false,
    disabled: false,
    block: false
  }
})

export type ButtonVariants = VariantProps<typeof button>
