<template>
  <div :class="containerClasses">
    <AccordionItem 
      v-for="(it, i) in items" 
      :key="i" 
      :title="it.title"
      :default-open="it.defaultOpen || false"
      :variant="variant"
    >
      <slot
        :name="`item-${i}`"
        :item="it"
      >
        {{ it.content }}
      </slot>
    </AccordionItem>
  </div>
</template>

<script lang="ts" setup>
import { computed } from 'vue'
import AccordionItem from './AccordionItem.vue'

type Variant = 'default' | 'ghost' | 'bordered' | 'gradient'

interface Item {
  title: string
  content?: string
  defaultOpen?: boolean
}

interface Props {
  items?: Item[]
  variant?: Variant
}

const props = withDefaults(defineProps<Props>(), {
  items: () => [],
  variant: 'default'
})

const containerClasses = computed(() => {
  const variants = {
    default: 'divide-y divide-border-dark',
    ghost: 'space-y-1',
    bordered: '',
    gradient: ''
  }
  
  return variants[props.variant]
})
</script>
