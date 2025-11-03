<template>
    <section class="space-y-6">
        <div class="flex flex-col gap-4 md:flex-row md:items-center md:justify-between">
            <TagFilter :selected="selectedTag" :tags="allTags" @update:selected="onTagSelected"/>
            <SearchBox :value="query" @update:value="v => query = v"/>
        </div>

        <div v-if="registry.isLoading.value"
             class="rounded-lg border border-[color:var(--vp-c-divider)] bg-[color:var(--vp-c-bg-soft)] p-6 text-[color:var(--vp-c-text-2)]">
            Loading examples…
        </div>
        <div v-else-if="registry.error.value"
             class="rounded-lg border border-[color:var(--vp-c-danger-1,#f87171)] bg-[color:var(--vp-c-bg-soft)] p-6 text-[color:var(--vp-c-danger-1,#f87171)]">
            {{ registry.error.value?.message ?? 'Unable to load examples' }}
        </div>

        <div @click.capture="onCardAreaClick">
            <ExampleGrid :examples="filteredExamples"/>
        </div>
    </section>
    <section class="mt-5 pt-2 border-t border-t-gray-600 border-solid">
        <h2 class="text-3xl font-semibold leading-tight my-4">Details</h2>
        <div v-for="example in filteredExamples" :id="example.slug" :key="example.slug || example.name" class="my-2">
            <InlineExample :slug="example.slug"/>
        </div>
    </section>
</template>

<script lang="ts" setup>
import {computed, nextTick, onBeforeUnmount, onMounted, ref, watch} from 'vue'
import {useConfigExamplesRegistry} from '../../composables/useConfigExamplesRegistry'
import TagFilter from './TagFilter.vue'
import SearchBox from './SearchBox.vue'
import ExampleGrid from './ExampleGrid.vue'
import InlineExample from "./InlineExample.vue";

const registry = useConfigExamplesRegistry()

const selectedTag = ref('All')
const query = ref('')

const allTags = computed(() => registry.allTags.value)

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
