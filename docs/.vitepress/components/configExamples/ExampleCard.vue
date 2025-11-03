<template>
  <Card class="h-full">
    <template #header>
      <h2 class="m-0 text-2xl font-semibold text-[var(--vp-c-text-1)]">
        {{ example.name }}
      </h2>
    </template>

    <div class="space-y-4 min-h-16">
      <MarkdownFromString :markdown="example.md_description" />
    </div>

    <template #footer>
      <div class="flex items-center justify-between gap-3">
        <div class="flex items-center gap-2">
          <TagBadges :tags="visibleTags" />
          <span v-if="extraCount>0" class="text-xs text-[color:var(--vp-c-text-3)]">+{{ extraCount }}</span>
        </div>
        <a
          :href="exampleLink"
          class="text-sm font-medium text-[var(--vp-c-brand-1)] transition hover:text-[var(--vp-c-brand-2)]"
        >
          Go to full example!
        </a>
      </div>
    </template>
  </Card>
</template>

<script lang="ts" setup>
import Card from '../core/basic/Card.vue'
import MarkdownFromString from './MarkdownFromString.vue'
import TagBadges from './TagBadges.vue'
import type { ExampleMeta } from '../../composables/useConfigExamplesRegistry'

const { example, exampleLink } = defineProps<{ example: ExampleMeta; exampleLink: string }>()

const visibleTags = (example.tags || []).slice(0, 3)
const extraCount = Math.max(0, (example.tags || []).length - visibleTags.length)
</script>
