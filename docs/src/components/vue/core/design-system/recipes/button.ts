import { tv, type VariantProps } from 'tailwind-variants'
import type { Variant, Tone, Size, Radius } from '../tokens.ts'

/**
 * Button recipe - Interactive button component
 *
 * Supports surface, outline, and subtle variants with tone-based colors.
 * Includes focus ring, loading, disabled, and block states.
 *
 * All variant keys use strict token types from tokens.ts.
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
      surface: 'border border-transparent shadow-sm',
      outline: 'border-2 bg-transparent',
      subtle: 'border border-transparent'
    } satisfies Record<Variant, string>,
    tone: {
      neutral: '',
      primary: '',
      success: '',
      warning: '',
      danger: '',
      info: ''
    } satisfies Record<Tone, string>,
    size: {
      sm: 'px-3 py-1.5 text-sm gap-1.5',
      md: 'px-4 py-2 text-base gap-2',
      lg: 'px-6 py-3 text-lg gap-2.5'
    } satisfies Record<Size, string>,
    radius: {
      lg: 'rounded-lg',
      xl: 'rounded-xl',
      '2xl': 'rounded-2xl'
    } satisfies Record<Radius, string>,
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
    // Surface variant colors
    { variant: 'surface', tone: 'neutral', class: 'bg-surface-lighter text-text-1 hover:bg-surface-dark border-border-dark' },
    { variant: 'surface', tone: 'primary', class: 'bg-primary text-white hover:bg-primary-dark' },
    { variant: 'surface', tone: 'success', class: 'bg-success text-white hover:bg-success-dark' },
    { variant: 'surface', tone: 'warning', class: 'bg-warning text-white hover:bg-warning-dark' },
    { variant: 'surface', tone: 'danger', class: 'bg-danger text-white hover:bg-danger-dark' },
    { variant: 'surface', tone: 'info', class: 'bg-info text-white hover:bg-info/90' },

    // Outline variant colors
    { variant: 'outline', tone: 'neutral', class: 'border-border-dark text-text-1 hover:bg-surface-dark' },
    { variant: 'outline', tone: 'primary', class: 'border-primary text-primary hover:bg-primary/10' },
    { variant: 'outline', tone: 'success', class: 'border-success text-success hover:bg-success/10' },
    { variant: 'outline', tone: 'warning', class: 'border-warning text-warning hover:bg-warning/10' },
    { variant: 'outline', tone: 'danger', class: 'border-danger text-danger hover:bg-danger/10' },
    { variant: 'outline', tone: 'info', class: 'border-info text-info hover:bg-info/10' },

    // Subtle variant colors
    { variant: 'subtle', tone: 'neutral', class: 'text-text-1 hover:bg-surface-dark' },
    { variant: 'subtle', tone: 'primary', class: 'text-primary hover:bg-primary/10' },
    { variant: 'subtle', tone: 'success', class: 'text-success hover:bg-success/10' },
    { variant: 'subtle', tone: 'warning', class: 'text-warning hover:bg-warning/10' },
    { variant: 'subtle', tone: 'danger', class: 'text-danger hover:bg-danger/10' },
    { variant: 'subtle', tone: 'info', class: 'text-info hover:bg-info/10' }
  ],
  defaultVariants: {
    variant: 'surface',
    tone: 'primary',
    size: 'md',
    radius: 'xl',
    loading: false,
    disabled: false,
    block: false
  }
})

export type ButtonVariants = VariantProps<typeof button>
