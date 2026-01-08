<!-- Row.vue -->
<template>
  <tr :class="[striped ? 'odd:bg-slate-900 even:bg-slate-800' : '', 'hover:bg-slate-700/40']">
    <slot/>
  </tr>
</template>

<script lang="ts" setup>
import {inject} from 'vue'

const striped = inject('tableStriped', false) as boolean
</script>
