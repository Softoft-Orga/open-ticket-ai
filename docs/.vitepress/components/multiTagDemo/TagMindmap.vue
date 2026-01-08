<script setup lang="ts">
import { computed, onBeforeUnmount, onMounted, ref, watch } from 'vue'
import { Transformer } from 'markmap-lib'
import { Markmap } from 'markmap-view'
import { useYamlTagTree, type TagNode } from '../../composables/useYamlTagTree'
import tagYaml from './tags.yml?raw'

const { tree, error } = useYamlTagTree(tagYaml)
const svgRef = ref<SVGSVGElement | null>(null)
const isMounted = ref(false)
const transformer = new Transformer()
let markmapInstance: Markmap | null = null

const hasData = computed(() => !error.value && tree.value.length > 0)

const nodeLabel = (key: string) =>
  `**${key}**`

const buildMarkdown = (nodes: TagNode[], depth = 0): string =>
  nodes
    .map(node => {
      const children = node.children.length ? `\n${buildMarkdown(node.children, depth + 1)}` : ''
      return `${'  '.repeat(depth)}- ${nodeLabel(node.key)}${children}`
    })
    .join('\n')

const renderMindmap = () => {
  if (!isMounted.value || !svgRef.value || !hasData.value) return
  const markdown = buildMarkdown(tree.value)
  const { root } = transformer.transform(markdown)

  if (!markmapInstance) {
    markmapInstance = Markmap.create(svgRef.value, {
      color: () => '#38bdf8',
      initialExpandLevel: 3
    })
  }

  markmapInstance.setData(root)
  markmapInstance.fit()
}

onMounted(() => {
  isMounted.value = true
  renderMindmap()
})

watch(tree, renderMindmap)

onBeforeUnmount(() => {
  markmapInstance?.destroy?.()
  markmapInstance = null
})
</script>

<template>
  <div class="flex flex-col gap-6">
    <div class="flex flex-wrap items-start justify-between gap-4">
      <div class="space-y-1">
        <div class="text-xs font-bold uppercase tracking-[0.18em] text-slate-400">
          tags.yml explorer
        </div>
        <div class="text-2xl font-extrabold text-white">
          Interactive Tag Mindmap
        </div>
        <p class="max-w-4xl text-sm text-slate-300">
          Convert the YAML taxonomy into a zoomable, pannable mindmap. Click nodes to collapse or expand
          branches and drag to explore the tree.
        </p>
      </div>

      <div class="flex items-center gap-2">
        <button
          :disabled="!hasData"
          class="inline-flex items-center rounded-xl border border-slate-600 bg-slate-800/80 px-4 py-2 text-sm font-semibold text-slate-100 shadow-sm transition hover:bg-slate-700/80 disabled:cursor-not-allowed disabled:opacity-50"
          type="button"
          @click="renderMindmap"
        >
          Refocus to fit
        </button>
      </div>
    </div>

    <div
      v-if="error"
      class="rounded-xl border border-red-600 bg-red-950/80 px-4 py-3 text-sm font-semibold text-red-50"
    >
      {{ error }}
    </div>

    <div v-else class="flex flex-col gap-4">
      <div class="rounded-2xl border border-slate-700 bg-slate-900/70 p-4 text-sm text-slate-100 shadow">
        <div class="mb-2 text-sm font-semibold text-slate-50">
          How to explore
        </div>
        <ul class="grid gap-1.5 pl-4 text-xs text-slate-300 list-disc">
          <li>Click a node to expand or collapse its branch.</li>
          <li>Scroll to zoom and drag to pan around the map.</li>
          <li>Use the refocus button to re-center if you get lost.</li>
        </ul>
      </div>

      <div
        class="relative h-[80vh] min-h-[720px] w-full overflow-hidden rounded-3xl border border-slate-700 bg-slate-950 shadow-2xl"
      >
        <div
          v-if="!hasData"
          class="absolute inset-0 flex items-center justify-center bg-slate-950/80 text-xs font-semibold uppercase tracking-[0.18em] text-slate-400 backdrop-blur"
        >
          Loading tag hierarchy…
        </div>
        <svg
          ref="svgRef"
          aria-label="Tag mindmap"
          class="h-full w-full"
        />
      </div>
    </div>
  </div>
</template>

<style scoped>
:deep(svg[aria-label='Tag mindmap']) {
  --mm-font-color: #ffffff;
}

:deep(.markmap-node text) {
  fill: #ffffff !important;
  font-size: 1.2rem;
  font-weight: 400;
}

:deep(.markmap-node tspan.markmap-strong) {
  font-weight: 800 !important;
}

:deep(.markmap-node circle) {
  r: 12;
  fill: #38bdf8;
  stroke: #020617;
  stroke-width: 2.2;
}

:deep(.markmap-link) {
  stroke: #1f2937;
  stroke-width: 2;
}
</style>
