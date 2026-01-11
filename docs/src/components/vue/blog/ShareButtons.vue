<template>
  <div class="flex flex-wrap items-center gap-3">
    <span class="text-sm font-medium text-gray-400">Share:</span>
    <button
      class="flex items-center gap-2 rounded-lg border border-surface-lighter bg-surface-dark px-4 py-2 text-sm font-medium text-white transition-all hover:border-primary/50 hover:bg-surface-lighter"
      @click="shareOn('twitter')"
    >
      <svg
        class="w-4 h-4"
        fill="currentColor"
        viewBox="0 0 24 24"
        aria-hidden="true"
      >
        <path d="M18.244 2.25h3.308l-7.227 8.26 8.502 11.24H16.17l-5.214-6.817L4.99 21.75H1.68l7.73-8.835L1.254 2.25H8.08l4.713 6.231zm-1.161 17.52h1.833L7.084 4.126H5.117z" />
      </svg>
      Twitter
    </button>
    <button
      class="flex items-center gap-2 rounded-lg border border-surface-lighter bg-surface-dark px-4 py-2 text-sm font-medium text-white transition-all hover:border-primary/50 hover:bg-surface-lighter"
      @click="shareOn('linkedin')"
    >
      <BriefcaseIcon
        class="w-4 h-4"
        aria-hidden="true"
      />
      LinkedIn
    </button>
    <button
      class="flex items-center gap-2 rounded-lg border border-surface-lighter bg-surface-dark px-4 py-2 text-sm font-medium text-white transition-all hover:border-primary/50 hover:bg-surface-lighter"
      @click="copyLink"
    >
      <component
        :is="copied ? CheckIcon : LinkIcon"
        class="w-4 h-4"
        aria-hidden="true"
      />
      {{ copied ? 'Copied!' : 'Copy Link' }}
    </button>
  </div>
</template>

<script lang="ts" setup>
import { ref } from 'vue'
import { CheckIcon, LinkIcon, BriefcaseIcon } from '@heroicons/vue/24/outline'

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
