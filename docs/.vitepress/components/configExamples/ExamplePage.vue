<template>
  <section class="space-y-6">
    <div v-if="registry.isLoading.value" class="rounded-lg border border-[color:var(--vp-c-divider)] bg-[color:var(--vp-c-bg-soft)] p-6 text-[color:var(--vp-c-text-2)]">
      Loading example…
    </div>
    <div v-else-if="registry.error.value" class="rounded-lg border border-[color:var(--vp-c-danger-1,#f87171)] bg-[color:var(--vp-c-bg-soft)] p-6 text-[color:var(--vp-c-danger-1,#f87171)]">
      {{ registry.error.value?.message ?? 'Unable to load example.' }}
    </div>
    <div v-else-if="example" class="space-y-6">
      <header class="space-y-4">
        <h1 class="m-0 text-3xl font-bold text-[color:var(--vp-c-text-1)]">{{ example.name }}</h1>
        <MarkdownFromString :markdown="example.description" />
        <TagBadges v-if="example.tags.length" :tags="example.tags" />
      </header>
      <ExampleViewer :file="example.path" />
    </div>
    <div v-else class="rounded-lg border border-[color:var(--vp-c-divider)] bg-[color:var(--vp-c-bg-soft)] p-6 text-[color:var(--vp-c-text-2)]">
      Could not find this example. Check the slug or return to the gallery.
    </div>
  </section>
</template>

<script lang="ts" setup>
import {computed} from 'vue'
import MarkdownFromString from './MarkdownFromString.vue'
import TagBadges from './TagBadges.vue'
import ExampleViewer from './ExampleViewer.vue'
import {useConfigExamplesRegistry} from '../../composables/useConfigExamplesRegistry'

const props = defineProps<{ slug: string }>()

const registry = useConfigExamplesRegistry()

const example = computed(() => registry.findBySlug(props.slug) ?? null)
</script>
