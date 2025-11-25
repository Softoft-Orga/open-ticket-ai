<script setup lang="ts">
import { computed, ref } from 'vue'
import { useYamlTagTree, type TagNode } from '../../composables/useYamlTagTree'
import tagYaml from './tags.yml?raw'

const { tree, error } = useYamlTagTree(tagYaml)
const focusedPath = ref<string | null>(null)

const findNodeByPath = (nodes: TagNode[], targetPath: string): TagNode | null => {
    for (const node of nodes) {
        if (node.path === targetPath) return node
        const childHit = findNodeByPath(node.children, targetPath)
        if (childHit) return childHit
    }
    return null
}

const focusedNode = computed<TagNode | null>(() => {
    if (!focusedPath.value) return null
    return findNodeByPath(tree.value, focusedPath.value)
})

const breadcrumb = computed<TagNode[]>(() => {
    if (!focusedPath.value) return []
    const parts = focusedPath.value.split('/')
    const crumbs: TagNode[] = []
    let currentPath = ''

    for (const part of parts) {
        currentPath = currentPath ? `${currentPath}/${part}` : part
        const node = findNodeByPath(tree.value, currentPath)
        if (node) crumbs.push(node)
    }

    return crumbs
})

const visibleNodes = computed<TagNode[]>(() => (focusedNode.value ? focusedNode.value.children : tree.value))

const displayIcon = (node: TagNode): string => node.icon ?? node.parentIcon ?? '🧭'

const descendantCount = (node: TagNode): number => node.children.reduce((sum, child) => sum + 1 + descendantCount(child), 0)
const leafCount = (node: TagNode): number => (node.children.length ? node.children.reduce((sum, child) => sum + leafCount(child), 0) : 1)

const focusNode = (path: string | null) => {
    focusedPath.value = path
}

const stepBack = () => {
    if (!focusedPath.value) return
    const parts = focusedPath.value.split('/')
    parts.pop()
    focusedPath.value = parts.length ? parts.join('/') : null
}
</script>

<template>
    <div class="mindmap-root">
        <div class="mindmap-header">
            <div>
                <div class="eyebrow">tags.yml Explorer</div>
                <div class="title">Interactive Tag Mindmap</div>
                <p class="lede">
                    Drill into the taxonomy to see how predicted tags line up with the YAML hierarchy.
                    Click a node to focus its branch and preview its children.
                </p>
            </div>
            <div class="header-actions">
                <button type="button" class="ghost" :disabled="!focusedPath" @click="stepBack">Go up one level</button>
                <button type="button" class="primary" :disabled="!focusedPath" @click="focusNode(null)">Back to roots</button>
            </div>
        </div>

        <div v-if="error" class="error">{{ error }}</div>
        <template v-else>
            <div v-if="breadcrumb.length" class="breadcrumb">
                <span class="crumb-label">Focus:</span>
                <button
                    v-for="crumb in breadcrumb"
                    :key="crumb.path"
                    type="button"
                    class="crumb"
                    @click="focusNode(crumb.path)"
                >
                    <span class="crumb-icon">{{ displayIcon(crumb) }}</span>
                    <span>{{ crumb.key }}</span>
                </button>
            </div>

            <div class="node-grid">
                <div
                    v-for="node in visibleNodes"
                    :key="node.path"
                    class="node-card"
                    :class="{ leaf: !node.children.length }"
                >
                    <div class="node-top">
                        <span class="node-icon">{{ displayIcon(node) }}</span>
                        <div class="node-meta">
                            <div class="node-key">{{ node.key }}</div>
                            <div class="node-path">{{ node.path }}</div>
                        </div>
                    </div>
                    <p class="node-desc" v-if="node.description">{{ node.description }}</p>
                    <div class="badges">
                        <span class="badge">{{ leafCount(node) }} leaf{{ leafCount(node) === 1 ? '' : 's' }}</span>
                        <span class="badge subtle" v-if="node.required">Required</span>
                        <span class="badge subtle" v-if="node.default">Default: {{ node.default }}</span>
                        <span class="badge subtle" v-else-if="node.children.length">Has {{ node.children.length }} direct child{{ node.children.length === 1 ? '' : 'ren' }}</span>
                    </div>

                    <div class="preview" v-if="node.children.length">
                        <div class="preview-label">Next layer</div>
                        <div class="preview-tags">
                            <span v-for="child in node.children.slice(0, 6)" :key="child.path" class="preview-tag">
                                {{ child.key }}
                            </span>
                            <span v-if="node.children.length > 6" class="more">+{{ node.children.length - 6 }} more</span>
                        </div>
                    </div>

                    <div class="node-actions">
                        <button type="button" class="secondary" @click="focusNode(node.path)" :disabled="!node.children.length">
                            Explore branch
                        </button>
                        <span class="descendant-count" :title="'Total descendants (including nested): ' + descendantCount(node)">
                            {{ descendantCount(node) }} total descendants
                        </span>
                    </div>
                </div>
            </div>
        </template>
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

.primary,
.secondary,
.ghost {
    padding: 0.55rem 0.9rem;
}

