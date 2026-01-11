<template>
  <div :class="cardClasses">
    <div class="mb-6">
      <h4 class="text-white text-xl font-bold font-display">
        {{ title }}
      </h4>
      <p
        v-if="subtitle"
        class="text-primary text-xs font-bold uppercase mt-1"
      >
        {{ subtitle }}
      </p>
    </div>
    <div class="mb-8">
      <div class="text-slate-400 text-sm mb-1 uppercase tracking-widest font-bold">
        from
      </div>
      <div class="text-3xl font-bold text-white font-display">
        {{ price }} <span class="text-sm font-normal text-slate-500">{{ priceSuffix }}</span>
      </div>
    </div>
    <ul class="space-y-3 mb-10 flex-grow">
      <li
        v-for="(feature, index) in features"
        :key="index"
        class="flex items-start gap-2.5 text-sm text-slate-300"
      >
        <CheckIcon
          class="w-5 h-5 text-primary flex-shrink-0 mt-0.5"
          aria-hidden="true"
        />
        <span>{{ feature }}</span>
      </li>
    </ul>
    <Button 
      :variant="highlighted ? 'primary' : 'outline'" 
      size="md"
      class="w-full"
      data-service-modal-trigger
      :data-service="serviceKey"
    >
      {{ buttonText }}
    </Button>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue';
import { CheckIcon } from '@heroicons/vue/24/outline';
import Button from '../core/basic/Button.vue';

const props = withDefaults(defineProps<{
  title: string;
  subtitle?: string;
  price: string;
  features: string[];
  badge?: string;
  highlighted?: boolean;
  buttonText?: string;
  priceSuffix?: string;
  serviceKey?: string;
}>(), {
  highlighted: false,
  buttonText: 'Contact Sales',
  priceSuffix: '',
  serviceKey: ''
});

const cardClasses = computed(() => {
  const base = 'flex flex-col rounded-2xl p-8 transition-all h-full';
  if (props.highlighted) {
    return `${base} bg-[#1a1033] border-2 border-primary shadow-[0_0_30px_rgba(166,13,242,0.2)]`;
  }
  return `${base} bg-[#150c19] border border-white/5 hover:border-white/20`;
});
</script>
