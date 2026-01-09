<script setup lang="ts">
import {computed} from 'vue'
import {useNewsArticles} from '../../../composables/useNewsArticles'

const {newsArticles} = useNewsArticles()
const articles = computed(() => newsArticles.value)
</script>

<template>
  <section v-if="articles.length" class="grid gap-8 my-16">
    <div class="grid gap-3">
      <h2>Latest News</h2>
      <p>Stay on top of product releases, platform updates, and community announcements.</p>
    </div>
    <div class="grid gap-6 md:grid-cols-2 lg:grid-cols-3">
      <article v-for="article in articles" :key="article.link" class="grid gap-4 rounded-2xl border border-[rgba(100,108,255,0.2)] overflow-hidden bg-[var(--vp-c-bg-soft)] transition-all duration-200 hover:border-[var(--vp-c-brand-2)] hover:-translate-y-1">
        <a :href="article.link" class="block overflow-hidden">
          <img :alt="`${article.title} cover image`" :src="article.image" class="w-full h-[200px] object-cover"/>
        </a>
        <div class="grid gap-3 px-5 pb-5">
          <p class="text-sm text-[var(--vp-c-text-2)] tracking-wide uppercase">{{ article.formattedDate }}</p>
          <h3 class="text-xl font-semibold text-[var(--vp-c-text-1)]">{{ article.title }}</h3>
          <p class="text-[var(--vp-c-text-2)] leading-relaxed">{{ article.description }}</p>
          <a :href="article.link" class="justify-self-start font-semibold text-[var(--vp-c-brand-1)] hover:text-[var(--vp-c-brand-2)]">Read full article</a>
        </div>
      </article>
    </div>
  </section>
</template>