.primary {
    background: var(--vp-c-brand-1);
    color: #0f172a;
    border-color: var(--vp-c-brand-1);
    box-shadow: var(--vp-shadow-1);
}

.primary:disabled {
    opacity: 0.5;
    cursor: not-allowed;
}

.secondary {
    background: var(--vp-c-bg-soft);
    color: var(--vp-c-text-1);
    border-color: var(--vp-c-border);
}

.secondary:disabled {
    opacity: 0.5;
    cursor: not-allowed;
}

.ghost {
    background: transparent;
    color: var(--vp-c-text-2);
    border-color: var(--vp-c-border);
}

.error {
    padding: 0.75rem 1rem;
    border-radius: 0.75rem;
    background: #7f1d1d;
    color: #fef2f2;
    border: 1px solid #b91c1c;
    font-weight: 600;
}

.breadcrumb {
    display: flex;
    flex-wrap: wrap;
    gap: 0.5rem;
    align-items: center;
    padding: 0.5rem 0.75rem;
    background: var(--vp-c-bg-soft);
    border: 1px dashed var(--vp-c-border);
    border-radius: 0.75rem;
}

.crumb-label {
    font-size: 0.8rem;
    color: var(--vp-c-text-2);
    font-weight: 600;
}

.crumb {
    display: inline-flex;
    align-items: center;
    gap: 0.35rem;
    background: var(--vp-c-bg);
    border: 1px solid var(--vp-c-border);
    color: var(--vp-c-text-1);
    padding: 0.35rem 0.6rem;
    border-radius: 999px;
}

.crumb-icon {
    display: inline-flex;
    align-items: center;
    justify-content: center;
    width: 1.4rem;
    height: 1.4rem;
    background: var(--vp-c-bg-soft);
    border-radius: 999px;
    font-size: 0.9rem;
}

.node-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(260px, 1fr));
    gap: 0.9rem;
}

.node-card {
    border: 1px solid var(--vp-c-border);
    border-radius: 1rem;
    padding: 0.9rem;
    background: linear-gradient(145deg, var(--vp-c-bg), var(--vp-c-bg-soft));
    display: flex;
    flex-direction: column;
    gap: 0.75rem;
    box-shadow: var(--vp-shadow-2);
    position: relative;
}

.node-card::after {
    content: '';
    position: absolute;
    inset: 0;
    border-radius: 1rem;
    border: 1px dashed transparent;
    transition: border-color 0.2s ease;
}

.node-card:hover::after {
    border-color: var(--vp-c-brand-1);
}

.node-card.leaf {
    background: linear-gradient(145deg, #0f172a, #0b1220);
}

.node-top {
    display: flex;
    gap: 0.75rem;
    align-items: center;
}

.node-icon {
    width: 2.5rem;
    height: 2.5rem;
    display: inline-flex;
    align-items: center;
    justify-content: center;
    border-radius: 0.8rem;
    background: var(--vp-c-brand-soft);
    color: var(--vp-c-text-1);
    font-size: 1.3rem;
    box-shadow: var(--vp-shadow-1);
}

.node-meta {
    display: flex;
    flex-direction: column;
    gap: 0.15rem;
}

.node-key {
    font-weight: 800;
    color: var(--vp-c-text-1);
    text-transform: capitalize;
}

.node-path {
    font-family: var(--vp-font-family-mono);
    font-size: 0.8rem;
    color: var(--vp-c-text-2);
}

.node-desc {
    margin: 0;
    color: var(--vp-c-text-1);
}

.badges {
    display: flex;
    flex-wrap: wrap;
    gap: 0.35rem;
}

.badge {
    display: inline-flex;
    align-items: center;
    gap: 0.35rem;
    background: var(--vp-c-bg-soft);
    color: var(--vp-c-text-1);
    border: 1px solid var(--vp-c-border);
    padding: 0.25rem 0.5rem;
    border-radius: 999px;
    font-size: 0.85rem;
}

.badge.subtle {
    background: transparent;
}

.preview {
    display: flex;
    flex-direction: column;
    gap: 0.4rem;
}

.preview-label {
    font-size: 0.8rem;
    color: var(--vp-c-text-2);
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.06em;
}

.preview-tags {
    display: flex;
    flex-wrap: wrap;
    gap: 0.35rem;
}

.preview-tag,
.more {
    padding: 0.2rem 0.45rem;
    background: var(--vp-c-bg);
    border-radius: 0.5rem;
    border: 1px dashed var(--vp-c-border);
    font-family: var(--vp-font-family-mono);
    color: var(--vp-c-text-1);
}

.more {
    color: var(--vp-c-text-2);
}

.node-actions {
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 0.5rem;
    flex-wrap: wrap;
}

.descendant-count {
    font-size: 0.85rem;
    color: var(--vp-c-text-2);
}

@media (max-width: 720px) {
    .header-actions {
        width: 100%;
        justify-content: flex-start;
    }

    .node-actions {
        flex-direction: column;
        align-items: flex-start;
    }
}
</style>
