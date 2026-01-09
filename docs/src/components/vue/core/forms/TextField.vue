<template>
    <div class="inline-block w-full relative">
        <div v-if="icon" class="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
            <component :is="icon" class="w-5 h-5 text-gray-400" />
        </div>
        <input
            :disabled="disabled"
            :name="name"
            :placeholder="placeholder"
            :value="modelValue"
            :class="[
                'w-full py-2 border rounded-lg bg-white dark:bg-gray-800 text-gray-900 dark:text-gray-100 focus:outline-none focus:ring-2 focus:ring-blue-500 disabled:opacity-50 disabled:cursor-not-allowed',
                icon ? 'pl-10 pr-3' : 'px-3'
            ]"
            @input="onInput"
        />
    </div>
</template>

<script lang="ts" setup>
import type { Component } from 'vue';

const {modelValue, placeholder, disabled, name, icon} = defineProps<{
    modelValue?: string
    placeholder?: string
    disabled?: boolean
    name?: string
    icon?: Component
}>()

const emit = defineEmits<{
    (e: 'update:modelValue', value: string): void
}>()

function onInput(event: Event) {
    const target = event.target as HTMLInputElement
    emit('update:modelValue', target.value)
}

</script>
