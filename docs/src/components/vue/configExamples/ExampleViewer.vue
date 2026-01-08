<template>
  <details class="group rounded-lg border border-[color:var(--vp-c-divider)] bg-[color:var(--vp-c-bg-soft)] p-4">
    <summary class="cursor-pointer select-none text-sm font-semibold text-[color:var(--vp-c-text-1)]">
      Config.yml Example
    </summary>

    <div>
      <div v-if="loading" class="text-[color:var(--vp-c-text-3)]">Loading example…</div>
      <div v-else-if="error" class="text-[color:var(--vp-c-danger-1,#f87171)]">{{ error }}</div>
      <div v-else>
        <div v-if="canCopy" class="flex items-center justify-end">
          <button
            class="inline-flex items-center rounded-md border border-[color:var(--vp-c-divider)] bg-[color:var(--vp-c-bg)] px-3 py-1 text-xs font-medium text-[color:var(--vp-c-text-2)] transition hover:text-[color:var(--vp-c-text-1)]"
            type="button"
            @click="copyToClipboard"
          >
            {{ copied ? 'Copied!' : 'Copy YAML' }}
          </button>
        </div>

        <div class="shiki-wrap" v-html="contentHtml"></div>
      </div>
    </div>
  </details>
</template>

<script lang="ts" setup>
import { computed, onMounted, ref, watch } from 'vue'
import { useData } from 'vitepress'
import { codeToHtml } from 'shiki'

const { file } = defineProps<{ file: string }>()

const raw = ref('')
const contentHtml = ref('')
const loading = ref(false)
const error = ref<string | null>(null)
const copied = ref(false)

const { site } = useData()
const canCopy = computed(() => typeof navigator !== 'undefined' && Boolean(navigator.clipboard))

async function fetchYaml(path: string) {
  if (!path) { raw.value = ''; contentHtml.value = ''; return }
  loading.value = true
  error.value = null
  try {
    const base = site.value?.base ?? '/'
    const nb = base.endsWith('/') ? base : `${base}/`
    const url = path.startsWith('/') ? `${nb}${path.slice(1)}` : `${nb}${path}`
    const res = await fetch(url)
    if (!res.ok) throw new Error(`Failed to load example: ${res.status} ${res.statusText}`)
    raw.value = await res.text()
    contentHtml.value = await codeToHtml(raw.value, { lang: 'yaml', theme: 'vitesse-dark' })
  } catch (e) {
    error.value = e instanceof Error ? e.message : 'Unable to load example'
  } finally {
    loading.value = false
  }
}

async function copyToClipboard() {
  if (!canCopy.value) return
  await navigator.clipboard.writeText(raw.value)
  copied.value = true
  setTimeout(() => { copied.value = false }, 2000)
}

watch(() => file, f => { void fetchYaml(f) }, { immediate: true })
onMounted(() => { if (!raw.value && file) void fetchYaml(file) })
</script>

<style scoped>
:deep(.shiki-wrap pre.shiki) {
  padding: 1rem;
  border-radius: 0.5rem;
  background: var(--vp-code-block-bg, #1e1e1e);
}
</style>
