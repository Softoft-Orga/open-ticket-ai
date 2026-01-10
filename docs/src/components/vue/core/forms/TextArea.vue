<template>
    <div class="relative w-full">
        <div v-if="icon" class="absolute top-3 left-3 pointer-events-none z-10">
            <component :is="icon" class="w-5 h-5 text-text-dim" />
        </div>
        <textarea
            :disabled="disabled"
            :placeholder="placeholder"
            :value="modelValue"
            :class="[
                'w-full py-3 border rounded-xl bg-surface-dark text-white placeholder-text-dim transition-all duration-200 focus:outline-none focus:ring-2 focus:ring-primary/50 focus:border-primary/50 focus:shadow-[0_0_20px_rgba(166,13,242,0.2)] disabled:opacity-50 disabled:cursor-not-allowed resize-none',
                'border-border-dark hover:border-primary/30',
                icon ? 'pl-10 pr-3' : 'px-3'
            ]"
            rows="4"
            @input="onInput"
        />
    </div>
</template>

<script lang="ts" setup>
import type { Component } from 'vue';

const props = withDefaults(defineProps<{
  modelValue?: string
  placeholder?: string
  disabled?: boolean
  icon?: Component
}>(), {
  modelValue: '',
  placeholder: '',
  disabled: false,
})

const emit = defineEmits<{
  (e: 'update:modelValue', value: string): void
}>()

function onInput(event: Event) {
  const value = (event.target as HTMLTextAreaElement).value
  emit('update:modelValue', value)
}
</script>
