<template>
    <div class="inline-block w-full relative">
        <div v-if="icon" class="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
            <component :is="icon" :class="iconClasses" />
        </div>
        <input
            :disabled="disabled"
            :name="name"
            :placeholder="placeholder"
            :value="modelValue"
            :type="type"
            :class="[
                'w-full transition-all focus:outline-none disabled:opacity-50 disabled:cursor-not-allowed',
                sizeClasses,
                variantClasses,
                icon ? 'pl-10' : ''
            ]"
            @input="onInput"
        />
    </div>
</template>

<script lang="ts" setup>
import { computed } from 'vue'
import type { Component } from 'vue'

interface Props {
    modelValue?: string
    placeholder?: string
    disabled?: boolean
    name?: string
    type?: string
    icon?: Component
    variant?: 'primary' | 'secondary' | 'outline' | 'ghost'
    size?: 'sm' | 'md' | 'lg'
}

const props = withDefaults(defineProps<Props>(), {
    variant: 'primary',
    size: 'md',
    type: 'text',
    disabled: false
})

const emit = defineEmits<{
    (e: 'update:modelValue', value: string): void
}>()

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
    switch (props.variant) {
        case 'secondary':
            return 'bg-surface-lighter border border-border-dark text-white placeholder:text-text-dim focus:ring-2 focus:ring-secondary/50 focus:border-secondary'
        case 'outline':
            return 'bg-transparent border border-border-dark text-white placeholder:text-text-dim hover:border-primary/50 focus:ring-2 focus:ring-primary/50 focus:border-primary'
        case 'ghost':
            return 'bg-transparent border-0 text-white placeholder:text-text-dim focus:ring-2 focus:ring-primary/30 focus:bg-white/5'
        default: // primary
            return 'bg-surface-dark border border-border-dark text-white placeholder:text-text-dim focus:ring-2 focus:ring-primary/50 focus:border-primary shadow-sm hover:shadow-[0_0_15px_rgba(166,13,242,0.2)]'
    }
})

const iconClasses = computed(() => {
    return 'w-5 h-5 text-text-dim'
})
</script>
