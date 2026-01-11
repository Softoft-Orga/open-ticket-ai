<script lang='ts' setup>
import type {TagNode} from '../../../composables/useYamlTagTree'

const props = defineProps<{
    node: TagNode
}>()

console.log(props)</script>

<template>
  <li class="space-y-2">
    <div class="flex flex-wrap items-center gap-3 text-sm text-slate-100">
      <span
        v-if="node.parentIcon || node.icon"
        class="flex h-7 w-7 items-center justify-center rounded-full bg-slate-800/70 text-lg shadow-inner shadow-black/50"
      >
        {{ node.parentIcon || node.icon }}
      </span>
      <span class="rounded-md bg-slate-800/70 px-2 py-1 font-mono text-xs font-semibold text-indigo-100 ring-1 ring-slate-700">
        {{ node.key }}
      </span>
      <span
        v-if="node.description"
        class="text-slate-300"
      >– {{ node.description }}</span>
    </div>
    <ul
      v-if="node.children.length"
      class="ml-4 border-l border-dashed border-slate-700 pl-3"
    >
      <TagNode
        v-for="child in node.children"
        :key="child.path"
        :node="child"
      />
    </ul>
  </li>
</template>
