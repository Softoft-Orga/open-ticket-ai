import { tv, type VariantProps } from 'tailwind-variants'
import type { Size } from '../tokens.ts'

/**
 * Prose recipe - MDX/Markdown content wrapper
 *
 * Provides consistent typography styling for documentation content.
 * Compatible with dark theme and works alongside @tailwindcss/typography.
 * Apply to wrapper elements containing rendered markdown/MDX.
 */
export const prose = tv({
  base: [
    'prose prose-invert max-w-none',
    'prose-headings:font-semibold prose-headings:text-text-1',
    'prose-p:text-text-1 prose-p:leading-relaxed',
    'prose-a:text-primary prose-a:no-underline hover:prose-a:underline',
    'prose-strong:text-text-1 prose-strong:font-semibold',
    'prose-code:text-primary-light prose-code:bg-surface-dark prose-code:px-1.5 prose-code:py-0.5 prose-code:rounded',
    'prose-pre:bg-surface-dark prose-pre:border prose-pre:border-border-dark',
    'prose-blockquote:border-l-primary prose-blockquote:text-text-dim',
    'prose-hr:border-border-dark',
    'prose-ul:text-text-1 prose-ol:text-text-1',
    'prose-li:text-text-1 prose-li:marker:text-text-dim',
    'prose-img:rounded-lg prose-img:border prose-img:border-border-dark',
    'prose-table:text-text-1'
  ],
  variants: {
    size: {
      sm: [
        'prose-sm',
        'prose-headings:mb-3 prose-headings:mt-6',
        'prose-p:mb-3',
        'prose-ul:my-3 prose-ol:my-3',
        'prose-li:my-1'
      ],
      md: [
        'prose-base',
        'prose-headings:mb-4 prose-headings:mt-8',
        'prose-p:mb-4',
        'prose-ul:my-4 prose-ol:my-4',
        'prose-li:my-1.5'
      ],
      lg: [
        'prose-lg',
        'prose-headings:mb-5 prose-headings:mt-10',
        'prose-p:mb-5',
        'prose-ul:my-5 prose-ol:my-5',
        'prose-li:my-2'
      ]
    } satisfies Record<Size, string>
  },
  defaultVariants: {
    size: 'md'
  }
})

export type ProseVariants = VariantProps<typeof prose>
