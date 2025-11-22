<script lang="ts" setup>
import {useYamlTagTree} from '../../composables/useYamlTagTree'
import TagNode from './TagNode.vue'

const {source} = defineProps<{
    source: string
}>()

const {tree, error} = useYamlTagTree(source)
</script>

<template>
    <div class="yaml-tree">
        <div v-if="error" class="yaml-tree__error">
            {{ error }}
        </div>
        <ul v-else class="yaml-tree__list">
            <TagNode
                v-for="node in tree"
                :key="node.path"
                :node="node"
            />
        </ul>
    </div>
</template>

<style scoped>
.yaml-tree {
    border: 1px solid var(--vp-c-divider);
    border-radius: 12px;
    padding: 12px;
    background: var(--vp-c-bg-soft);
}

.yaml-tree__error {
    color: #ff6b6b;
    font-family: var(--vp-font-family-mono), serif;
    font-size: 13px;
}

.yaml-tree__list {
    list-style: none;
    padding-left: 0;
    margin: 0;
}
</style>
