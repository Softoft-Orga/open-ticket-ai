<template>
  <div>
    <h3 class="mb-6 text-2xl font-bold text-white">Related Articles</h3>
    <div class="grid gap-6 md:grid-cols-2 lg:grid-cols-3">
      <a
        v-for="(post, index) in posts"
        :key="index"
        :href="post.href"
        class="group block overflow-hidden rounded-xl border border-surface-lighter bg-surface-dark transition-all hover:-translate-y-1 hover:border-primary/50 hover:shadow-xl"
      >
        <div v-if="post.image" class="relative aspect-[16/9] overflow-hidden bg-surface-lighter">
          <img
            :src="post.image"
            :alt="post.title"
            class="h-full w-full object-cover transition-transform duration-500 group-hover:scale-105"
            loading="lazy"
          />
        </div>
        <div class="p-4">
          <div class="mb-2 flex items-center gap-2">
            <span class="inline-block rounded-full bg-primary/10 px-2 py-1 text-xs font-semibold uppercase tracking-wider text-primary-light">
              {{ post.category }}
            </span>
            <span class="text-xs text-text-dim">{{ post.date }}</span>
          </div>
          <h4 class="mb-2 font-bold leading-snug text-white transition-colors group-hover:text-primary-light">
            {{ post.title }}
          </h4>
          <p class="text-sm text-gray-400 line-clamp-2">
            {{ post.description }}
          </p>
        </div>
      </a>
    </div>
  </div>
</template>

<script lang="ts" setup>
interface Post {
  title: string
  description: string
  category: string
  date: string
  image?: string
  href: string
}

interface Props {
  posts: Post[]
}

defineProps<Props>()
</script>
