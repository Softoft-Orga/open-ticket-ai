<template>
  <div class="space-y-4">
    <div class="flex items-center gap-4">
      <div
        v-for="(step, index) in steps"
        :key="index"
        class="flex flex-1 items-center gap-4"
      >
        <div class="flex flex-col items-center gap-2">
          <div
            :class="[
              'flex size-10 items-center justify-center rounded-full border-2 font-bold transition-all',
              currentStep > index
                ? 'border-emerald-500 bg-emerald-500 text-white'
                : currentStep === index
                ? 'border-primary bg-primary text-white'
                : 'border-surface-lighter bg-surface-dark text-text-dim'
            ]"
          >
            <CheckIcon v-if="currentStep > index" class="w-5 h-5" aria-hidden="true" />
            <span v-else>{{ index + 1 }}</span>
          </div>
          <span
            :class="[
              'text-xs font-medium',
              currentStep >= index ? 'text-white' : 'text-text-dim'
            ]"
          >
            {{ step }}
          </span>
        </div>
        <div
          v-if="index < steps.length - 1"
          :class="[
            'h-0.5 flex-1 transition-all',
            currentStep > index ? 'bg-emerald-500' : 'bg-surface-lighter'
          ]"
        ></div>
      </div>
    </div>
  </div>
</template>

<script lang="ts" setup>
import { CheckIcon } from '@heroicons/vue/24/outline'

interface Props {
  steps: string[]
  currentStep: number
}

defineProps<Props>()
</script>
