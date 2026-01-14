import { tv, type VariantProps } from 'tailwind-variants'
import type { Tone, Size } from '../tokens.ts'

type Style = 'underline' | 'pill'

/**
 * Tabs recipe - Tab navigation component
 *
 * Supports underline and pill styles with tone-based colors.
 * Use for tab navigation patterns.
 */
export const tabs = tv({
  slots: {
    list: 'flex gap-1',
    trigger: 'px-4 py-2 font-medium transition-all duration-200 cursor-pointer',
    panel: 'mt-4'
  },
  variants: {
    style: {
      underline: {
        list: 'border-b border-border-dark',
        trigger: 'border-b-2 border-transparent hover:text-text-1 data-[selected]:border-current data-[selected]:text-current',
        panel: ''
      },
      pill: {
        list: 'bg-surface-dark p-1 rounded-xl',
        trigger: 'rounded-lg hover:bg-surface-lighter data-[selected]:bg-surface-lighter data-[selected]:text-current',
        panel: ''
      }
    },
    tone: {
      neutral: {
        trigger: 'text-text-dim data-[selected]:text-text-1'
      } satisfies Record<Tone, string>,
      primary: {
        trigger: 'text-text-dim data-[selected]:text-primary'
      },
      success: {
        trigger: 'text-text-dim data-[selected]:text-success'
      },
      warning: {
        trigger: 'text-text-dim data-[selected]:text-warning'
      },
      danger: {
        trigger: 'text-text-dim data-[selected]:text-danger'
      },
      info: {
        trigger: 'text-text-dim data-[selected]:text-info'
      }
    },
    size: {
      sm: {
        trigger: 'px-3 py-1.5 text-sm'
      } satisfies Record<Size, string>,
      md: {
        trigger: 'px-4 py-2 text-base'
      },
      lg: {
        trigger: 'px-5 py-2.5 text-lg'
      }
    }
  },
  defaultVariants: {
    style: 'underline',
    tone: 'primary',
    size: 'md'
  }
})

export type TabsVariants = VariantProps<typeof tabs>
