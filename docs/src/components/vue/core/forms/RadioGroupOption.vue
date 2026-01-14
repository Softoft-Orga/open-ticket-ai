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
import { card } from '../design-system/recipes'
import { focusRing } from '../design-system/recipes'
import type { Variant, Tone } from '../design-system/tokens.ts'

interface Props {
  value: string | number
  label?: string
  description?: string
  variant?: Variant
  tone?: Tone
}

const props = withDefaults(defineProps<Props>(), {
  label: '',
  description: '',
  variant: 'surface',
  tone: undefined
})

const focusClasses = computed(() => {
  const tone = props.tone || 'primary'
  return focusRing({ tone })
})

const cardClasses = (checked: boolean, disabled: boolean) => {
  if (disabled) {
    return card({ variant: 'surface', size: 'sm', radius: 'lg' })
  }

  const tone = props.tone || 'primary'
  const variant = props.variant

  return card({
    variant: checked ? (variant === 'outline' ? 'outline' : 'subtle') : variant,
    tone: variant === 'outline' && checked ? 'primary' : tone,
    intensity: checked && variant !== 'outline' ? 'soft' : 'none',
    size: 'sm',
    radius: 'lg',
    highlighted: checked
  })
}

const checkedTextClass = computed(() => {
  const tone = props.tone || 'primary'

  switch (tone) {
    case 'info':
      return 'text-info'
    case 'success':
      return 'text-success'
    case 'warning':
      return 'text-warning'
    case 'danger':
      return 'text-danger'
    case 'neutral':
      return 'text-text-1'
    case 'primary':
    default:
      return 'text-primary-light'
  }
})

const checkedRadioClasses = computed(() => {
  const tone = props.tone || 'primary'

  switch (tone) {
    case 'info':
      return 'border-info text-info'
    case 'success':
      return 'border-success text-success'
    case 'warning':
      return 'border-warning text-warning'
    case 'danger':
      return 'border-danger text-danger'
    case 'neutral':
      return 'border-border-dark text-text-1'
    case 'primary':
    default:
      return 'border-primary text-primary'
  }
})

const uncheckedRadioClasses = computed(() => {
  return 'border-border-dark text-transparent'
})
</script>
