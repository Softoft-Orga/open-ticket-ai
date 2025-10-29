<template>
  <div class="inline-block w-full">
    <input
        :disabled="disabled"
        :placeholder="placeholder"
        :value="modelValue"
        class="w-full px-3 py-2 border rounded-lg bg-white dark:bg-gray-800 text-gray-900 dark:text-gray-100 focus:outline-none focus:ring-2 focus:ring-blue-500 disabled:opacity-50 disabled:cursor-not-allowed"
        @input="onInput"
    />
  </div>
</template>

<script lang="ts" setup>
const {modelValue, placeholder, disabled} = defineProps<{
  modelValue?: string
  placeholder?: string
  disabled?: boolean
}>()

const emit = defineEmits<{
  (e: 'update:modelValue', value: string): void
}>()

function onInput(event: Event) {
  const target = event.target as HTMLInputElement
  emit('update:modelValue', target.value)
}
</script>
