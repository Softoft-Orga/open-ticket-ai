<template>
  <div class="inline-block w-full relative">
    <div
      v-if="icon"
      class="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none"
    >
      <component
        :is="icon"
        :class="iconClasses"
      />
    </div>
    <input
      :disabled="disabled"
      :name="name"
      :placeholder="placeholder"
      :value="modelValue"
      :type="type"
      :class="[
        'w-full transition-colors duration-200 focus:outline-none disabled:opacity-50 disabled:cursor-not-allowed',
        sizeClasses,
        variantClasses,
        toneClasses,
        icon ? 'pl-10' : ''
      ]"
      @input="onInput"
    >
  </div>
</template>

<script lang="ts" setup>
import { computed } from 'vue'
import type { Component } from 'vue'
import type { Variant, Size, Tone } from '../design-system/tokens'

interface Props {
    modelValue?: string
    placeholder?: string
    disabled?: boolean
    name?: string
    type?: string
    icon?: Component
    variant?: Variant
    size?: Size
    tone?: Tone
}

const props = withDefaults(defineProps<Props>(), {
    variant: 'primary',
    size: 'md',
    type: 'text',
    disabled: false
})

/* eslint-disable no-unused-vars */
const emit = defineEmits<{
    (e: 'update:modelValue', value: string): void
}>()
/* eslint-enable no-unused-vars */

function onInput(event: Event) {
    const target = event.target as HTMLInputElement
    emit('update:modelValue', target.value)
}

const sizeClasses = computed(() => {
    switch (props.size) {
        case 'sm':
            return 'h-10 px-3 text-sm rounded-lg'
        case 'lg':
            return 'h-14 px-5 text-lg rounded-xl'
        default: // md
            return 'h-12 px-4 text-base rounded-xl'
    }
})

const variantClasses = computed(() => {
    if (props.tone) {
        return ''
    }
    
    switch (props.variant) {
        case 'secondary':
            return 'bg-surface-lighter border border-secondary/30 text-white placeholder:text-text-dim hover:border-secondary/50 focus:ring-2 focus:ring-secondary/50 focus:border-secondary active:border-secondary active:ring-secondary/60'
        case 'outline':
            return 'bg-transparent border-2 border-border-dark text-white placeholder:text-text-dim hover:border-primary/40 focus:ring-2 focus:ring-primary/40 focus:border-primary active:border-primary active:ring-primary/50'
        case 'ghost':
            return 'bg-transparent border-0 text-white placeholder:text-text-dim hover:bg-white/5 focus:ring-2 focus:ring-primary/30 focus:bg-white/10 active:bg-white/15'
        default: // primary
            return 'bg-surface-dark border border-primary/40 text-white placeholder:text-text-dim hover:border-primary/60 hover:shadow-[0_0_15px_rgba(166,13,242,0.2)] focus:ring-2 focus:ring-primary/50 focus:border-primary active:border-primary active:ring-primary/60 shadow-sm'
    }
})

const toneClasses = computed(() => {
    if (!props.tone) {
        return ''
    }
    
    const baseClasses = 'bg-surface-dark text-white placeholder:text-text-dim'
    
    switch (props.tone) {
        case 'info':
            return `${baseClasses} border border-info/40 hover:border-info/60 focus:ring-2 focus:ring-info/50 focus:border-info active:border-info active:ring-info/60`
        case 'success':
            return `${baseClasses} border border-success/40 hover:border-success/60 focus:ring-2 focus:ring-success/50 focus:border-success active:border-success active:ring-success/60`
        case 'warning':
            return `${baseClasses} border border-warning/40 hover:border-warning/60 focus:ring-2 focus:ring-warning/50 focus:border-warning active:border-warning active:ring-warning/60`
        case 'danger':
            return `${baseClasses} border border-danger/40 hover:border-danger/60 focus:ring-2 focus:ring-danger/50 focus:border-danger active:border-danger active:ring-danger/60`
        default:
            return baseClasses
    }
})

const iconClasses = computed(() => {
    return 'w-5 h-5 text-text-dim'
})
</script>
