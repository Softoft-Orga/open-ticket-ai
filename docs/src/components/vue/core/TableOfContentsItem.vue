<template>
  <li>
    <div class="flex items-start">
      <!-- Collapse button (only if collapsible and has children) -->
      <button
        v-if="collapsible && hasChildren"
        :class="[
          'flex-shrink-0 w-4 h-4 mr-1 mt-1.5 text-text-dim hover:text-primary transition-colors',
          'focus:outline-none focus-visible:ring-2 focus-visible:ring-primary rounded'
        ]"
        :aria-expanded="isExpanded"
        type="button"
        @click="toggleExpanded"
      >
        <svg
          :class="['w-full h-full transition-transform duration-200', isExpanded ? 'rotate-90' : '']"
          fill="none"
          viewBox="0 0 24 24"
          stroke="currentColor"
        >
          <path
            stroke-linecap="round"
            stroke-linejoin="round"
            stroke-width="2"
            d="M9 5l7 7-7 7"
          />
        </svg>
      </button>
      <!-- Spacer when no collapse button -->
      <span
        v-else-if="collapsible"
        class="flex-shrink-0 w-4 mr-1"
      />
      
      <!-- Link -->
      <a
        :href="`#${item.id}`"
        :class="linkClasses"
        @click.prevent="handleNavigate"
      >
        {{ item.text }}
      </a>
    </div>
    
    <!-- Nested children -->
    <transition
      name="toc-collapse"
      @enter="onEnter"
      @after-enter="onAfterEnter"
      @leave="onLeave"
    >
      <ul
        v-if="hasChildren && isExpanded"
        :class="['mt-1 space-y-1', showLine && 'border-l-2 border-border-dark ml-3']"
      >
        <TableOfContentsItem
          v-for="child in item.children"
          :key="child.id"
          :item="child"
          :active-id="activeId"
          :show-line="showLine"
          :collapsible="collapsible"
          :level="level + 1"
          @navigate="$emit('navigate', $event)"
        />
      </ul>
    </transition>
  </li>
</template>

<script lang="ts" setup>
import { ref, computed } from 'vue'
import type { HeadingNode } from './TableOfContents.vue'

interface Props {
  item: HeadingNode
  activeId: string
  showLine: boolean
  collapsible: boolean
  level: number
}

const props = defineProps<Props>()

/* eslint-disable no-unused-vars */
const emit = defineEmits<{
  (e: 'navigate', id: string): void
}>()
/* eslint-enable no-unused-vars */

const isExpanded = ref(true)

const hasChildren = computed(() => {
  return props.item.children && props.item.children.length > 0
})

const isActive = computed(() => {
  return props.activeId === props.item.id
})

const isParentOfActive = computed(() => {
  const checkChildren = (node: HeadingNode): boolean => {
    if (node.id === props.activeId) return true
    if (node.children) {
      return node.children.some(checkChildren)
    }
    return false
  }
  return hasChildren.value && props.item.children!.some(checkChildren)
})

const linkClasses = computed(() => {
  const base = [
    'block py-1 text-sm transition-all duration-200',
    'relative group flex-1'
  ]
  
  const indent = props.showLine ? 'pl-4' : `pl-${Math.min(props.level * 4, 12)}`
  
  const stateClasses = isActive.value
    ? [
        'text-primary font-medium',
        props.showLine && 'border-l-2 border-primary -ml-[2px]'
      ]
    : isParentOfActive.value
    ? [
        'text-secondary',
        props.showLine && 'border-l-2 border-transparent -ml-[2px]'
      ]
    : [
        'text-text-dim',
        'hover:text-white hover:underline hover:decoration-primary/50',
        props.showLine && 'border-l-2 border-transparent hover:border-primary/30 -ml-[2px]'
      ]
  
  return [...base, indent, ...stateClasses].filter(Boolean)
})

const toggleExpanded = () => {
  isExpanded.value = !isExpanded.value
}

const handleNavigate = () => {
  emit('navigate', props.item.id)
}

// Animation handlers for collapse/expand
const onEnter = (el: Element) => {
  const element = el as HTMLElement
  element.style.height = '0'
  element.style.opacity = '0'
  element.offsetHeight // Force reflow
  element.style.height = element.scrollHeight + 'px'
  element.style.opacity = '1'
}

const onAfterEnter = (el: Element) => {
  const element = el as HTMLElement
  element.style.height = 'auto'
}

const onLeave = (el: Element) => {
  const element = el as HTMLElement
  element.style.height = element.scrollHeight + 'px'
  element.offsetHeight // Force reflow
  element.style.height = '0'
  element.style.opacity = '0'
}
</script>

<style scoped>
.toc-collapse-enter-active,
.toc-collapse-leave-active {
  transition: height 0.3s ease-in-out, opacity 0.3s ease-in-out;
  overflow: hidden;
}

.toc-collapse-enter-from,
.toc-collapse-leave-to {
  height: 0;
  opacity: 0;
}
</style>
