<script lang="ts" setup>
import {ref} from 'vue'

const loaded = ref(false)
</script>

<template>
  <div v-if="!loaded" class="absolute inset-0 flex items-center justify-center h-[80vh]">
    <span class="animate-pulse text-lg">Loading...</span>
  </div>
  <div class="flex justify-center mb-4 w-full h-[80vh] relative">

    <iframe
        height="100%"
        src="https://app.terrastruct.com/diagrams/1810325889"
        title="Open_Ticket_AI"
        width="100%"
        @load="loaded = true"
    />
  </div>
</template>
