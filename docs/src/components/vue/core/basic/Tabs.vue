<template>
  <TabGroup 
    :selected-index="selectedIndex" 
    @change="handleChange"
    :vertical="vertical"
    as="div"
    :class="containerClass"
  >
    <TabList 
      :class="tabListClass"
      :aria-label="ariaLabel"
    >
      <Tab
        v-for="(label, idx) in tabs"
        :key="idx"
        v-slot="{ selected }"
        as="template"
      >
        <button
          :class="getTabButtonClass(selected)"
        >
          {{ label }}
          <div
            v-if="selected && showIndicator && variant !== 'pills'"
            :class="indicatorClass"
          ></div>
        </button>
      </Tab>
    </TabList>

    <TabPanels :class="tabPanelsClass">
      <TabPanel
        v-for="(label, idx) in tabs"
        :key="`panel-${idx}`"
        :class="tabPanelClass"
      >
        <slot :name="`tab-${idx}`" :index="idx" />
      </TabPanel>
    </TabPanels>
  </TabGroup>
</template>

<script lang="ts" setup>
import { ref, computed, watch } from 'vue'
import { TabGroup, TabList, Tab, TabPanels, TabPanel } from '@headlessui/vue'

type TabSize = 'sm' | 'md' | 'lg'
type TabVariant = 'underline' | 'pills' | 'enclosed' | 'ghost'
type TabAlignment = 'start' | 'center' | 'end' | 'stretch'

interface Props {
  tabs: string[]
  modelValue?: number
  ariaLabel?: string
  size?: TabSize
  variant?: TabVariant
  alignment?: TabAlignment
  fullWidth?: boolean
  vertical?: boolean
  showIndicator?: boolean
  glowEffect?: boolean
}

const props = withDefaults(defineProps<Props>(), {
  modelValue: 0,
  ariaLabel: 'Tabs',
  size: 'md',
  variant: 'underline',
  alignment: 'start',
  fullWidth: false,
  vertical: false,
  showIndicator: true,
  glowEffect: true
})

const emit = defineEmits<{
  (e: 'update:modelValue', value: number): void
  (e: 'change', value: number): void
}>()

const selectedIndex = ref(props.modelValue)

watch(() => props.modelValue, (newVal) => {
  selectedIndex.value = newVal
})

const handleChange = (index: number) => {
  selectedIndex.value = index
  emit('update:modelValue', index)
  emit('change', index)
}

const containerClass = computed(() => {
  const classes = []
  if (props.vertical) {
    classes.push('flex gap-4')
  }
  return classes.join(' ')
})

const tabListClass = computed(() => {
  const classes = ['flex']
  
  if (props.vertical) {
    classes.push('flex-col', 'min-w-[200px]')
  } else {
    if (props.alignment === 'center') classes.push('justify-center')
    else if (props.alignment === 'end') classes.push('justify-end')
    else if (props.alignment === 'stretch') classes.push('justify-stretch')
    
    if (props.variant === 'underline' || props.variant === 'ghost') {
      classes.push('border-b border-border-dark')
    } else if (props.variant === 'enclosed') {
      classes.push('border-b border-border-dark bg-surface-dark rounded-t-xl')
    }
  }
  
  if (props.variant === 'pills') {
    classes.push('gap-2 p-1 bg-surface-dark rounded-xl')
  } else if (props.variant === 'enclosed') {
    classes.push('gap-0')
  } else {
    classes.push('gap-1')
  }
  
  return classes.join(' ')
})

const getTabButtonClass = (selected: boolean) => {
  const classes = ['relative transition-all duration-200 font-medium']
  
  const sizeClasses = {
    sm: 'px-3 py-1.5 text-sm',
    md: 'px-4 py-2 text-base',
    lg: 'px-6 py-3 text-lg'
  }
  classes.push(sizeClasses[props.size])
  
  if (props.fullWidth) {
    classes.push('flex-1')
  }
  
  if (props.variant === 'pills') {
    classes.push('rounded-lg')
    if (selected) {
      classes.push('bg-primary text-white')
      if (props.glowEffect) {
        classes.push('shadow-glow')
      }
    } else {
      classes.push('text-text-dim hover:text-white hover:bg-surface-lighter')
    }
  } else if (props.variant === 'enclosed') {
    classes.push('border-x border-t border-transparent')
    if (selected) {
      classes.push('bg-background-dark border-border-dark text-white rounded-t-lg -mb-px')
    } else {
      classes.push('text-text-dim hover:text-white hover:bg-surface-lighter')
    }
  } else if (props.variant === 'ghost') {
    classes.push('rounded-lg')
    if (selected) {
      classes.push('bg-surface-lighter text-white')
    } else {
      classes.push('text-text-dim hover:text-white hover:bg-surface-dark')
    }
  } else {
    classes.push('-mb-px')
    if (selected) {
      classes.push('text-white')
    } else {
      classes.push('text-text-dim hover:text-white')
    }
  }
  
  classes.push('focus:outline-none focus-visible:ring-2 focus-visible:ring-primary focus-visible:ring-offset-2 focus-visible:ring-offset-background-dark')
  
  return classes.join(' ')
}

const indicatorClass = computed(() => {
  const classes = ['absolute bottom-0 left-0 right-0 transition-all duration-200']
  
  if (props.variant === 'underline') {
    classes.push('h-0.5 bg-primary')
    if (props.glowEffect) {
      classes.push('shadow-[0_0_10px_rgba(166,13,242,0.5)]')
    }
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

const tabPanelClass = computed(() => {
  const classes = []
  
  if (props.variant === 'enclosed') {
    classes.push('mt-0 p-4 bg-background-dark border border-border-dark rounded-b-xl border-t-0')
  } else {
    classes.push('mt-4')
  }
  
  classes.push('focus:outline-none focus-visible:ring-2 focus-visible:ring-primary focus-visible:ring-offset-2 focus-visible:ring-offset-background-dark')
  
  return classes.join(' ')
})
</script>
