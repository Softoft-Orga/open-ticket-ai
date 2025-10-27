<script setup lang="ts">
import {computed} from 'vue'
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
</script>

<template>
  <div v-if="recentArticle" aria-live="polite" class="recent-news-toast" role="status">
    <a :href="recentArticle.link" class="recent-news-toast__link">{{ recentArticle.toastMessage }}</a>
  </div>
</template>

<style scoped>
.recent-news-toast {
  width: 100%;
  background: var(--vp-c-brand-soft);
  color: var(--vp-c-brand-1);
  padding: 0.75rem 1rem;
  display: flex;
  justify-content: center;
  align-items: center;
  border-bottom: 1px solid rgba(100, 108, 255, 0.25);
}

.recent-news-toast__link {
  color: inherit;
  font-weight: 600;
}

.recent-news-toast__link:hover {
  color: var(--vp-c-brand-2);
}
</style>
