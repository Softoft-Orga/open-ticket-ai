<template>
  <section class="space-y-4">
    <div v-if="registry.isLoading.value" class="rounded-lg border border-[color:var(--vp-c-divider)] bg-[color:var(--vp-c-bg-soft)] p-4 text-sm text-[color:var(--vp-c-text-2)]">
      Loading example…
    </div>
    <div v-else-if="registry.error.value" class="rounded-lg border border-[color:var(--vp-c-danger-1,#f87171)] bg-[color:var(--vp-c-bg-soft)] p-4 text-sm text-[color:var(--vp-c-danger-1,#f87171)]">
      {{ registry.error.value?.message ?? 'Unable to load example.' }}
    </div>
    <Card v-else-if="example" class="space-y-4">
      <template #header>
        <h2 class="m-0 text-2xl font-semibold text-[color:var(--vp-c-text-1)]">{{ example.name }}</h2>
      </template>
      <div class="space-y-4">
        <MarkdownFromString :markdown="example.md_details" />
        <ExampleViewer :file="example.path" />
      </div>
    </Card>
    <div v-else class="rounded-lg border border-[color:var(--vp-c-divider)] bg-[color:var(--vp-c-bg-soft)] p-4 text-sm text-[color:var(--vp-c-text-2)]">
      Could not find the requested example.
    </div>
  </section>
</template>

<script lang="ts" setup>
import {computed} from 'vue'
import Card from '../core/basic/Card.vue'
import MarkdownFromString from './MarkdownFromString.vue'
import ExampleViewer from './ExampleViewer.vue'
import {useConfigExamplesRegistry} from '../../composables/useConfigExamplesRegistry'

const props = defineProps<{ slug: string }>()

const registry = useConfigExamplesRegistry()

const example = computed(() => registry.findBySlug(props.slug) ?? null)
</script>
