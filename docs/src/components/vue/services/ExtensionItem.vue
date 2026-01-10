<template>
  <div class="flex items-start gap-4">
    <div class="text-primary mt-0.5">
      <component :is="IconComponent" class="w-6 h-6" aria-hidden="true" />
    </div>
    <div>
      <h5 class="text-white text-sm font-bold mb-1">{{ title }}</h5>
      <p class="text-slate-500 text-xs leading-relaxed">{{ desc }}</p>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue';
import {
  WrenchScrewdriverIcon,
  ChartBarIcon,
  Cog6ToothIcon,
  ArrowPathIcon,
  CpuChipIcon,
  CubeTransparentIcon,
  CheckBadgeIcon,
  RocketLaunchIcon
} from '@heroicons/vue/24/outline';

const props = defineProps<{
  icon: string;
  title: string;
  desc: string;
}>();

// Map material icon names to Heroicons
const iconMap: Record<string, any> = {
  'tune': WrenchScrewdriverIcon,
  'analytics': ChartBarIcon,
  'integration_instructions': Cog6ToothIcon,
  'update': ArrowPathIcon,
  'psychology': CpuChipIcon,
  'hub': CubeTransparentIcon,
  'verified': CheckBadgeIcon,
  'rocket_launch': RocketLaunchIcon,
};

const IconComponent = computed(() => iconMap[props.icon] || WrenchScrewdriverIcon);
</script>
