<template>
  <div class="flex flex-col gap-4 p-8 bg-surface-dark/50 border border-border-dark rounded-2xl hover:border-primary/50 transition-all duration-300 group">
    <div class="flex items-center gap-3">
      <component :is="heroIcon" class="w-10 h-10 text-primary group-hover:scale-110 transition-transform" />
    </div>
    <h3 class="text-2xl font-bold text-white">{{ title }}</h3>
    <p class="text-gray-400 text-base leading-relaxed">{{ desc }}</p>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue';
import { CpuChipIcon, Squares2X2Icon, CubeTransparentIcon } from '@heroicons/vue/24/outline';

const props = defineProps<{
  icon: string;
  title: string;
  desc: string;
}>();

const iconMap: Record<string, any> = {
  'psychology': CpuChipIcon,
  'account_tree': Squares2X2Icon,
  'hub': CubeTransparentIcon,
};

const heroIcon = computed(() => iconMap[props.icon] || CpuChipIcon);
</script>
