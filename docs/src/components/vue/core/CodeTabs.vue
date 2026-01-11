<template>
  <div class="rounded-xl border border-surface-lighter bg-surface-dark overflow-hidden">
    <div class="flex border-b border-surface-lighter bg-background-dark">
      <button
        v-for="(tab, index) in tabs"
        :key="index"
        :class="[
          'relative px-6 py-3 text-sm font-medium transition-all',
          activeTab === index
            ? 'text-white'
            : 'text-text-dim hover:text-white'
        ]"
        @click="activeTab = index"
      >
        {{ tab }}
        <div
          v-if="activeTab === index"
          class="absolute bottom-0 left-0 right-0 h-0.5 bg-primary"
        />
      </button>
    </div>
    <div class="p-6">
      <slot :name="`tab-${activeTab}`" />
    </div>
  </div>
</template>

<script lang="ts" setup>
import { ref } from 'vue'

interface Props {
  tabs: string[]
  defaultTab?: number
}

const props = withDefaults(defineProps<Props>(), {
  defaultTab: 0
})

const activeTab = ref(props.defaultTab)
</script>
