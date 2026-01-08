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
      <span class="material-symbols-outlined text-xl">{{ icon }}</span>
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
interface Props {
  icon: string;
  label: string;
  count?: number;
  active?: boolean;
  href?: string;
}

withDefaults(defineProps<Props>(), {
  active: false,
  href: '#'
});
</script>
