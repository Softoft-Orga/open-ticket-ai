import { tv, type VariantProps } from 'tailwind-variants'
import type { Variant, Tone } from '../tokens'

/**
 * Alert recipe - Alert/notification component
 * 
 * Provides consistent alert styling with tone-based colors and variants.
 * Use for informational messages, warnings, errors, and success messages.
 * 
 * All variant keys use strict token types from tokens.ts.
 */
export const alert = tv({
  base: 'flex items-start gap-3 p-4 rounded-lg border transition-colors duration-200',
  variants: {
    variant: {
      surface: 'border-transparent',
      subtle: 'border-transparent',
      outline: 'bg-transparent'
    } satisfies Record<Variant, string>,
    tone: {
      neutral: '',
      primary: '',
      success: '',
      warning: '',
      danger: '',
      info: ''
    } satisfies Record<Tone, string>
  },
  compoundVariants: [
    // Surface variant colors
    { variant: 'surface', tone: 'neutral', class: 'bg-surface-lighter text-text-1' },
    { variant: 'surface', tone: 'primary', class: 'bg-primary text-white' },
    { variant: 'surface', tone: 'success', class: 'bg-success text-white' },
    { variant: 'surface', tone: 'warning', class: 'bg-warning text-white' },
    { variant: 'surface', tone: 'danger', class: 'bg-danger text-white' },
    { variant: 'surface', tone: 'info', class: 'bg-info text-white' },
    
    // Subtle variant colors
    { variant: 'subtle', tone: 'neutral', class: 'bg-surface-dark text-text-1' },
    { variant: 'subtle', tone: 'primary', class: 'bg-primary/10 text-primary border-primary/20' },
    { variant: 'subtle', tone: 'success', class: 'bg-success/10 text-success border-success/20' },
    { variant: 'subtle', tone: 'warning', class: 'bg-warning/10 text-warning border-warning/20' },
    { variant: 'subtle', tone: 'danger', class: 'bg-danger/10 text-danger border-danger/20' },
    { variant: 'subtle', tone: 'info', class: 'bg-info/10 text-info border-info/20' },
    
    // Outline variant colors
    { variant: 'outline', tone: 'neutral', class: 'border-border-dark text-text-1' },
    { variant: 'outline', tone: 'primary', class: 'border-primary text-primary' },
    { variant: 'outline', tone: 'success', class: 'border-success text-success' },
    { variant: 'outline', tone: 'warning', class: 'border-warning text-warning' },
    { variant: 'outline', tone: 'danger', class: 'border-danger text-danger' },
    { variant: 'outline', tone: 'info', class: 'border-info text-info' }
  ],
  defaultVariants: {
    variant: 'subtle',
    tone: 'info'
  }
})

export type AlertVariants = VariantProps<typeof alert>
