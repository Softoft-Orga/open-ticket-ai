<template>
  <div class="flex flex-col gap-6 p-8 bg-surface-dark/50 border border-border-dark rounded-2xl hover:border-primary/50 transition-all duration-300 group h-full">
    <div class="flex items-start justify-between gap-4">
      <div class="flex items-center gap-3">
        <component :is="iconComponent" class="w-8 h-8 text-primary group-hover:scale-110 transition-transform flex-shrink-0" />
      </div>
      <div v-if="startingPrice" class="text-primary font-bold text-lg whitespace-nowrap">
        ${{ formatPrice(startingPrice) }}
      </div>
    </div>
    
    <div class="flex flex-col gap-3 flex-grow">
      <h3 class="text-xl font-bold text-white">{{ title }}</h3>
      <p v-if="oneLiner" class="text-primary/80 text-sm font-medium">{{ oneLiner }}</p>
      <p class="text-gray-400 text-sm leading-relaxed">{{ description }}</p>
    </div>

    <div v-if="outcomes && outcomes.length > 0" class="flex flex-col gap-2">
      <ul class="space-y-2">
        <li v-for="(outcome, idx) in outcomes.slice(0, 3)" :key="idx" class="flex items-start gap-2 text-sm text-gray-400">
          <CheckIcon class="w-4 h-4 text-primary flex-shrink-0 mt-0.5" />
          <span>{{ outcome }}</span>
        </li>
      </ul>
    </div>

    <button class="w-full py-3 px-6 rounded-lg border border-border-dark hover:border-primary/50 text-white text-sm font-medium transition-colors bg-surface-lighter/50 hover:bg-surface-lighter">
      Contact Sales
    </button>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue';
import { 
  CpuChipIcon, 
  Cog6ToothIcon, 
  BoltIcon, 
  WrenchScrewdriverIcon,
  AcademicCapIcon,
  ClockIcon,
  ChartBarIcon,
  DocumentTextIcon,
  CheckIcon
} from '@heroicons/vue/24/outline';

const props = defineProps<{
  title: string;
  oneLiner?: string;
  description: string;
  outcomes?: string[];
  startingPrice?: number;
  group?: string;
}>();

const iconMap: Record<string, any> = {
  'Integration': Cog6ToothIcon,
  'Automation': BoltIcon,
  'Services': CpuChipIcon,
  'Flexible': WrenchScrewdriverIcon,
  'Model Development': AcademicCapIcon,
  'Support': ClockIcon,
  'Analytics': ChartBarIcon,
};

const iconComponent = computed(() => {
  if (props.group && iconMap[props.group]) {
    return iconMap[props.group];
  }
  return DocumentTextIcon;
});

const formatPrice = (price: number): string => {
  return price.toLocaleString();
};
</script>
