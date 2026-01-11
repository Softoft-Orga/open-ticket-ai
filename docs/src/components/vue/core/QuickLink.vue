<template>
  <a
    class="group flex flex-col items-center gap-3 p-6 bg-slate-900/30 rounded-xl border border-slate-800 hover:border-primary/40 hover:bg-slate-900/50 transition-all duration-300"
    href="#"
  >
    <div class="w-12 h-12 rounded-lg bg-primary/5 flex items-center justify-center group-hover:bg-primary/10 transition-colors">
      <component
        :is="getIcon(icon)"
        class="w-6 h-6 text-primary"
      />
    </div>
    <span class="text-sm font-medium text-slate-300 group-hover:text-white transition-colors text-center">{{ label }}</span>
  </a>
</template>

<script lang="ts" setup>
import { RocketLaunchIcon, ShieldCheckIcon, WrenchScrewdriverIcon, ClockIcon } from '@heroicons/vue/24/outline';

const props = defineProps<{
  icon: string;
  label: string;
}>();

console.log(props)

const iconMap: Record<string, any> = {
  'rocket': RocketLaunchIcon,
  'shield': ShieldCheckIcon,
  'wrench': WrenchScrewdriverIcon,
  'clock': ClockIcon,
};

const getIcon = (iconName: string) => {
  return iconMap[iconName] || RocketLaunchIcon;
};
</script>
