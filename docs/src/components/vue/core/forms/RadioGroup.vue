<template>
  <RadioGroupRoot
    v-model="selected"
    :disabled="disabled"
  >
    <RadioGroupLabel
      v-if="label"
      class="block text-sm font-medium text-gray-300 mb-3"
    >
      {{ label }}
    </RadioGroupLabel>
    
    <div
      v-if="$slots.description"
      class="text-sm text-text-dim mb-3"
    >
      <slot name="description" />
    </div>
    
    <div class="space-y-2">
      <slot />
    </div>
  </RadioGroupRoot>
</template>

<script lang="ts" setup>
import { ref, watch } from 'vue'
import { RadioGroup as RadioGroupRoot, RadioGroupLabel } from '@headlessui/vue'

interface Props {
  modelValue?: string | number | null
  label?: string
  disabled?: boolean
}

const props = withDefaults(defineProps<Props>(), {
  modelValue: null,
  label: '',
  disabled: false
})

/* eslint-disable no-unused-vars */
const emit = defineEmits<{
  (e: 'update:modelValue', value: string | number | null): void
}>()
/* eslint-enable no-unused-vars */

const selected = ref(props.modelValue)

watch(
  () => props.modelValue,
  (newValue) => {
    selected.value = newValue
  }
)

watch(selected, (newValue) => {
  emit('update:modelValue', newValue)
})
</script>
