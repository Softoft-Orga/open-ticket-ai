<template>
  <div class="divide-y divide-vp-border">
    <AccordionItem 
      v-for="(it, i) in items" 
      :key="i" 
      :title="it.title"
      :default-open="it.defaultOpen"
      :is-open="openItems.includes(i)"
      @toggle="toggleItem(i)"
    >
      <slot :name="`item-${i}`" :item="it">
        {{ it.content }}
      </slot>
    </AccordionItem>
  </div>
</template>

<script lang="ts" setup>
import {ref, watch} from 'vue'
import AccordionItem from './AccordionItem.vue'

interface Item {
  title: string
  content?: string
  defaultOpen?: boolean
}

interface Props {
  items?: Item[]
  allowMultiple?: boolean
  modelValue?: number[]
}

const props = withDefaults(defineProps<Props>(), {
  items: () => [],
  allowMultiple: false,
  modelValue: () => []
})

const emit = defineEmits<{
  (e: 'update:modelValue', value: number[]): void
}>()

const openItems = ref<number[]>(
  props.modelValue.length > 0 
    ? props.modelValue 
    : props.items
        .map((item, index) => item.defaultOpen ? index : -1)
        .filter(index => index !== -1)
)

watch(() => props.modelValue, (newValue) => {
  openItems.value = newValue
})

function toggleItem(index: number) {
  const isOpen = openItems.value.includes(index)
  
  if (props.allowMultiple) {
    if (isOpen) {
      openItems.value = openItems.value.filter(i => i !== index)
    } else {
      openItems.value = [...openItems.value, index]
    }
  } else {
    openItems.value = isOpen ? [] : [index]
  }
  
  emit('update:modelValue', openItems.value)
}
</script>
