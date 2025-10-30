<script setup lang="ts">
import {computed, onMounted, onUnmounted, ref} from 'vue'
import {useNewsArticles} from '../composables/useNewsArticles'

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
  <div v-if="recentArticle" ref="toastRef" aria-live="polite" class="recent-news-toast" role="status">
    <a :href="recentArticle.link" class="recent-news-toast__link">{{ recentArticle.toastMessage }}</a>
  </div>
</template>

<style scoped>
.recent-news-toast {
  width: 100%;
  height: 50px;
  background: var(--vp-c-brand-soft);
  color: var(--vp-c-brand-1);
  display: flex;
  justify-content: center;
  align-items: center;
  border-bottom: 1px solid rgba(100, 108, 255, 0.25);
  z-index: 10;
}

.recent-news-toast__link {
  color: inherit;
  font-weight: 600;
}

.recent-news-toast__link:hover {
  color: var(--vp-c-brand-2);
}
</style>
