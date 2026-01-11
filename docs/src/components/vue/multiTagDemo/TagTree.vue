<script lang='ts' setup>
import { computed, ref } from 'vue'
import YamlTree from './YamlTree.vue'
import tagYaml from './tags.yml?raw'
import { useYamlTagTree, type TagNode } from '../../../composables/useYamlTagTree'

const detailsRef = ref<HTMLDetailsElement | null>(null)
const { tree } = useYamlTagTree(tagYaml)

const countNodes = (nodes: TagNode[]): number => nodes.reduce((sum, node) => sum + 1 + countNodes(node.children), 0)
const totalTags = computed(() => countNodes(tree.value))

const openList = () => {
    if (detailsRef.value) detailsRef.value.open = true
}
</script>

<template>
  <div class="border border-[var(--vp-c-border)] rounded-2xl bg-[var(--vp-c-bg)] shadow-[var(--vp-shadow-2)]">
    <details
      ref="detailsRef"
      class="rounded-2xl overflow-hidden"
    >
      <summary class="flex items-center justify-between gap-4 p-4 px-5 cursor-pointer bg-[var(--vp-c-bg-soft)] list-none [&::-webkit-details-marker]:hidden max-sm:flex-col max-sm:items-start">
        <div class="flex flex-col gap-0.5">
          <span class="font-extrabold text-[var(--vp-c-text-1)]">Browse all tags</span>
          <span class="text-[var(--vp-c-text-2)] text-sm">Full YAML list, collapsed by default</span>
        </div>
        <div class="flex items-center gap-3 max-sm:w-full max-sm:justify-between">
          <span class="py-1.5 px-2.5 rounded-full bg-[var(--vp-c-bg)] border border-[var(--vp-c-border)] font-bold">{{ totalTags }} tags</span>
          <button
            type="button"
            class="border border-[var(--vp-c-border)] bg-[var(--vp-c-brand-soft)] text-[var(--vp-c-text-1)] rounded-xl py-2 px-3 font-bold cursor-pointer"
            @click.stop.prevent="openList"
          >
            Expand
          </button>
        </div>
      </summary>
      <div class="p-4 px-5 pb-6 bg-[var(--vp-c-bg)]">
        <YamlTree :source="tagYaml" />
      </div>
    </details>
  </div>
</template>
