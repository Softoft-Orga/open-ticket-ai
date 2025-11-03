<template>
  <section class="space-y-6">
    <div class="flex flex-col gap-4 md:flex-row md:items-center md:justify-between">
      <TagFilter
        :selected="selectedTag"
        :tags="allTags"
        @update:selected="onTagSelected"
      />
      <SearchBox :value="query" @update:value="value => query = value" />
    </div>

    <div v-if="registry.isLoading.value" class="rounded-lg border border-[color:var(--vp-c-divider)] bg-[color:var(--vp-c-bg-soft)] p-6 text-[color:var(--vp-c-text-2)]">
      Loading examples…
    </div>
    <div v-else-if="registry.error.value" class="rounded-lg border border-[color:var(--vp-c-danger-1,#f87171)] bg-[color:var(--vp-c-bg-soft)] p-6 text-[color:var(--vp-c-danger-1,#f87171)]">
      {{ registry.error.value?.message ?? 'Unable to load examples' }}
    </div>
    <ExampleList v-else :examples="filteredExamples" />
  </section>
</template>

<script lang="ts" setup>
import {computed, ref, watch} from 'vue'
import {useRegistry} from '../../composables/useRegistry'
import TagFilter from './TagFilter.vue'
import SearchBox from './SearchBox.vue'
import ExampleList from './ExampleList.vue'

const registry = useRegistry()

const selectedTag = ref('All')
const query = ref('')

const allTags = computed(() => registry.allTags.value)

const filteredExamples = computed(() => {
  const examples = registry.examples.value
  const normalizedQuery = query.value.trim().toLowerCase()

  return examples.filter(example => {
    const matchesTag = selectedTag.value === 'All' || example.tags.includes(selectedTag.value)
    const matchesQuery = !normalizedQuery || example.name.toLowerCase().includes(normalizedQuery)
    return matchesTag && matchesQuery
  })
})

function onTagSelected(tag: string) {
  selectedTag.value = tag
}

watch(registry.examples, () => {
  if (selectedTag.value !== 'All') {
    const hasTag = registry.allTags.value.includes(selectedTag.value)
    if (!hasTag) {
      selectedTag.value = 'All'
    }
  }
})
</script>
