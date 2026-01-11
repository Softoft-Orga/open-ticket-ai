import { tv, type VariantProps } from 'tailwind-variants'

/**
 * Input recipe - Text input, textarea, and select styling
 * 
 * Provides consistent styling for form inputs with state variants.
 * Includes focus ring and support for error/success states.
 */
export const input = tv({
  base: [
    'w-full px-3 py-2 bg-surface-dark border text-text-1',
    'placeholder:text-text-dim',
    'transition-all duration-200',
    'disabled:opacity-50 disabled:cursor-not-allowed',
    'focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-offset-2 focus-visible:ring-offset-background-dark'
  ],
  variants: {
    tone: {
      neutral: 'border-border-dark',
      primary: 'border-primary/50',
      success: 'border-success/50',
      warning: 'border-warning/50',
      danger: 'border-danger/50',
      info: 'border-info/50'
    },
    size: {
      sm: 'px-2.5 py-1.5 text-sm',
      md: 'px-3 py-2 text-base',
      lg: 'px-4 py-3 text-lg'
    },
    radius: {
      lg: 'rounded-lg',
      xl: 'rounded-xl',
      '2xl': 'rounded-2xl'
    },
    state: {
      default: '',
      error: 'border-danger focus-visible:ring-danger',
      success: 'border-success focus-visible:ring-success'
    },
    disabled: {
      false: '',
      true: 'opacity-50 cursor-not-allowed pointer-events-none'
    }
  },
  compoundVariants: [
    // State overrides tone for border colors
    { state: 'error', class: 'border-danger' },
    { state: 'success', class: 'border-success' }
  ],
  defaultVariants: {
    tone: 'neutral',
    size: 'md',
    radius: 'lg',
    state: 'default',
    disabled: false
  }
})

export type InputVariants = VariantProps<typeof input>
