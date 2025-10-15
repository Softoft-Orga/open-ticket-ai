<!-- components/YoutubeVideo.vue -->
<template>
  <div class="relative w-full aspect-video overflow-hidden rounded-2xl shadow-lg">
    <button
        v-if="!loaded"
        class="group absolute inset-0 block"
        type="button"
        @click="loaded = true"
    >
      <img
          :alt="title || 'Video preview'"
          :src="`https://i.ytimg.com/vi/${videoId}/hqdefault.jpg`"
          :srcset="`
          https://i.ytimg.com/vi/${videoId}/mqdefault.jpg 320w,
          https://i.ytimg.com/vi/${videoId}/hqdefault.jpg 480w,
          https://i.ytimg.com/vi/${videoId}/sddefault.jpg 640w,
          https://i.ytimg.com/vi/${videoId}/maxresdefault.jpg 1280w
        `"
          class="absolute inset-0 w-full h-full object-cover transition-transform duration-500 group-hover:scale-105"
          decoding="async"
          draggable="false"
          fetchpriority="low"
          height="720"
          loading="lazy"
          sizes="100vw"
          width="1280"
      />
      <div class="absolute inset-0 bg-black/40"></div>
      <div class="relative z-10 flex items-center justify-center h-full">
        <svg class="w-16 h-16 text-white opacity-90" fill="currentColor" viewBox="0 0 24 24"
             xmlns="http://www.w3.org/2000/svg">
          <path d="M8 5v14l11-7z"/>
        </svg>
      </div>
    </button>

    <iframe
        v-else
        :src="`https://www.youtube-nocookie.com/embed/${videoId}?rel=0&autoplay=1`"
        :title="title || 'YouTube video'"
        allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture"
        allowfullscreen
        class="absolute inset-0 w-full h-full"
        loading="lazy"
        referrerpolicy="strict-origin-when-cross-origin"
    />
  </div>
</template>

<script lang="ts" setup>
import {ref} from 'vue'

const props = defineProps<{ videoId: string; title?: string }>()
const loaded = ref(false)
</script>
