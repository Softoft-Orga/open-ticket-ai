<script lang='ts' setup>
import {useYamlTagTree} from '../../../composables/useYamlTagTree'
import TagNode from './TagNode.vue'

const {source} = defineProps<{
    source: string
}>()

const {tree, error} = useYamlTagTree(source)
</script>

<template>
  <div class="space-y-3 text-slate-100">
    <div
      v-if="error"
      class="rounded-lg border border-red-800 bg-red-950/70 px-3 py-2 text-sm font-medium text-red-100"
    >
      {{ error }}
    </div>
    <ul
      v-else
      class="list-none space-y-2 p-0"
    >
      <TagNode
        v-for="node in tree"
        :key="node.path"
        :node="node"
      />
    </ul>
  </div>
</template>
