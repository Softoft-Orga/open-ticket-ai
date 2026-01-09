<template>
  <nav class="sticky top-20 space-y-2">
    <h3 class="mb-4 text-sm font-bold uppercase tracking-wider text-gray-400">On This Page</h3>
    <ul class="space-y-2 border-l-2 border-surface-lighter">
      <li v-for="heading in headings" :key="heading.id">
        <a
          :href="`#${heading.id}`"
          @click.prevent="scrollToHeading(heading.id)"
          :class="[
            'block border-l-2 py-1 text-sm transition-all',
            activeId === heading.id
              ? 'border-primary text-primary-light -ml-[2px]'
              : 'border-transparent text-text-dim hover:text-white -ml-[2px]',
            heading.level === 3 ? 'pl-4' : 'pl-8'
          ]"
        >
          {{ heading.text }}
        </a>
      </li>
    </ul>
  </nav>
</template>

<script lang="ts" setup>
import { ref, onMounted, onUnmounted } from 'vue'

interface Heading {
  id: string
  text: string
  level: number
}

interface Props {
  headings?: Heading[]
}

const props = withDefaults(defineProps<Props>(), {
  headings: () => []
})

const activeId = ref<string>('')

const scrollToHeading = (id: string) => {
  const element = document.getElementById(id)
  if (element) {
    element.scrollIntoView({ behavior: 'smooth', block: 'start' })
    activeId.value = id
  }
}

const updateActiveId = () => {
  const headingElements = props.headings
    .map(h => ({
      id: h.id,
      element: document.getElementById(h.id)
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
