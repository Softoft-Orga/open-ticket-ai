<template>
  <a 
    :href="href"
    :class="[
      'group flex items-center justify-between rounded-lg px-4 py-3 text-sm font-medium transition-all',
      active 
        ? 'bg-primary/20 text-primary-light border border-primary/30' 
        : 'text-gray-400 hover:bg-surface-lighter hover:text-white border border-transparent'
    ]"
  >
    <div class="flex items-center gap-3">
      <component
        :is="heroIcon"
        class="w-5 h-5"
      />
      <span>{{ label }}</span>
    </div>
    <span 
      v-if="count !== undefined" 
      :class="[
        'rounded-full px-2.5 py-0.5 text-xs font-bold transition-colors',
        active 
          ? 'bg-primary/30 text-primary-light' 
          : 'bg-surface-lighter text-text-dim group-hover:bg-primary/20 group-hover:text-primary'
      ]"
    >
      {{ count }}
    </span>
  </a>
</template>

<script setup lang="ts">
import { computed } from 'vue';
import { 
  Squares2X2Icon, 
  RocketLaunchIcon, 
  CodeBracketIcon, 
  LightBulbIcon, 
  ShieldCheckIcon 
} from '@heroicons/vue/24/outline';

interface Props {
  icon: string;
  label: string;
  count?: number;
  active?: boolean;
  href?: string;
}

const props = withDefaults(defineProps<Props>(), {
  active: false,
  href: '#'
});

const iconMap: Record<string, any> = {
  'grid_view': Squares2X2Icon,
  'rocket_launch': RocketLaunchIcon,
  'code': CodeBracketIcon,
  'lightbulb': LightBulbIcon,
  'security': ShieldCheckIcon,
};

const heroIcon = computed(() => iconMap[props.icon] || Squares2X2Icon);
</script>
