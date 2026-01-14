<script setup lang="ts">
import { ref, computed } from 'vue';
import {
  MagnifyingGlassIcon,
  CalendarIcon,
  EnvelopeIcon,
  Squares2X2Icon,
  RocketLaunchIcon,
  CodeBracketIcon,
  LightBulbIcon,
  ShieldCheckIcon,
} from '@heroicons/vue/24/outline';
import Button from '../core/basic/Button.vue';

interface BlogPost {
  id: string;
  data: {
    title: string;
    description?: string;
    date: Date;
    category?: string;
    image?: string;
    draft?: boolean;
    tags?: string[];
  };
}

interface Props {
  posts: BlogPost[];
}

const props = defineProps<Props>();

const searchQuery = ref('');
const selectedTopic = ref('All Posts');
const sortBy = ref('Newest First');

const topics = [
  { name: 'All Posts', icon: Squares2X2Icon },
  { name: 'Product Updates', icon: RocketLaunchIcon },
  { name: 'Engineering', icon: CodeBracketIcon },
  { name: 'Use Cases', icon: LightBulbIcon },
  { name: 'Security', icon: ShieldCheckIcon },
];

const formatDate = (date: Date) => {
  return date.toLocaleDateString('en-US', { month: 'short', day: 'numeric', year: 'numeric' });
};

const getPlaceholderImage = (index: number) => {
  return `https://picsum.photos/400/250?${index}`;
};

const getBlogUrl = (id: string) => {
  return `/blog/${id.replace(/^[a-z]{2}\//, '').replace(/\.(md|mdx)$/, '')}/`;
};

const filteredAndSortedPosts = computed(() => {
  let result = [...props.posts];

  // Filter by search query (search by title)
  if (searchQuery.value.trim()) {
    const query = searchQuery.value.toLowerCase();
    result = result.filter(post => post.data.title.toLowerCase().includes(query));
  }

  // Filter by topic/category
  if (selectedTopic.value !== 'All Posts') {
    result = result.filter(post => {
      const category = post.data.category || '';
      return (
        category.toLowerCase() === selectedTopic.value.toLowerCase() ||
        selectedTopic.value.toLowerCase().includes(category.toLowerCase())
      );
    });
  }

  // Sort
  if (sortBy.value === 'Newest First') {
    result.sort((a, b) => b.data.date.getTime() - a.data.date.getTime());
  } else if (sortBy.value === 'Oldest First') {
    result.sort((a, b) => a.data.date.getTime() - b.data.date.getTime());
  } else if (sortBy.value === 'Most Popular') {
    // For now, sort by newest first as we don't have popularity metrics
    // This can be extended later to use view counts or other metrics
    result.sort((a, b) => b.data.date.getTime() - a.data.date.getTime());
  }

  return result;
});

const topicCounts = computed(() => {
  const counts: Record<string, number> = {
    'All Posts': props.posts.length,
  };

  topics.forEach(topic => {
    if (topic.name !== 'All Posts') {
      counts[topic.name] = props.posts.filter(post => {
        const category = post.data.category || '';
        return (
          category.toLowerCase() === topic.name.toLowerCase() ||
          topic.name.toLowerCase().includes(category.toLowerCase())
        );
      }).length;
    }
  });

  return counts;
});
</script>

