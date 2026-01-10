<template>
  <Card>
    <!-- Header -->
    <template #header>
      <span class="text-sm font-semibold text-text-dim uppercase tracking-wide">
        {{ heading }}
      </span>
    </template>

    <!-- Main content -->
    <slot/>

    <!-- Footer -->
    <template #footer>
      <div class="flex items-center gap-2 text-sm">
        <span class="text-text-dim">Confidence:</span>
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

const {heading, confidence} = props
</script>
