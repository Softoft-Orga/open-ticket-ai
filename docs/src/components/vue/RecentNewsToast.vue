<script setup lang="ts">
import {computed, onMounted, onUnmounted, ref} from 'vue'
import {useNewsArticles} from '../../composables/useNewsArticles'

const {mostRecentNewsArticle, isMostRecentNewsRecentlyPublished} = useNewsArticles()

const recentArticle = computed(() => {
  if (!isMostRecentNewsRecentlyPublished.value) {
    return null
  }
  const article = mostRecentNewsArticle.value
  if (!article || !article.toastMessage) {
    return null
  }
  return article
})

const toastRef = ref<HTMLElement | null>(null)


onMounted(() => {
})

onUnmounted(() => {
})
</script>

<template>
  <div
    v-if="recentArticle"
    ref="toastRef"
    aria-live="polite"
    class="w-full h-[50px] bg-[var(--vp-c-brand-soft)] text-[var(--vp-c-brand-1)] flex justify-center items-center border-b border-[rgba(100,108,255,0.25)] z-10"
    role="status"
  >
    <a
      :href="recentArticle.link"
      class="text-inherit font-semibold hover:text-[var(--vp-c-brand-2)]"
    >{{ recentArticle.toastMessage }}</a>
  </div>
</template>
