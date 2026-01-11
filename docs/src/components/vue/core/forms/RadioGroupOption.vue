<template>
  <RadioGroupOption 
    v-slot="{ checked, disabled }" 
    :value="value" 
    as="template"
  >
    <div
      :class="[
        'relative flex cursor-pointer rounded-lg px-5 py-4 transition-all',
        'focus:outline-none focus-visible:ring-2 focus-visible:ring-offset-2',
        ringClasses,
        variantClasses(checked, disabled),
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
import type { Variant, Tone } from '../design-system/tokens'

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
  variant: 'primary',
  tone: undefined
})

const ringClasses = computed(() => {
  if (props.tone) {
    switch (props.tone) {
      case 'info':
        return 'focus-visible:ring-info focus-visible:ring-offset-background-dark'
      case 'success':
        return 'focus-visible:ring-success focus-visible:ring-offset-background-dark'
      case 'warning':
        return 'focus-visible:ring-warning focus-visible:ring-offset-background-dark'
      case 'danger':
        return 'focus-visible:ring-danger focus-visible:ring-offset-background-dark'
    }
  }
  
  switch (props.variant) {
    case 'secondary':
      return 'focus-visible:ring-secondary focus-visible:ring-offset-background-dark'
    case 'outline':
      return 'focus-visible:ring-primary/50 focus-visible:ring-offset-background-dark'
    case 'ghost':
      return 'focus-visible:ring-white/50 focus-visible:ring-offset-background-dark'
    default: // primary
      return 'focus-visible:ring-primary focus-visible:ring-offset-background-dark'
  }
})

const variantClasses = (checked: boolean, disabled: boolean) => {
  if (disabled) {
    return 'bg-surface-dark border border-border-dark'
  }

  const toneColor = props.tone ? getToneClasses(checked) : null
  if (toneColor) return toneColor

  switch (props.variant) {
    case 'secondary':
      return checked
        ? 'bg-secondary/10 border-2 border-secondary shadow-[0_0_15px_rgba(31,213,255,0.2)]'
        : 'bg-surface-dark border border-border-dark hover:border-secondary/50 hover:bg-secondary/5'
    case 'outline':
      return checked
        ? 'bg-primary/5 border-2 border-primary shadow-[0_0_15px_rgba(166,13,242,0.15)]'
        : 'bg-transparent border border-border-dark hover:border-primary/50 hover:bg-white/5'
    case 'ghost':
      return checked
        ? 'bg-white/10 border border-white/30'
        : 'bg-transparent border border-transparent hover:bg-white/5 hover:border-white/10'
    default: // primary
      return checked
        ? 'bg-primary/10 border-2 border-primary shadow-[0_0_15px_rgba(166,13,242,0.2)]'
        : 'bg-surface-dark border border-border-dark hover:border-primary/50 hover:bg-primary/5'
  }
}

const getToneClasses = (checked: boolean) => {
  switch (props.tone) {
    case 'info':
      return checked
        ? 'bg-info/10 border-2 border-info shadow-[0_0_15px_rgba(60,200,255,0.2)]'
        : 'bg-surface-dark border border-border-dark hover:border-info/50 hover:bg-info/5'
    case 'success':
      return checked
        ? 'bg-success/10 border-2 border-success shadow-[0_0_15px_rgba(22,219,160,0.2)]'
        : 'bg-surface-dark border border-border-dark hover:border-success/50 hover:bg-success/5'
    case 'warning':
      return checked
        ? 'bg-warning/10 border-2 border-warning shadow-[0_0_15px_rgba(247,183,51,0.2)]'
        : 'bg-surface-dark border border-border-dark hover:border-warning/50 hover:bg-warning/5'
    case 'danger':
      return checked
        ? 'bg-danger/10 border-2 border-danger shadow-[0_0_15px_rgba(255,79,109,0.2)]'
        : 'bg-surface-dark border border-border-dark hover:border-danger/50 hover:bg-danger/5'
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
