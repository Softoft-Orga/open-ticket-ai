<template>
  <div class="grid gap-6 md:grid-cols-2">
    <ExampleCard
      v-for="example in props.examples"
      :key="example.slug ?? example.name"
      :example="example"
      :exampleLink="'#' + example.slug ?? example.name"
    />
    <p
      v-if="!props.examples.length"
      class="col-span-full rounded-lg border border-[var(--vp-c-divider)] bg-[var(--vp-c-bg-soft)] p-6 text-center text-[var(--vp-c-text-2)]"
    >
      No examples match your filters yet. Try clearing the search or picking a different tag.
    </p>
  </div>
</template>

<script lang="ts" setup>
import ExampleCard from './ExampleCard.vue'
import type {ExampleMeta} from '../../composables/useConfigExamplesRegistry'

const props = defineProps<{ examples: ExampleMeta[] }>()
</script>
