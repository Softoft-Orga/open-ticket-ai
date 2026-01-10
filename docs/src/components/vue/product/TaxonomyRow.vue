<template>
  <div 
    class="flex items-center justify-between py-4 border-b border-border-dark/30"
    :class="{ 'bg-primary/5': active }"
  >
    <div class="flex items-center gap-4">
      <div 
        class="w-2 h-2 rounded-full"
        :class="[
          level === 1 ? 'bg-primary ml-0' : '',
          level === 2 ? 'bg-cyan-glow ml-6' : '',
          level === 3 ? 'bg-purple-400 ml-12' : '',
          level === 4 ? 'bg-pink-400 ml-16' : ''
        ]"
      ></div>
      <span 
        class="font-mono text-sm"
        :class="active ? 'text-white font-bold' : 'text-text-dim'"
      >
        {{ label }}
      </span>
    </div>
    <div class="flex gap-2 flex-wrap justify-end">
      <Badge 
        v-for="(tag, idx) in tags" 
        :key="idx"
        :type="active ? 'primary' : 'secondary'"
      >
        {{ tag }}
      </Badge>
    </div>
  </div>
</template>

<script setup lang="ts">
import Badge from '../core/basic/Badge.vue'

defineProps<{
  level: number
  label: string
  tags: string[]
  active?: boolean
}>()
</script>
