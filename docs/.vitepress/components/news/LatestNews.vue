<script setup lang="ts">
import {computed} from 'vue'
import {useNewsArticles} from '../../composables/useNewsArticles'

const {newsArticles} = useNewsArticles()
const articles = computed(() => newsArticles.value)
</script>

<template>
  <section v-if="articles.length" class="latest-news">
    <div class="latest-news__intro">
      <h2>Latest News</h2>
      <p>Stay on top of product releases, platform updates, and community announcements.</p>
    </div>
    <div class="latest-news__grid">
      <article v-for="article in articles" :key="article.link" class="latest-news__item">
        <a :href="article.link" class="latest-news__image-wrapper">
          <img :alt="`${article.title} cover image`" :src="article.image" class="latest-news__image"/>
        </a>
        <div class="latest-news__content">
          <p class="latest-news__date">{{ article.formattedDate }}</p>
          <h3 class="latest-news__title">{{ article.title }}</h3>
          <p class="latest-news__description">{{ article.description }}</p>
          <a :href="article.link" class="latest-news__cta">Read full article</a>
        </div>
      </article>
    </div>
  </section>
</template>

<style scoped>
.latest-news {
  display: grid;
  gap: 2rem;
  margin: 4rem 0;
}

.latest-news__intro {
  display: grid;
  gap: 0.75rem;
}

.latest-news__grid {
  display: grid;
  gap: 1.5rem;
}

@media (min-width: 768px) {
  .latest-news__grid {
    grid-template-columns: repeat(2, minmax(0, 1fr));
  }
}

@media (min-width: 1024px) {
  .latest-news__grid {
    grid-template-columns: repeat(3, minmax(0, 1fr));
  }
}

.latest-news__item {
  display: grid;
  gap: 1rem;
  border-radius: 1rem;
  border: 1px solid rgba(100, 108, 255, 0.2);
  overflow: hidden;
  background: var(--vp-c-bg-soft);
  transition: border-color 0.2s ease, transform 0.2s ease;
}

.latest-news__item:hover {
  border-color: var(--vp-c-brand-2);
  transform: translateY(-4px);
}

.latest-news__image-wrapper {
  display: block;
  overflow: hidden;
}

.latest-news__image {
  width: 100%;
  height: 200px;
  object-fit: cover;
}

.latest-news__content {
  display: grid;
  gap: 0.75rem;
  padding: 1.25rem;
}

.latest-news__date {
  font-size: 0.875rem;
  color: var(--vp-c-text-2);
  letter-spacing: 0.03em;
  text-transform: uppercase;
}

.latest-news__title {
  font-size: 1.25rem;
  font-weight: 600;
  color: var(--vp-c-text-1);
}

.latest-news__description {
  color: var(--vp-c-text-2);
  line-height: 1.6;
}

.latest-news__cta {
  justify-self: flex-start;
  font-weight: 600;
  color: var(--vp-c-brand-1);
}

.latest-news__cta:hover {
  color: var(--vp-c-brand-2);
}
</style>
