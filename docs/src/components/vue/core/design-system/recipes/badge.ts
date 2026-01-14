import { tv, type VariantProps } from 'tailwind-variants'
import type { Variant, Tone, Size } from '../tokens.ts'

/**
 * Badge recipe - Small label/tag component
 *
 * Supports surface, subtle, and outline variants with tone-based colors.
 * Used for status indicators, labels, and tags.
 *
 * All variant keys use strict token types from tokens.ts.
 */
export const badge = tv({
  base: 'inline-flex items-center justify-center font-medium transition-colors duration-200 whitespace-nowrap',
  variants: {
    variant: {
      surface: 'border border-transparent',
      subtle: 'border border-transparent',
      outline: 'border bg-transparent'
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
      sm: 'px-2 py-0.5 text-xs gap-1 rounded-md',
      md: 'px-2.5 py-1 text-sm gap-1.5 rounded-lg'
    } satisfies Record<Size, string>
  },
  compoundVariants: [
    // Surface variant colors
    { variant: 'surface', tone: 'neutral', class: 'bg-surface-lighter text-text-1' },
    { variant: 'surface', tone: 'primary', class: 'bg-primary text-white' },
    { variant: 'surface', tone: 'success', class: 'bg-success-dark text-white' },
    { variant: 'surface', tone: 'warning', class: 'bg-warning text-white' },
    { variant: 'surface', tone: 'danger', class: 'bg-danger text-white' },
    { variant: 'surface', tone: 'info', class: 'bg-info text-white' },

    // Subtle variant colors
    { variant: 'subtle', tone: 'neutral', class: 'bg-surface-dark text-text-1' },
    { variant: 'subtle', tone: 'primary', class: 'bg-primary/10 text-primary' },
    { variant: 'subtle', tone: 'success', class: 'bg-success/10 text-success' },
    { variant: 'subtle', tone: 'warning', class: 'bg-warning/10 text-warning' },
    { variant: 'subtle', tone: 'danger', class: 'bg-danger/10 text-danger' },
    { variant: 'subtle', tone: 'info', class: 'bg-info/10 text-info' },

    // Outline variant colors
    { variant: 'outline', tone: 'neutral', class: 'border-border-dark text-text-1' },
    { variant: 'outline', tone: 'primary', class: 'border-primary text-primary' },
    { variant: 'outline', tone: 'success', class: 'border-success text-success' },
    { variant: 'outline', tone: 'warning', class: 'border-warning text-warning' },
    { variant: 'outline', tone: 'danger', class: 'border-danger text-danger' },
    { variant: 'outline', tone: 'info', class: 'border-info text-info' }
  ],
  defaultVariants: {
    variant: 'surface',
    tone: 'primary',
    size: 'md'
  }
})

export type BadgeVariants = VariantProps<typeof badge>
