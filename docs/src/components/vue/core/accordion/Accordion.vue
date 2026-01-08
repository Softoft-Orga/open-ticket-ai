<template>
  <div class="divide-y divide-vp-border">
    <AccordionItem
      v-for="(it, i) in items"
      :key="i"
      :title="it.title"
      :default-open="it.defaultOpen || false"
      :is-open="isItemOpen(i)"
      @toggle="handleToggle(i)"
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
  multiple?: boolean
  modelValue?: number[]
}

const props = withDefaults(defineProps<Props>(), {
  items: () => [],
  multiple: true,
  modelValue: () => []
})

const emit = defineEmits<{
  (e: 'update:modelValue', value: number[]): void
}>()

const openItems = ref<Set<number>>(new Set(props.modelValue))

watch(() => props.modelValue, (newVal) => {
  openItems.value = new Set(newVal)
}, {deep: true})

const isItemOpen = (index: number): boolean => {
  return openItems.value.has(index)
}

const handleToggle = (index: number) => {
  const newOpenItems = new Set(openItems.value)

  if (newOpenItems.has(index)) {
    newOpenItems.delete(index)
  } else {
    if (!props.multiple) {
      newOpenItems.clear()
    }
    newOpenItems.add(index)
  }

  openItems.value = newOpenItems
  emit('update:modelValue', Array.from(newOpenItems))
}
</script>
