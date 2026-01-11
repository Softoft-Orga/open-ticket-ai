<template>
  <div class="w-full">
    <Listbox
      v-model="selected"
      :disabled="disabled"
    >
      <ListboxLabel
        v-if="label"
        class="block text-sm font-medium text-text-dim mb-1"
      >
        {{ label }}
      </ListboxLabel>

      <div class="relative">
        <ListboxButton
          :class="buttonClasses"
        >
          <span class="block truncate">{{ selectedLabel }}</span>
          <span class="pointer-events-none absolute inset-y-0 right-0 flex items-center pr-2">
            <ChevronUpDownIcon
              aria-hidden="true"
              class="h-5 w-5 text-text-dim"
            />
          </span>
        </ListboxButton>

        <transition
          enter-active-class="transition-all duration-150 ease-out motion-reduce:transition-none motion-reduce:transform-none"
          enter-from-class="opacity-0 -translate-y-2"
          enter-to-class="opacity-100 translate-y-0"
          leave-active-class="transition-all duration-100 ease-in motion-reduce:transition-none motion-reduce:transform-none"
          leave-from-class="opacity-100 translate-y-0"
          leave-to-class="opacity-0 -translate-y-2"
        >
          <ListboxOptions
            class="absolute !pl-0 !ml-0 mt-1 max-h-60 w-full overflow-auto rounded-md bg-surface-lighter shadow-lg ring-1 ring-border-dark focus:outline-none list-none p-1 m-0 z-10"
          >
            <ListboxOption
              v-for="option in options"
              :key="option.value"
              v-slot="{ active, selected: isSelected }"
              :value="option.value"
              :disabled="option.disabled"
              as="template"
              class="!ml-0"
            >
              <li
                :class="[
                  'relative cursor-default select-none py-2 pl-10 pr-4 rounded-md transition-colors list-none',
                  {
                    'bg-primary text-white': active && !option.disabled,
                    'text-white': !active && !option.disabled,
                    'text-muted opacity-50 cursor-not-allowed': option.disabled,
                  }
                ]"
              >
                <span :class="[isSelected ? 'font-semibold' : '', 'block truncate']">
                  {{ option.label }}
                </span>
                <span
                  v-if="isSelected"
                  :class="{ 'text-white': active, 'text-primary-light': !active }"
                  class="absolute inset-y-0 left-0 flex items-center pl-3"
                >
                  <CheckIcon
                    aria-hidden="true"
                    class="h-5 w-5"
                  />
                </span>
              </li>
            </ListboxOption>
          </ListboxOptions>
        </transition>
      </div>
    </Listbox>
  </div>
</template>

<script lang="ts" setup>
import {computed, ref, watch} from 'vue'
import {Listbox, ListboxButton, ListboxLabel, ListboxOption, ListboxOptions,} from '@headlessui/vue'
import {CheckIcon, ChevronUpDownIcon} from '@heroicons/vue/20/solid'
import { input } from '../../../../design-system/recipes/input'

interface Option {
  value: string | number
  label: string
  disabled?: boolean
}

interface Props {
  options: Option[]
  modelValue?: string | number | null
  placeholder?: string
  disabled?: boolean
  label?: string
  error?: boolean
  size?: 'sm' | 'md' | 'lg'
}

const props = withDefaults(defineProps<Props>(), {
  modelValue: null,
  placeholder: 'Select an option',
  disabled: false,
  label: '',
  error: false,
  size: 'md'
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

const selectedLabel = computed(() => {
  const foundOption = props.options.find(opt => opt.value === selected.value)
  return foundOption ? foundOption.label : props.placeholder
})

const buttonClasses = computed(() => {
  return input({
    size: props.size,
    radius: 'lg',
    state: props.error ? 'error' : 'default',
    disabled: props.disabled
  }) + ' pr-10 text-left'
})
</script>
