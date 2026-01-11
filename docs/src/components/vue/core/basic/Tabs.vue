<template>
  <TabGroup 
    :selected-index="selectedIndex" 
    :vertical="vertical"
    as="div"
    :class="containerClass"
    @change="handleChange"
  >
    <TabList 
      :class="tabsStyles.list()"
      :aria-label="ariaLabel"
    >
      <Tab
        v-for="(label, idx) in tabs"
        :key="idx"
        v-slot="{ selected }"
        as="template"
      >
        <button
          :class="tabsStyles.trigger({ class: selected ? 'data-[selected]' : '' })"
          :data-selected="selected || undefined"
        >
          {{ label }}
        </button>
      </Tab>
    </TabList>

    <TabPanels :class="tabPanelsClass">
      <TabPanel
        v-for="(label, idx) in tabs"
        :key="`panel-${idx}`"
        :class="tabsStyles.panel()"
      >
        <slot
          :name="`tab-${idx}`"
          :index="idx"
        />
      </TabPanel>
    </TabPanels>
  </TabGroup>
</template>

<script lang="ts" setup>
import { ref, computed, watch } from 'vue'
import { TabGroup, TabList, Tab, TabPanels, TabPanel } from '@headlessui/vue'
import { tabs } from '../../../../design-system/recipes'
import type { Tone, Size } from '../../../../design-system/tokens'

type TabVariant = 'underline' | 'pill'

interface Props {
  tabs: string[]
  modelValue?: number
  ariaLabel?: string
  size?: Size
  variant?: TabVariant
  tone?: Tone
  vertical?: boolean
}

const props = withDefaults(defineProps<Props>(), {
  modelValue: 0,
  ariaLabel: 'Tabs',
  size: 'md',
  variant: 'underline',
  tone: 'primary',
  vertical: false
})

/* eslint-disable no-unused-vars */
const emit = defineEmits<{
  (e: 'update:modelValue', value: number): void
  (e: 'change', value: number): void
}>()
/* eslint-enable no-unused-vars */

const selectedIndex = ref(props.modelValue)

watch(() => props.modelValue, (newVal) => {
  selectedIndex.value = newVal
})

const handleChange = (index: number) => {
  selectedIndex.value = index
  emit('update:modelValue', index)
  emit('change', index)
}

const tabsStyles = computed(() => {
  return tabs({
    variant: props.variant,
    tone: props.tone,
    size: props.size
  })
})

const containerClass = computed(() => {
  const classes = []
  if (props.vertical) {
    classes.push('flex gap-4')
  }
  return classes.join(' ')
})

const tabPanelsClass = computed(() => {
  const classes = []
  
  if (props.vertical) {
    classes.push('flex-1')
  }
  
  return classes.join(' ')
})
</script>
