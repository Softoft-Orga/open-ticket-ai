<template>
  <div class="w-full">
    <Listbox v-model="selected" :disabled="disabled">
      <ListboxLabel v-if="label" class="block text-sm font-medium text-text-dim mb-1">
        {{ label }}
      </ListboxLabel>

      <div class="relative">
        <ListboxButton
            class="w-full rounded-md border border-border-dark bg-surface-dark py-2 pl-3 pr-10 text-left shadow-sm focus:outline-none focus-visible:border-primary focus-visible:ring-2 focus-visible:ring-primary/50 text-white disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
        >
          <span class="block truncate">{{ selectedLabel }}</span>
          <span class="pointer-events-none absolute inset-y-0 right-0 flex items-center pr-2">
            <ChevronUpDownIcon aria-hidden="true" class="h-5 w-5 text-text-dim"/>
          </span>
        </ListboxButton>

        <UiTransitionSlide direction="down">
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
                  <CheckIcon aria-hidden="true" class="h-5 w-5"/>
                </span>
              </li>
            </ListboxOption>
          </ListboxOptions>
        </UiTransitionSlide>
      </div>
    </Listbox>
  </div>
</template>

<script lang="ts" setup>
import {computed, ref, watch} from 'vue'
import {Listbox, ListboxButton, ListboxLabel, ListboxOption, ListboxOptions,} from '@headlessui/vue'
import {CheckIcon, ChevronUpDownIcon} from '@heroicons/vue/20/solid'
import UiTransitionSlide from '../transitions/UiTransitionSlide.vue'

interface Option {
  value: string | number
  label: string
  disabled?: boolean
}

const props = withDefaults(
    defineProps<{
      options: Option[]
      modelValue?: string | number | null
      placeholder?: string
      disabled?: boolean
      label?: string
    }>(),
    {
      modelValue: null,
      placeholder: 'Select an option',
      disabled: false,
      label: '',
    }
)

const emit = defineEmits<{
  (e: 'update:modelValue', value: string | number | null): void
}>()

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
</script>
