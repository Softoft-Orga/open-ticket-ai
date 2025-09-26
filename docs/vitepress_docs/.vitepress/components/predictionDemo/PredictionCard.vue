<template>
  <Card>
    <!-- Header -->
    <template #header>
      <span class="text-lg font-medium text-gray-500 dark:text-gray-400">
        {{ heading }}
      </span>
    </template>

    <!-- Main content -->
    <div class="min-h-14">
      <slot />
    </div>

    <!-- Footer -->
    <template #footer>
      <div class="text-md text-gray-900 dark:text-gray-100">
        Confidence:
        <Badge :type="badgeClass(confidence)">
          {{ asPercent(confidence) }}
        </Badge>
      </div>
    </template>
  </Card>
</template>

<script lang="ts" setup>
import Card from '../core/basic/Card.vue'
import Badge from '../core/basic/Badge.vue'

const props = defineProps<{
  heading: string
  confidence: number
}>()

function asPercent(s: number) {
  return `${(s * 100).toFixed(1)}%`
}

function badgeClass(s: number) {
  const p = s * 100
  if (p > 90) return 'success'
  if (p > 80) return 'secondary'
  if (p > 50) return 'warning'
  return 'danger'
}

const { heading, confidence } = props
</script>
