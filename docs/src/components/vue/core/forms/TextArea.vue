<template>
    <div class="relative w-full">
        <div v-if="icon" class="absolute top-3 left-3 pointer-events-none">
            <component :is="icon" class="w-5 h-5 text-gray-400" />
        </div>
        <textarea
            :disabled="disabled"
            :placeholder="placeholder"
            :value="modelValue"
            :class="[
                'w-full py-2 border rounded-lg bg-gray-800 text-gray-100 focus:outline-none focus:ring-2 focus:ring-blue-500 disabled:opacity-50 disabled:cursor-not-allowed resize-none',
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
