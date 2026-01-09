<template>
  <div class="relative group">
    <div class="rounded-xl border border-surface-lighter bg-surface-dark overflow-hidden">
      <div v-if="title || language" class="flex items-center justify-between border-b border-surface-lighter bg-background-dark px-4 py-2">
        <div class="flex items-center gap-2">
          <span v-if="language" class="text-xs font-mono text-text-dim uppercase">{{ language }}</span>
          <span v-if="title" class="text-sm text-white">{{ title }}</span>
        </div>
        <button
          @click="copyCode"
          class="flex items-center gap-1.5 rounded-lg px-3 py-1.5 text-xs font-medium text-text-dim transition-all hover:bg-surface-lighter hover:text-white"
          :class="copied ? 'text-emerald-400' : ''"
        >
          <span class="material-symbols-outlined text-base">{{ copied ? 'check' : 'content_copy' }}</span>
          {{ copied ? 'Copied!' : 'Copy' }}
        </button>
      </div>
      <div class="relative">
        <button
          v-if="!title && !language"
          @click="copyCode"
          class="absolute right-2 top-2 z-10 flex items-center gap-1.5 rounded-lg bg-surface-dark/90 px-3 py-1.5 text-xs font-medium text-text-dim opacity-0 transition-all group-hover:opacity-100 hover:bg-surface-lighter hover:text-white"
          :class="copied ? 'text-emerald-400 opacity-100' : ''"
        >
          <span class="material-symbols-outlined text-base">{{ copied ? 'check' : 'content_copy' }}</span>
          {{ copied ? 'Copied!' : 'Copy' }}
        </button>
        <pre class="overflow-x-auto p-4"><code ref="codeElement" class="text-sm font-mono"><slot /></code></pre>
      </div>
    </div>
  </div>
</template>

<script lang="ts" setup>
import { ref } from 'vue'

interface Props {
  language?: string
  title?: string
}

defineProps<Props>()

const copied = ref(false)
const codeElement = ref<HTMLElement | null>(null)

const copyCode = async () => {
  if (!codeElement.value) return
  
  const code = codeElement.value.textContent || ''
  
  try {
    await navigator.clipboard.writeText(code)
    copied.value = true
    setTimeout(() => {
      copied.value = false
    }, 2000)
  } catch (err) {
    console.error('Failed to copy code:', err)
  }
}
</script>
