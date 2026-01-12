<template>
  <RadioGroupOption 
    v-slot="{ checked, disabled }" 
    :value="value" 
    as="template"
  >
    <div
      :class="[
        'relative flex cursor-pointer px-5 py-4 transition-all',
        cardClasses(checked, disabled),
        focusClasses,
        disabled && 'opacity-50 cursor-not-allowed'
      ]"
    >
      <div class="flex w-full items-center justify-between">
        <div class="flex items-center">
          <div class="text-sm">
            <div :class="['font-medium', checked ? checkedTextClass : 'text-gray-300']">
              <slot name="label">
                {{ label }}
              </slot>
            </div>
            <div
              v-if="description || $slots.description"
              class="text-text-dim mt-1"
            >
              <slot name="description">
                {{ description }}
              </slot>
            </div>
          </div>
        </div>
        
        <div
          :class="[
            'shrink-0 h-5 w-5 rounded-full border-2 flex items-center justify-center transition-all',
            checked ? checkedRadioClasses : uncheckedRadioClasses,
            disabled && 'opacity-50'
          ]"
        >
          <div
            v-if="checked"
            class="h-2.5 w-2.5 rounded-full bg-current"
          />
        </div>
      </div>
    </div>
  </RadioGroupOption>
</template>

<script lang="ts" setup>
import { computed } from 'vue'
import { RadioGroupOption } from '@headlessui/vue'
import { card } from '../../../../design-system/recipes/card'
import { focusRing } from '../../../../design-system/recipes/focus'
import type { Tone } from '../../../../design-system/tokens'

type VariantOption = 'primary' | 'secondary' | 'outline' | 'ghost'

interface Props {
  value: string | number
  label?: string
  description?: string
  variant?: VariantOption
  tone?: Tone
}

const props = withDefaults(defineProps<Props>(), {
  label: '',
  description: '',
  variant: 'primary',
  tone: undefined
})

const focusClasses = computed(() => {
  const tone = props.tone || (props.variant === 'secondary' ? 'neutral' : 'primary')
  return focusRing({ tone })
})

const cardClasses = (checked: boolean, disabled: boolean) => {
  if (disabled) {
    return card({ variant: 'surface', size: 'sm', radius: 'lg' })
  }

  const tone = props.tone
  if (tone) {
    return card({
      variant: checked ? 'subtle' : 'surface',
      tone,
      intensity: checked ? 'soft' : 'none',
      size: 'sm',
      radius: 'lg',
      highlighted: checked
    })
  }

  switch (props.variant) {
    case 'secondary':
      return card({
        variant: checked ? 'subtle' : 'surface',
        tone: 'neutral',
        size: 'sm',
        radius: 'lg',
        highlighted: checked
      })
    case 'outline':
      return card({
        variant: 'outline',
        tone: checked ? 'primary' : 'neutral',
        size: 'sm',
        radius: 'lg',
        highlighted: checked
      })
    case 'ghost':
      return card({
        variant: 'outline',
        tone: 'neutral',
        size: 'sm',
        radius: 'lg'
      })
    default:
      return card({
        variant: checked ? 'subtle' : 'surface',
        tone: 'primary',
        intensity: checked ? 'soft' : 'none',
        size: 'sm',
        radius: 'lg',
        highlighted: checked
      })
  }
}

const checkedTextClass = computed(() => {
  if (props.tone) {
    switch (props.tone) {
      case 'info':
        return 'text-info'
      case 'success':
        return 'text-success'
      case 'warning':
        return 'text-warning'
      case 'danger':
        return 'text-danger'
      default:
        break
    }
  }
  
  switch (props.variant) {
    case 'secondary':
      return 'text-secondary'
    case 'outline':
    case 'primary':
      return 'text-primary-light'
    case 'ghost':
      return 'text-white'
    default:
      return 'text-primary-light'
  }
})

const checkedRadioClasses = computed(() => {
  if (props.tone) {
    switch (props.tone) {
      case 'info':
        return 'border-info text-info'
      case 'success':
        return 'border-success text-success'
      case 'warning':
        return 'border-warning text-warning'
      case 'danger':
        return 'border-danger text-danger'
      default:
        break
    }
  }
  
  switch (props.variant) {
    case 'secondary':
      return 'border-secondary text-secondary'
    case 'outline':
    case 'primary':
      return 'border-primary text-primary'
    case 'ghost':
      return 'border-white text-white'
    default:
      return 'border-primary text-primary'
  }
})

const uncheckedRadioClasses = computed(() => {
  return 'border-border-dark text-transparent'
})
</script>
