<template>
  <a 
    :href="link" 
    class="group relative block p-8 bg-card-dark rounded-2xl border border-slate-700 hover:border-primary/50 transition-all duration-300 shadow-lg hover:shadow-2xl hover:shadow-primary/10"
  >
    <div class="absolute -inset-1 bg-gradient-to-r from-primary/0 to-primary/0 group-hover:from-primary/20 group-hover:to-purple-600/20 rounded-2xl blur opacity-0 group-hover:opacity-50 transition duration-500"></div>
    <div class="relative">
      <div class="flex items-center gap-4 mb-4">
        <div class="w-14 h-14 rounded-xl bg-primary/10 flex items-center justify-center group-hover:bg-primary/20 transition-colors">
          <component :is="getIcon(icon)" class="w-8 h-8 text-primary" />
        </div>
      </div>
      <h3 class="text-2xl font-bold text-white mb-3 group-hover:text-primary transition-colors">{{ title }}</h3>
      <p class="text-slate-400 leading-relaxed mb-4">{{ desc }}</p>
      <div class="flex items-center gap-2 text-primary text-sm font-semibold">
        <span>{{ linkText }}</span>
        <ArrowRightIcon class="w-5 h-5 group-hover:translate-x-1 transition-transform" />
      </div>
    </div>
  </a>
</template>

<script setup lang="ts">
import { ArrowRightIcon, CogIcon, TagIcon } from '@heroicons/vue/24/outline';

const props = defineProps<{
  icon: string;
  title: string;
  desc: string;
  link: string;
  linkText?: string;
}>();

const iconMap: Record<string, any> = {
  'cog': CogIcon,
  'tag': TagIcon,
};

const getIcon = (iconName: string) => {
  return iconMap[iconName] || CogIcon;
};
</script>
