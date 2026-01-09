<template>
  <a 
    :href="href"
    class="group block overflow-hidden rounded-2xl border border-surface-lighter bg-surface-dark transition-all hover:-translate-y-1 hover:border-primary/50 hover:shadow-2xl"
  >
    <div class="relative aspect-[16/10] w-full overflow-hidden bg-surface-lighter">
      <img 
        :src="img" 
        :alt="title" 
        class="h-full w-full object-cover transition-transform duration-500 group-hover:scale-105"
        loading="lazy"
      />
      <div class="absolute inset-0 bg-gradient-to-t from-background-dark/80 via-transparent to-transparent"></div>
    </div>
    <div class="p-6">
      <div class="mb-3 flex items-center justify-between">
        <span 
          :class="[
            'inline-block rounded-full px-3 py-1 text-xs font-bold uppercase tracking-wider',
            tagColor || 'text-primary-light',
            bgColor || 'bg-primary/10'
          ]"
        >
          {{ category }}
        </span>
        <span class="flex items-center gap-1.5 text-xs text-text-dim">
          <CalendarIcon class="w-4 h-4" />
          {{ date }}
        </span>
      </div>
      <h3 class="mb-3 font-display text-xl font-bold leading-snug text-white transition-colors group-hover:text-primary-light">
        {{ title }}
      </h3>
      <p class="text-sm leading-relaxed text-gray-400">
        {{ desc }}
      </p>
    </div>
  </a>
</template>

<script setup lang="ts">
import { CalendarIcon } from '@heroicons/vue/24/outline';

interface Props {
  category: string;
  title: string;
  date: string;
  img: string;
  desc: string;
  tagColor?: string;
  bgColor?: string;
  href?: string;
}

withDefaults(defineProps<Props>(), {
  href: '#'
});
</script>
