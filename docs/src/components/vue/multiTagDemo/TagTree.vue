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
    <div class="collapsible">
        <details ref="detailsRef">
            <summary class="summary">
                <div class="summary-text">
                    <span class="summary-title">Browse all tags</span>
                    <span class="summary-sub">Full YAML list, collapsed by default</span>
                </div>
                <div class="summary-actions">
                    <span class="count">{{ totalTags }} tags</span>
                    <button type="button" class="open-button" @click.stop.prevent="openList">Expand</button>
                </div>
            </summary>
            <div class="panel">
                <YamlTree :source="tagYaml" />
            </div>
        </details>
    </div>
</template>

<style scoped>
.collapsible {
    border: 1px solid var(--vp-c-border);
    border-radius: 1rem;
    background: var(--vp-c-bg);
    box-shadow: var(--vp-shadow-2);
}

details {
    border-radius: 1rem;
    overflow: hidden;
}

.summary {
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 1rem;
    padding: 1rem 1.25rem;
    cursor: pointer;
    background: var(--vp-c-bg-soft);
    list-style: none;
}

.summary::-webkit-details-marker {
    display: none;
}

.summary-text {
    display: flex;
    flex-direction: column;
    gap: 0.1rem;
}

.summary-title {
    font-weight: 800;
    color: var(--vp-c-text-1);
}

.summary-sub {
    color: var(--vp-c-text-2);
    font-size: 0.9rem;
}

.summary-actions {
    display: flex;
    align-items: center;
    gap: 0.75rem;
}

.count {
    padding: 0.3rem 0.6rem;
    border-radius: 999px;
    background: var(--vp-c-bg);
    border: 1px solid var(--vp-c-border);
    font-weight: 700;
}

.open-button {
    border: 1px solid var(--vp-c-border);
    background: var(--vp-c-brand-soft);
    color: var(--vp-c-text-1);
    border-radius: 0.65rem;
    padding: 0.45rem 0.8rem;
    font-weight: 700;
    cursor: pointer;
}

.panel {
    padding: 1rem 1.25rem 1.5rem;
    background: var(--vp-c-bg);
}

@media (max-width: 640px) {
    .summary {
        flex-direction: column;
        align-items: flex-start;
    }

    .summary-actions {
        width: 100%;
        justify-content: space-between;
    }
}
</style>