<template>
  <div class="mx-auto max-w-7xl px-4 py-24 sm:px-6 lg:px-8">
    <div class="flex flex-col gap-16 lg:flex-row">
      <!-- Sidebar -->
      <aside class="w-full flex-shrink-0 space-y-12 lg:w-80">
        <div class="relative">
          <label for="search-articles" class="sr-only">Search articles</label>
          <MagnifyingGlassIcon
            class="absolute left-4 top-1/2 h-5 w-5 -translate-y-1/2 text-text-dim"
            aria-hidden="true"
          />
          <input
            id="search-articles"
            v-model="searchQuery"
            class="block w-full rounded-xl border border-surface-lighter bg-surface-dark py-4 pl-12 pr-4 text-sm text-white placeholder-text-dim shadow-sm transition-all focus:border-primary focus:ring-primary"
            placeholder="Search articles..."
            type="text"
            aria-label="Search articles"
          />
        </div>

        <div>
          <h3 class="font-display mb-6 text-sm font-bold uppercase tracking-wider text-text-dim">
            Explore Topics
          </h3>
          <nav class="space-y-2">
            <Button
              v-for="topic in topics"
              :key="topic.name"
              :variant="selectedTopic === topic.name ? 'outline' : 'subtle'"
              :tone="selectedTopic === topic.name ? 'primary' : 'neutral'"
              size="md"
              radius="lg"
              :class="[
                'group flex w-full items-center justify-between text-left text-sm font-medium',
                selectedTopic === topic.name ? '' : 'hover:text-white',
              ]"
              @click="selectedTopic = topic.name"
            >
              <div class="flex items-center gap-3">
                <component :is="topic.icon" class="h-5 w-5" />
                <span>{{ topic.name }}</span>
              </div>
              <span
                v-if="topic.name === 'All Posts' || topicCounts[topic.name] > 0"
                :class="[
                  'rounded-full px-2.5 py-0.5 text-xs font-bold',
                  selectedTopic === topic.name
                    ? 'bg-primary/30 text-primary-light'
                    : 'bg-surface-lighter text-text-dim',
                ]"
              >
                {{ topicCounts[topic.name] || 0 }}
              </span>
            </Button>
          </nav>
        </div>

        <div class="rounded-2xl border border-surface-lighter bg-surface-dark p-8">
          <div
            class="mb-6 flex size-12 items-center justify-center rounded-xl bg-primary/20 text-primary"
          >
            <EnvelopeIcon class="h-7 w-7" aria-hidden="true" />
          </div>
          <h3 class="font-display mb-3 text-xl font-bold text-white">Stay in the loop</h3>
          <p class="mb-6 text-sm text-text-dim">
            Get the latest on AI automation and engineering straight to your inbox.
          </p>
          <form
            name="blog-subscription"
            method="POST"
            action="/success/blog-subscription/"
            data-netlify="true"
            class="space-y-4"
          >
            <input type="hidden" name="form-name" value="blog-subscription" />
            <label for="newsletter-email" class="sr-only">Email address</label>
            <input
              id="newsletter-email"
              name="email"
              class="w-full rounded-xl border border-surface-lighter bg-background-dark px-4 py-3 text-sm text-white placeholder-text-dim focus:border-primary"
              placeholder="work@email.com"
              type="email"
              aria-label="Email address for newsletter"
              required
            />
            <Button type="submit" variant="outline" tone="primary" size="md" radius="xl" block>
              Subscribe
            </Button>
          </form>
        </div>
      </aside>

      <!-- Articles Grid -->
      <div class="flex-1">
        <div class="mb-12 flex items-end justify-between border-b border-surface-lighter pb-6">
          <h2 class="font-display text-3xl font-bold text-white">Latest Articles</h2>
          <div class="flex items-center gap-2">
            <label for="sort-select" class="text-sm text-text-dim">Sort by:</label>
            <select
              id="sort-select"
              v-model="sortBy"
              aria-label="Sort articles by"
              class="cursor-pointer rounded border-none bg-transparent py-0 pl-2 pr-10 text-sm font-medium text-white focus:ring-0"
            >
              <option>Newest First</option>
              <option>Oldest First</option>
              <option>Most Popular</option>
            </select>
          </div>
        </div>

        <div v-if="filteredAndSortedPosts.length === 0" class="py-12 text-center">
          <p class="text-lg text-text-dim">No articles found matching your criteria.</p>
        </div>

        <div v-else class="grid gap-8 md:grid-cols-2">
          <a
            v-for="(post, index) in filteredAndSortedPosts"
            :key="post.id"
            :href="getBlogUrl(post.id)"
            class="group block overflow-hidden rounded-2xl border border-surface-lighter bg-surface-dark transition-all hover:-translate-y-1 hover:border-primary/50 hover:shadow-2xl"
          >
            <div class="relative aspect-[16/10] w-full overflow-hidden bg-surface-lighter">
              <img
                :src="post.data.image || getPlaceholderImage(index + 1)"
                :alt="post.data.title"
                class="h-full w-full object-cover transition-transform duration-500 group-hover:scale-105"
                loading="lazy"
              />
              <div
                class="absolute inset-0 bg-gradient-to-t from-background-dark/80 via-transparent to-transparent"
              />
            </div>
            <div class="p-6">
              <div class="mb-3 flex items-center justify-between">
                <span
                  class="inline-block rounded-full bg-primary/10 px-3 py-1 text-xs font-bold uppercase tracking-wider text-primary-light"
                >
                  {{ post.data.category || 'Article' }}
                </span>
                <span class="flex items-center gap-1.5 text-xs text-text-dim">
                  <CalendarIcon class="h-4 w-4" />
                  {{ formatDate(post.data.date) }}
                </span>
              </div>
              <h3
                class="font-display mb-3 text-xl font-bold leading-snug text-white transition-colors group-hover:text-primary-light"
              >
                {{ post.data.title }}
              </h3>
              <p class="text-sm leading-relaxed text-text-dim">
                {{ post.data.description || '' }}
              </p>
            </div>
          </a>
        </div>
      </div>
    </div>
  </div>
</template>
