<template>
  <div class="flex flex-wrap items-center gap-3">
    <span class="text-sm font-medium text-gray-400">Share:</span>
    <button
      @click="shareOn('twitter')"
      class="flex items-center gap-2 rounded-lg border border-surface-lighter bg-surface-dark px-4 py-2 text-sm font-medium text-white transition-all hover:border-primary/50 hover:bg-surface-lighter"
    >
      <span class="material-symbols-outlined text-base">X</span>
      Twitter
    </button>
    <button
      @click="shareOn('linkedin')"
      class="flex items-center gap-2 rounded-lg border border-surface-lighter bg-surface-dark px-4 py-2 text-sm font-medium text-white transition-all hover:border-primary/50 hover:bg-surface-lighter"
    >
      <span class="material-symbols-outlined text-base">business_center</span>
      LinkedIn
    </button>
    <button
      @click="copyLink"
      class="flex items-center gap-2 rounded-lg border border-surface-lighter bg-surface-dark px-4 py-2 text-sm font-medium text-white transition-all hover:border-primary/50 hover:bg-surface-lighter"
    >
      <span class="material-symbols-outlined text-base">{{ copied ? 'check' : 'link' }}</span>
      {{ copied ? 'Copied!' : 'Copy Link' }}
    </button>
  </div>
</template>

<script lang="ts" setup>
import { ref } from 'vue'

interface Props {
  title: string
  url?: string
}

const props = defineProps<Props>()

const copied = ref(false)

const shareOn = (platform: 'twitter' | 'linkedin') => {
  const url = props.url || window.location.href
  const text = encodeURIComponent(props.title)
  const encodedUrl = encodeURIComponent(url)
  
  let shareUrl = ''
  
  if (platform === 'twitter') {
    shareUrl = `https://twitter.com/intent/tweet?text=${text}&url=${encodedUrl}`
  } else if (platform === 'linkedin') {
    shareUrl = `https://www.linkedin.com/sharing/share-offsite/?url=${encodedUrl}`
  }
  
  if (shareUrl) {
    window.open(shareUrl, '_blank', 'width=600,height=400')
  }
}

const copyLink = async () => {
  const url = props.url || window.location.href
  
  try {
    await navigator.clipboard.writeText(url)
    copied.value = true
    setTimeout(() => {
      copied.value = false
    }, 2000)
  } catch (err) {
    console.error('Failed to copy link:', err)
  }
}
</script>
