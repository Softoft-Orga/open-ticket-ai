import { tv, type VariantProps } from 'tailwind-variants'
import type { Size } from '../tokens.ts'

export const prose = tv({
  base: [
    'prose prose-invert max-w-none',

    'prose-headings:font-semibold prose-headings:text-text-1 prose-headings:scroll-mt-24',
    'prose-p:text-text-1 prose-p:leading-relaxed',
    'prose-a:text-primary prose-a:no-underline hover:prose-a:underline',
    'prose-strong:text-text-1 prose-strong:font-semibold',

    'prose-pre:bg-surface-dark prose-pre:border prose-pre:border-border-dark',

    'prose-blockquote:border-l-primary prose-blockquote:text-text-dim',
    'prose-hr:border-border-dark',

    'prose-ul:text-text-1 prose-ol:text-text-1',
    'prose-li:text-text-1 prose-li:marker:text-text-dim',

    'prose-img:rounded-lg prose-img:border prose-img:border-border-dark',

    'prose-table:text-text-1 prose-table:w-full',
    'prose-thead:border-b prose-thead:border-border-dark',
    'prose-tr:border-b prose-tr:border-border-dark',
    'prose-th:text-left prose-th:font-semibold prose-th:text-text-1',
    'prose-td:align-top prose-td:text-text-1',

    '[&_:not(pre)>code]:text-primary-light',
    '[&_:not(pre)>code]:bg-surface-dark',
    '[&_:not(pre)>code]:px-1.5',
    '[&_:not(pre)>code]:py-0.5',
    '[&_:not(pre)>code]:rounded',
    '[&_:not(pre)>code]:before:content-none',
    '[&_:not(pre)>code]:after:content-none',
  ],
  variants: {
    size: {
      sm: 'prose-sm',
      md: 'prose-base',
      lg: 'prose-lg',
    } satisfies Record<Size, string>,
  },
  defaultVariants: {
    size: 'md',
  },
})

export type ProseVariants = VariantProps<typeof prose>
