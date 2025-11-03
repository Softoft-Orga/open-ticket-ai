<template>
  <label class="block w-full max-w-sm">
    <span class="sr-only">Search examples</span>
    <TextField
      :model-value="props.value"
      placeholder="Search examples…"
      @update:model-value="value => emit('update:value', value)"
    />
  </label>
</template>

<script lang="ts" setup>
import TextField from '../core/forms/TextField.vue'

const props = defineProps<{ value: string }>()
const emit = defineEmits<{ 'update:value': [value: string] }>()
</script>
