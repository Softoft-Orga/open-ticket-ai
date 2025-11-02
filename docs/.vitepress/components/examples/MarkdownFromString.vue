<template>
  <div v-html="rendered" class="prose prose-invert max-w-none"></div>
</template>

<script lang="ts" setup>
import {computed} from 'vue'
import MarkdownIt from 'markdown-it'

const props = defineProps<{ markdown: string }>()

const renderer = new MarkdownIt({
  html: true,
  linkify: true,
  breaks: true,
})

const rendered = computed(() => renderer.render(props.markdown ?? ''))
</script>
