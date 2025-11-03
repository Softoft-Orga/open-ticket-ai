<template>
    <div class="vp-doc" v-html="html"/>
</template>

<script lang="ts" setup>
import {ref, watchEffect} from 'vue'
import MarkdownIt from 'markdown-it'

const {markdown} = defineProps<{ markdown: string }>()

const html = ref('')
let md: MarkdownIt | null = null

async function ensureMd() {
    if (md) return
    md = new MarkdownIt({html: true, linkify: true, breaks: true})
}

watchEffect(async () => {
    await ensureMd()
    html.value = md!.render(markdown ?? '')
})
</script>
