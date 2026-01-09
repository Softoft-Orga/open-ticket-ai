<template>
  <section class="w-full px-4 md:px-10 lg:px-20 xl:px-40 py-24 bg-[#160b1b]">
    <div class="w-full max-w-7xl mx-auto">
      <div class="flex flex-col lg:flex-row gap-16 items-center rounded-3xl bg-[#1d1023] border border-border-dark p-12 relative overflow-hidden shadow-2xl">
        <div class="absolute -right-20 -top-20 w-96 h-96 bg-cyan-500/10 rounded-full blur-[100px]"></div>

        <!-- Image/Visual Side -->
        <div class="w-full lg:w-1/2 order-2 lg:order-1 z-10">
          <div class="relative group">
            <div class="absolute -inset-1 bg-gradient-to-r from-primary to-cyan-500 rounded-xl blur opacity-20 group-hover:opacity-40 transition duration-1000"></div>
            <div class="relative bg-surface-dark border border-border-dark rounded-xl overflow-hidden shadow-2xl">
              <img 
                v-if="imageSrc" 
                :src="imageSrc" 
                :alt="imageAlt || title"
                class="w-full h-auto"
              />
              <div v-else class="w-full aspect-video bg-gradient-to-br from-primary/20 to-cyan-500/20 flex items-center justify-center">
                <component :is="iconComponent" class="w-24 h-24 text-primary/50" />
              </div>
            </div>
          </div>
        </div>

        <!-- Content Side -->
        <div class="w-full lg:w-1/2 flex flex-col gap-6 order-1 lg:order-2 z-10">
          <div v-if="badge" class="flex items-center gap-2 w-fit px-3 py-1 rounded-full border border-primary/30 bg-primary/10 text-primary text-xs font-bold uppercase tracking-wider">
            <span>{{ badge }}</span>
          </div>
          
          <h2 class="font-display text-4xl font-bold text-white leading-tight">{{ title }}</h2>
          
          <p class="text-gray-400 text-xl leading-relaxed">{{ description }}</p>

          <div v-if="features && features.length > 0" class="flex flex-col gap-3 mt-4">
            <div 
              v-for="(feature, idx) in features" 
              :key="idx"
              class="flex items-start gap-3"
            >
              <div class="w-6 h-6 rounded-full bg-primary/20 flex items-center justify-center flex-shrink-0 mt-1">
                <CheckIcon class="w-4 h-4 text-primary" />
              </div>
              <div class="flex flex-col gap-1">
                <span class="text-white font-semibold">{{ feature.title }}</span>
                <span v-if="feature.description" class="text-gray-400 text-sm">{{ feature.description }}</span>
              </div>
            </div>
          </div>

          <div v-if="ctaText" class="flex items-center gap-2 text-primary font-bold text-lg cursor-pointer group hover:text-white transition-colors mt-4">
            <span>{{ ctaText }}</span>
            <ArrowRightIcon class="w-6 h-6 transition-transform group-hover:translate-x-1" aria-hidden="true" />
          </div>
        </div>
      </div>
    </div>
  </section>
</template>

<script setup lang="ts">
import { computed } from 'vue';
import { ArrowRightIcon, CheckIcon } from '@heroicons/vue/24/outline';
import { CpuChipIcon } from '@heroicons/vue/24/outline';

interface Feature {
  title: string;
  description?: string;
}

const props = defineProps<{
  badge?: string;
  title: string;
  description: string;
  features?: Feature[];
  imageSrc?: string;
  imageAlt?: string;
  ctaText?: string;
}>();

const iconComponent = computed(() => CpuChipIcon);
</script>
