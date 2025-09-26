<template>
  <div>
    <div class="flex border-b border-vp-border">
      <button
        v-for="(label, idx) in tabs"
        :key="idx"
        @click="active = idx"
        :class="[
          'px-4 py-2 -mb-px',
          active === idx
            ? 'border-b-2 text-vp-brand border-vp-brand'
            : 'text-vp-text-2'
        ]"
      >
        {{ label }}
      </button>
    </div>
    <div class="mt-4">
      <slot :name="`tab-${active}`" />
    </div>
  </div>
</template>

<script lang="ts" setup>
import { ref } from 'vue'

const props = defineProps<{ tabs: string[] }>()
const active = ref(0)
</script>
