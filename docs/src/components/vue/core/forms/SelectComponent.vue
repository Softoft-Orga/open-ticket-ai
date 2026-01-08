<template>
  <div class="w-full">
    <Listbox v-model="selected" :disabled="disabled">
      <ListboxLabel v-if="label" class="block text-sm font-medium text-gray-300 mb-1">
        {{ label }}
      </ListboxLabel>

      <div class="relative">
        <ListboxButton
            class="w-full rounded-md border border-gray-600 bg-gray-800 py-2 pl-3 pr-10 text-left shadow-sm focus:outline-none focus-visible:border-indigo-500 focus-visible:ring-2 focus-visible:ring-white/75 focus-visible:ring-offset-2 focus-visible:ring-offset-indigo-500 text-white"
        >
          <span class="block truncate">{{ selectedLabel }}</span>
          <span class="pointer-events-none absolute inset-y-0 right-0 flex items-center pr-2">
            <ChevronUpDownIcon aria-hidden="true" class="h-5 w-5 text-gray-400"/>
          </span>
        </ListboxButton>

        <transition
            leave-active-class="transition duration-100 ease-in"
            leave-from-class="opacity-100"
            leave-to-class="opacity-0"
        >
          <ListboxOptions
              class="absolute !pl-0 !ml-0 mt-0 w-full overflow-auto rounded-md bg-gray-700 shadow-lg ring-1 ring-black/20 focus:outline-none list-none p-0 m-0 z-10"
          >
            <ListboxOption
                v-for="option in options"
                :key="option.value"
                v-slot="{ active, selected: isSelected }"
                :value="option.value"
                as="template"
                class="!ml-0"
            >
              <li
                  :class="[
                  'relative cursor-default select-none py-1 pl-10 pr-4 rounded-md transition-colors list-none',
                  {
                    'bg-indigo-500 text-white': active,
                    'text-gray-300': !active,
                  }
                ]"
              >
                <span :class="[isSelected ? 'font-semibold' : '', 'block truncate']">
                  {{ option.label }}
                </span>
                <span
                    v-if="isSelected"
                    :class="{ 'text-white': active, 'text-indigo-400': !active }"
                    class="absolute inset-y-0 left-0 flex items-center pl-3"
                >
                  <CheckIcon aria-hidden="true" class="h-5 w-5"/>
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

interface Option {
  value: string | number
  label: string
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
