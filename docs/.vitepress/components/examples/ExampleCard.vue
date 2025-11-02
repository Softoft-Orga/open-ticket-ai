<template>
  <Card class="h-full">
    <template #header>
      <h2 class="m-0 text-2xl font-semibold text-[var(--vp-c-text-1)]">
        {{ example.name }}
      </h2>
    </template>

    <div class="space-y-4">
      <MarkdownFromString :markdown="example.description" />
      <TagBadges v-if="example.tags.length" :tags="example.tags" />
      <ExampleViewer :file="example.path" />
    </div>

    <template #footer>
      <div class="flex justify-end">
        <a
          :href="exampleLink"
          class="text-sm font-medium text-[var(--vp-c-brand-1)] transition hover:text-[var(--vp-c-brand-2)]"
        >
          Open full page →
        </a>
      </div>
    </template>
  </Card>
</template>

<script lang="ts" setup>
import {computed} from 'vue'
import {useData} from 'vitepress'
import Card from '../core/basic/Card.vue'
import MarkdownFromString from './MarkdownFromString.vue'
import TagBadges from './TagBadges.vue'
import ExampleViewer from './ExampleViewer.vue'
import type {ExampleMeta} from '../../composables/useRegistry'

const props = defineProps<{ example: ExampleMeta }>()

const {site} = useData()

const exampleLink = computed(() => {
  const base = site.value?.base ?? '/'
  const normalizedBase = base.endsWith('/') ? base : `${base}/`
  return `${normalizedBase}examples/${props.example.slug}.html`
})
</script>
