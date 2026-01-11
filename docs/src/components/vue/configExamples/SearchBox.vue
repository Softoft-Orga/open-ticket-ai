<template>
  <label class="block w-full max-w-sm">
    <span class="sr-only">Search examples</span>
    <input
      :value="props.value"
      class="w-full h-12 px-4 text-base rounded-xl bg-surface-dark border border-primary/40 text-white placeholder:text-text-dim hover:border-primary/60 hover:shadow-[0_0_15px_rgba(166,13,242,0.2)] focus:ring-2 focus:ring-primary/50 focus:border-primary focus:outline-none active:border-primary active:ring-primary/60 shadow-sm transition-colors duration-200"
      placeholder="Search examples…"
      type="text"
      @input="event => emit('update:value', (event.target as HTMLInputElement).value)"
    >
  </label>
</template>

<script lang="ts" setup>
const props = defineProps<{ value: string }>()
const emit = defineEmits<{ 'update:value': [value: string] }>()
</script>
