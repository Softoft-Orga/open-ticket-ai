<template>
  <div class="flex flex-wrap gap-2">
    <Badge
      v-for="tag in tags"
      :key="tag"
      class="text-xs"
    >
      {{ tag }}
    </Badge>
  </div>
</template>

<script lang="ts" setup>
import Badge from '../core/basic/Badge.vue'

const {tags} = defineProps<{ tags: string[] }>()
</script>
