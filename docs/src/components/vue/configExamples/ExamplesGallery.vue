<template>
  <section class="space-y-6">
    <div class="flex flex-col gap-4 md:flex-row md:items-center md:justify-between">
      <!-- Tag Filter -->
      <div class="flex flex-wrap gap-2">
        <button
          v-for="tag in tagsWithAll"
          :key="tag"
          :class="buttonClass(tag)"
          type="button"
          @click="() => onTagSelected(tag)"
        >
          {{ tag }}
        </button>
      </div>
      
      <!-- Search Box -->
      <label class="block w-full max-w-sm">
        <span class="sr-only">Search examples</span>
        <input
          :value="query"
          class="w-full h-12 px-4 text-base rounded-xl bg-surface-dark border border-primary/40 text-white placeholder:text-text-dim hover:border-primary/60 hover:shadow-[0_0_15px_rgba(166,13,242,0.2)] focus:ring-2 focus:ring-primary/50 focus:border-primary focus:outline-none active:border-primary active:ring-primary/60 shadow-sm transition-colors duration-200"
          placeholder="Search examples…"
          type="text"
          @input="event => query = (event.target as HTMLInputElement).value"
        >
      </label>
    </div>

    <div
      v-if="registry.isLoading.value"
      class="rounded-lg border border-[color:var(--vp-c-divider)] bg-[color:var(--vp-c-bg-soft)] p-6 text-[color:var(--vp-c-text-2)]"
    >
      Loading examples…
    </div>
    <div
      v-else-if="registry.error.value"
      class="rounded-lg border border-[color:var(--vp-c-danger-1,#f87171)] bg-[color:var(--vp-c-bg-soft)] p-6 text-[color:var(--vp-c-danger-1,#f87171)]"
    >
      {{ registry.error.value?.message ?? 'Unable to load examples' }}
    </div>

    <!-- Example Grid -->
    <div @click.capture="onCardAreaClick">
      <div class="grid gap-6 md:grid-cols-2">
        <Card
          v-for="example in filteredExamples"
          :key="example.slug ?? example.name"
          class="h-full"
        >
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
                <!-- Tag Badges -->
                <div class="flex flex-wrap gap-2">
                  <Badge
                    v-for="tag in getVisibleTags(example)"
                    :key="tag"
                    class="text-xs"
                  >
                    {{ tag }}
                  </Badge>
                </div>
                <span
                  v-if="getExtraCount(example) > 0"
                  class="text-xs text-[color:var(--vp-c-text-3)]"
                >+{{ getExtraCount(example) }}</span>
              </div>
              <a
                :href="'#' + (example.slug ?? example.name)"
                class="text-sm font-medium text-[var(--vp-c-brand-1)] transition hover:text-[var(--vp-c-brand-2)]"
              >
                Go to full example!
              </a>
            </div>
          </template>
        </Card>
        <p
          v-if="!filteredExamples.length"
          class="col-span-full rounded-lg border border-[var(--vp-c-divider)] bg-[var(--vp-c-bg-soft)] p-6 text-center text-[var(--vp-c-text-2)]"
        >
          No examples match your filters yet. Try clearing the search or picking a different tag.
        </p>
      </div>
    </div>
  </section>
  <section class="mt-5 pt-2 border-t border-t-gray-600 border-solid">
    <h2 class="text-3xl font-semibold leading-tight my-4">
      Details
    </h2>
    <div
      v-for="example in filteredExamples"
      :id="example.slug"
      :key="example.slug || example.name"
      class="my-2"
    >
      <InlineExample :slug="example.slug" />
    </div>
  </section>
</template>

<script lang="ts" setup>
import {computed, nextTick, onBeforeUnmount, onMounted, ref, watch} from 'vue'
import {useConfigExamplesRegistry} from '../../../composables/useConfigExamplesRegistry'
import type {ExampleMeta} from '../../../composables/useConfigExamplesRegistry'
import InlineExample from "./InlineExample.vue"
import Card from '../core/basic/Card.vue'
import Badge from '../core/basic/Badge.vue'
import MarkdownFromString from './MarkdownFromString.vue'

const registry = useConfigExamplesRegistry()

const selectedTag = ref('All')
const query = ref('')

const allTags = computed(() => registry.allTags.value)
const tagsWithAll = computed(() => ['All', ...allTags.value])

function hasTag(e: any, tag: string) {
    if (tag === 'All') return true
    const tags: string[] = Array.isArray(e.tags) ? e.tags : []
    return tags.map(t => String(t).toLowerCase()).includes(tag.toLowerCase())
}

function matchesQuery(e: any, q: string) {
    const s = q.trim().toLowerCase()
    if (!s) return true
    const fields = [
        e.name, e.title, e.slug,
        e.description, e.descriptionMd
    ].map(v => (v ?? '').toString().toLowerCase())
    return fields.some(f => f.includes(s))
}

const filteredExamples = computed(() => {
    const list = Array.isArray(registry.examples.value) ? registry.examples.value : []
    return list.filter(e => hasTag(e, selectedTag.value) && matchesQuery(e, query.value))
})

function onTagSelected(tag: string) {
    selectedTag.value = tag
}

function buttonClass(tag: string) {
  const isActive = tag === selectedTag.value
  return [
    'rounded-full border px-4 py-1 text-xs font-medium transition focus:outline-none focus-visible:ring-2 focus-visible:ring-[color:var(--vp-c-brand-1)]',
    isActive
      ? 'bg-[color:var(--vp-c-brand-1)] text-white border-transparent shadow-sm'
      : 'bg-[color:var(--vp-c-bg-soft)] text-[color:var(--vp-c-text-2)] border-[color:var(--vp-c-divider)] hover:text-[color:var(--vp-c-text-1)]'
  ]
}

function getVisibleTags(example: ExampleMeta) {
  return (example.tags || []).slice(0, 3)
}

function getExtraCount(example: ExampleMeta) {
  const visibleTags = (example.tags || []).slice(0, 3)
  return Math.max(0, (example.tags || []).length - visibleTags.length)
}

async function scrollToHash() {
    const id = decodeURIComponent(location.hash.replace('#', ''))
    if (!id) return
    await nextTick()
    document.getElementById(id)?.scrollIntoView({behavior: 'smooth', block: 'start'})
}

function onCardAreaClick(e: MouseEvent) {
    const a = (e.target as HTMLElement).closest('a') as HTMLAnchorElement | null
    if (!a) return
    const href = a.getAttribute('href') || ''
    if (!href.startsWith('#')) return
    e.preventDefault()
    history.pushState(null, '', href)
    void scrollToHash()
}

function onHashChange() {
    void scrollToHash()
}

watch(filteredExamples, () => {
    if (location.hash) void scrollToHash()
})

watch(registry.examples, () => {
    if (selectedTag.value !== 'All' && !registry.allTags.value.includes(selectedTag.value)) {
        selectedTag.value = 'All'
    }
    if (location.hash) void scrollToHash()
})

onMounted(() => {
    window.addEventListener('hashchange', onHashChange)
    void scrollToHash()
})

onBeforeUnmount(() => {
    window.removeEventListener('hashchange', onHashChange)
})
</script>
