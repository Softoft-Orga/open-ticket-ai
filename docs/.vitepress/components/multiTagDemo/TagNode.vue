<script lang="ts" setup>
import type {TagNode} from '../../composables/useYamlTagTree'

const props = defineProps<{
    node: TagNode
}>()
</script>

<template>
    <li class="tag-node">
        <div class="tag-node__label">
            <span class="tag-node__key">{{ node.key }}</span>
            <span v-if="node.description" class="tag-node__description">
        – {{ node.description }}
      </span>
        </div>
        <ul v-if="node.children.length" class="tag-node__children">
            <TagNode
                v-for="child in node.children"
                :key="child.path"
                :node="child"
            />
        </ul>
    </li>
</template>

<style scoped>
.tag-node {
    margin: 2px 0;
}

.tag-node__label {
    font-size: 14px;
}

.tag-node__key {
    font-family: var(--vp-font-family-mono), serif;
    font-weight: 600;
}

.tag-node__description {
    margin-left: 4px;
    color: var(--vp-c-text-2);
    font-size: 13px;
}

.tag-node__children {
    margin-left: 14px;
    padding-left: 8px;
    border-left: 1px dashed var(--vp-c-divider);
}
</style>
