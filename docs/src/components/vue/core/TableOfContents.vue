<template>
  <nav class="sticky top-20 space-y-2">
    <h3 class="mb-4 text-sm font-bold uppercase tracking-wider text-text-dim">On This Page</h3>
    <ul :class="['space-y-1', showLine && 'border-l-2 border-border-dark']">
      <TableOfContentsItem
        v-for="item in treeStructure"
        :key="item.id"
        :item="item"
        :active-id="activeId"
        :show-line="showLine"
        :collapsible="collapsible"
        :level="0"
        @navigate="scrollToHeading"
      />
    </ul>
  </nav>
</template>

<script lang="ts" setup>
import { ref, computed, onMounted, onUnmounted } from 'vue'
import TableOfContentsItem from './TableOfContentsItem.vue'

export interface Heading {
  id: string
  text: string
  level: number
}

export interface HeadingNode extends Heading {
  children?: HeadingNode[]
}

interface Props {
  headings?: Heading[]
  showLine?: boolean
  collapsible?: boolean
}

const props = withDefaults(defineProps<Props>(), {
  headings: () => [],
  showLine: true,
  collapsible: false
})

const activeId = ref<string>('')

// Convert flat heading list to tree structure
const treeStructure = computed<HeadingNode[]>(() => {
  const result: HeadingNode[] = []
  const stack: HeadingNode[] = []

  for (const heading of props.headings) {
    const node: HeadingNode = { ...heading, children: [] }

    // Find the appropriate parent
    while (stack.length > 0 && stack[stack.length - 1].level >= heading.level) {
      stack.pop()
    }

    if (stack.length === 0) {
      result.push(node)
    } else {
      const parent = stack[stack.length - 1]
      if (!parent.children) {
        parent.children = []
      }
      parent.children.push(node)
    }

    stack.push(node)
  }

  return result
})

const scrollToHeading = (id: string) => {
  const element = document.getElementById(id)
  if (element) {
    element.scrollIntoView({ behavior: 'smooth', block: 'start' })
    activeId.value = id
  }
}

const getAllHeadingIds = (nodes: HeadingNode[]): string[] => {
  const ids: string[] = []
  for (const node of nodes) {
    ids.push(node.id)
    if (node.children) {
      ids.push(...getAllHeadingIds(node.children))
    }
  }
  return ids
}

const updateActiveId = () => {
  const allIds = getAllHeadingIds(treeStructure.value)
  const headingElements = allIds
    .map(id => ({
      id,
      element: document.getElementById(id)
    }))
    .filter(h => h.element)

  for (let i = headingElements.length - 1; i >= 0; i--) {
    const { id, element } = headingElements[i]
    if (element) {
      const rect = element.getBoundingClientRect()
      if (rect.top <= 150) {
        activeId.value = id
        return
      }
    }
  }
  
  if (headingElements.length > 0) {
    activeId.value = headingElements[0].id
  }
}

onMounted(() => {
  window.addEventListener('scroll', updateActiveId)
  updateActiveId()
})

onUnmounted(() => {
  window.removeEventListener('scroll', updateActiveId)
})
</script>
