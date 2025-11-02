<template>
  <details class="group rounded-lg border border-[color:var(--vp-c-divider)] bg-[color:var(--vp-c-bg-soft)] p-4">
    <summary class="cursor-pointer select-none text-sm font-semibold text-[color:var(--vp-c-text-1)]">
      Config.yml Example
    </summary>
    <div class="mt-4 space-y-4 text-sm text-[color:var(--vp-c-text-2)]">
      <div v-if="loading" class="text-[color:var(--vp-c-text-3)]">Loading example…</div>
      <div v-else-if="error" class="text-[color:var(--vp-c-danger-1,#f87171)]">
        {{ error }}
      </div>
      <div v-else>
        <div
          v-if="canCopy"
          class="flex items-center justify-end"
        >
          <button
            type="button"
            class="inline-flex items-center rounded-md border border-[color:var(--vp-c-divider)] bg-[color:var(--vp-c-bg)] px-3 py-1 text-xs font-medium text-[color:var(--vp-c-text-2)] transition hover:text-[color:var(--vp-c-text-1)]"
            @click="copyToClipboard"
          >
            {{ copied ? 'Copied!' : 'Copy YAML' }}
          </button>
        </div>
        <pre class="max-h-[32rem] overflow-auto rounded-md bg-[color:var(--vp-code-block-bg,#1e1e1e)] p-4 text-[color:var(--vp-code-block-text,#f8f8f2)]">
          <code class="language-yaml">{{ content }}</code>
        </pre>
      </div>
    </div>
  </details>
</template>

<script lang="ts" setup>
import {computed, onMounted, ref, watch} from 'vue'
import {useData} from 'vitepress'

const props = defineProps<{ file: string }>()

const content = ref('')
const loading = ref(false)
const error = ref<string | null>(null)
const copied = ref(false)

const {site} = useData()

const canCopy = computed(() => typeof navigator !== 'undefined' && Boolean(navigator.clipboard))

async function fetchYaml(path: string) {
  if (!path) {
    content.value = ''
    return
  }

  loading.value = true
  error.value = null

  try {
    const base = site.value?.base ?? '/'
    const normalizedBase = base.endsWith('/') ? base : `${base}/`
    const url = path.startsWith('/') ? `${normalizedBase}${path.slice(1)}` : `${normalizedBase}${path}`
    const response = await fetch(url)
    if (!response.ok) {
      throw new Error(`Failed to load example: ${response.status} ${response.statusText}`)
    }
    content.value = await response.text()
  } catch (err) {
    error.value = err instanceof Error ? err.message : 'Unable to load example'
  } finally {
    loading.value = false
  }
}

async function copyToClipboard() {
  if (!canCopy.value) {
    return
  }
  try {
    await navigator.clipboard.writeText(content.value)
    copied.value = true
    setTimeout(() => {
      copied.value = false
    }, 2000)
  } catch (err) {
    console.error('Failed to copy YAML', err)
  }
}

watch(() => props.file, file => {
  void fetchYaml(file)
}, {immediate: true})

onMounted(() => {
  if (!content.value && props.file) {
    void fetchYaml(props.file)
  }
})
</script>
