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

const nodeLabel = (key: string, description?: string) =>
    `${key}${description ? ` — ${description}` : ''}`

const buildMarkdown = (nodes: TagNode[], depth = 0): string =>
    nodes
        .map(node => {
            const children = node.children.length ? `\n${buildMarkdown(node.children, depth + 1)}` : ''
            return `${'  '.repeat(depth)}- ${nodeLabel(node.key, node.description)}${children}`
        })
        .join('\n')

const renderMindmap = () => {
    if (!isMounted.value || !svgRef.value || !hasData.value) return
    const markdown = buildMarkdown(tree.value)
    const { root } = transformer.transform(markdown)
    if (!markmapInstance) {
        markmapInstance = Markmap.create(svgRef.value)
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
    <div class="mindmap-root">
        <div class="mindmap-header">
            <div>
                <div class="eyebrow">tags.yml Explorer</div>
                <div class="title">Interactive Tag Mindmap</div>
                <p class="lede">
                    Convert the YAML taxonomy into a zoomable, pannable mindmap. Click nodes to collapse or expand branches and
                    drag to explore the tree.
                </p>
            </div>
            <div class="header-actions">
                <button type="button" class="secondary" :disabled="!hasData" @click="renderMindmap">Refocus to fit</button>
            </div>
        </div>

        <div v-if="error" class="error">{{ error }}</div>
        <div v-else class="mindmap-shell">
            <div class="mindmap-legend">
                <div class="legend-title">How to explore</div>
                <ul>
                    <li>Click a node to expand or collapse its branch.</li>
                    <li>Scroll to zoom and drag to pan around the map.</li>
                    <li>Use the refocus button to re-center if you get lost.</li>
                </ul>
            </div>
            <div class="mindmap-frame" :class="{ 'has-data': hasData }">
                <div v-if="!hasData" class="placeholder">Loading tag hierarchy…</div>
                <svg ref="svgRef" class="mindmap-canvas" aria-label="Tag mindmap"></svg>
            </div>
        </div>
    </div>
</template>

<style scoped>
.mindmap-root {
    display: flex;
    flex-direction: column;
    gap: 1rem;
}

.mindmap-header {
    display: flex;
    flex-wrap: wrap;
    gap: 1rem;
    justify-content: space-between;
    align-items: flex-start;
}

.eyebrow {
    font-size: 0.75rem;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.08em;
    color: var(--vp-c-text-2);
}

.title {
    font-size: 1.4rem;
    font-weight: 800;
    color: var(--vp-c-text-1);
}

.lede {
    max-width: 72ch;
    color: var(--vp-c-text-2);
    margin: 0.3rem 0 0;
}

.header-actions {
    display: flex;
    gap: 0.5rem;
    align-items: center;
}

button {
    cursor: pointer;
    border-radius: 0.6rem;
    font-weight: 600;
    border: 1px solid transparent;
    transition: all 0.2s ease;
}

.secondary {
    background: var(--vp-c-bg-soft);
    color: var(--vp-c-text-1);
    border-color: var(--vp-c-border);
    padding: 0.55rem 0.9rem;
}

.secondary:disabled {
    opacity: 0.5;
    cursor: not-allowed;
}

.error {
    padding: 0.75rem 1rem;
    border-radius: 0.75rem;
    background: #7f1d1d;
    color: #fef2f2;
    border: 1px solid #b91c1c;
    font-weight: 600;
}

.mindmap-shell {
    display: grid;
    grid-template-columns: minmax(240px, 320px) 1fr;
    gap: 1rem;
    align-items: stretch;
}

.mindmap-legend {
    border: 1px dashed var(--vp-c-border);
    border-radius: 0.9rem;
    background: var(--vp-c-bg-soft);
    padding: 1rem;
    color: var(--vp-c-text-1);
    box-shadow: var(--vp-shadow-1);
}

.legend-title {
    font-weight: 700;
    margin-bottom: 0.35rem;
}

.mindmap-legend ul {
    margin: 0;
    padding-left: 1.1rem;
    color: var(--vp-c-text-2);
    display: grid;
    gap: 0.2rem;
}

.mindmap-frame {
    position: relative;
    border: 1px solid var(--vp-c-border);
    border-radius: 1rem;
    background: radial-gradient(circle at 20% 20%, rgba(99, 102, 241, 0.08), transparent 45%),
        radial-gradient(circle at 80% 30%, rgba(94, 234, 212, 0.08), transparent 40%),
        var(--vp-c-bg);
    min-height: 520px;
    overflow: hidden;
}

.mindmap-frame.has-data {
    box-shadow: var(--vp-shadow-2);
}

.mindmap-canvas {
    width: 100%;
    height: 100%;
}

.placeholder {
    position: absolute;
    inset: 0;
    display: flex;
    align-items: center;
    justify-content: center;
    color: var(--vp-c-text-2);
    font-weight: 600;
    letter-spacing: 0.04em;
    z-index: 1;
    background: linear-gradient(120deg, rgba(15, 23, 42, 0.85), rgba(15, 23, 42, 0.75));
    backdrop-filter: blur(6px);
}

@media (max-width: 960px) {
    .mindmap-shell {
        grid-template-columns: 1fr;
    }
}
</style>
