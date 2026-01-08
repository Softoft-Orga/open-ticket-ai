<template>
  <div class="pipe-sidecar bg-vp-bg-soft border border-vp-border rounded-lg overflow-hidden">
    <!-- Header -->
    <div class="bg-vp-bg p-6 border-b border-vp-border">
      <div class="flex items-start justify-between">
        <div class="flex-1">
          <h2 class="text-2xl font-bold text-vp-text-1 mb-2">{{ sidecar._title }}</h2>
          <p class="text-vp-text-2 mb-3">{{ sidecar._summary }}</p>
          <div class="flex flex-wrap gap-2">
                        <span
                            class="inline-flex items-center px-3 py-1 rounded-full text-xs font-medium bg-vp-brand text-white">
                            {{ sidecar._category }}
                        </span>
            <span
                class="inline-flex items-center px-3 py-1 rounded-full text-xs font-medium bg-vp-bg-soft border border-vp-border text-vp-text-2">
                            {{ sidecar._version }}
                        </span>
          </div>
        </div>
        <div v-if="$slots.actions" class="ml-4">
          <slot name="actions"/>
        </div>
      </div>
    </div>

    <!-- Content -->
    <div class="p-6 space-y-6">
      <!-- Metadata Table -->
      <section>
        <h3 class="text-lg font-semibold text-vp-text-1 mb-3">Metadata</h3>
        <table class="w-full text-sm">
          <tbody>
          <tr v-for="item in metadataItems" :key="item.label" class="border-b border-vp-border">
            <td class="py-2 font-medium text-vp-text-2 w-32">{{ item.label }}</td>
            <td class="py-2 text-vp-text-1 font-mono text-xs">{{ item.value }}</td>
          </tr>
          </tbody>
        </table>
      </section>

      <!-- Inputs Table -->
      <section>
        <h3 class="text-lg font-semibold text-vp-text-1 mb-3">Inputs</h3>
        <table class="w-full text-sm">
          <tbody>
          <tr class="border-b border-vp-border">
            <td class="py-2 font-medium text-vp-text-2 w-32">Placement</td>
            <td class="py-2 text-vp-text-1">{{ sidecar._inputs.placement }}</td>
          </tr>
          <tr v-if="sidecar._inputs.alongside" class="border-b border-vp-border">
            <td class="py-2 font-medium text-vp-text-2 w-32">Alongside</td>
            <td class="py-2 text-vp-text-1">{{ sidecar._inputs.alongside.join(', ') }}</td>
          </tr>
          <tr v-if="sidecar._inputs.params" class="border-b border-vp-border">
            <td class="py-2 font-medium text-vp-text-2 w-32 align-top">Parameters</td>
            <td class="py-2">
              <div v-for="(desc, param) in sidecar._inputs.params" :key="param" class="flex gap-2 mb-1">
                <span class="font-mono text-xs text-vp-brand font-semibold">{{ param }}:</span>
                <span class="text-vp-text-1 text-xs">{{ desc }}</span>
              </div>
            </td>
          </tr>
          </tbody>
        </table>
      </section>

      <!-- Defaults Table -->
      <section v-if="sidecar._defaults && Object.keys(sidecar._defaults).length > 0">
        <h3 class="text-lg font-semibold text-vp-text-1 mb-3">Defaults</h3>
        <table class="w-full text-sm">
          <tbody>
          <tr v-for="(value, key) in sidecar._defaults" :key="key" class="border-b border-vp-border">
            <td class="py-2 font-mono text-xs text-vp-brand font-semibold w-48">{{ key }}</td>
            <td class="py-2 text-vp-text-1 text-xs">{{ value }}</td>
          </tr>
          </tbody>
        </table>
      </section>

      <!-- Output -->
      <section>
        <h3 class="text-lg font-semibold text-vp-text-1 mb-3">Output</h3>
        <div class="space-y-3">
          <p class="text-sm text-vp-text-2">{{ sidecar._output.description }}</p>
          <div class="flex flex-wrap gap-2">
                        <span
                            v-for="state in sidecar._output.state_enum"
                            :key="state"
                            :class="getStateClass(state)"
                            class="inline-flex items-center px-2 py-1 rounded text-xs font-mono"
                        >
                            {{ state }}
                        </span>
          </div>
          <div v-if="sidecar._output.payload_schema_ref" class="text-xs">
            <span class="font-medium text-vp-text-2">Schema:</span>
            <span class="ml-2 font-mono text-vp-text-1">{{ sidecar._output.payload_schema_ref }}</span>
          </div>
          <AccordionItem v-if="sidecar._output.examples" title="Output Examples">
            <table class="w-full text-xs">
              <tbody>
              <tr v-for="(example, state) in sidecar._output.examples" :key="state" class="border-b border-vp-border">
                <td class="py-2 font-semibold w-24">{{ state }}</td>
                <td class="py-2">
                  <pre class="text-xs">{{ JSON.stringify(example, null, 2) }}</pre>
                </td>
              </tr>
              </tbody>
            </table>
          </AccordionItem>
        </div>
      </section>

      <!-- Errors -->
      <section>
        <h3 class="text-lg font-semibold text-vp-text-1 mb-3">Errors</h3>
        <div class="space-y-3">
          <div v-for="(errors, type) in errorsByType" :key="type" :class="getErrorClass(type)"
               class="border rounded-lg p-3">
            <h4 class="font-semibold text-sm mb-2">{{ getErrorTitle(type) }}</h4>
            <ul class="space-y-1">
              <li v-for="(error, idx) in errors" :key="idx" class="text-xs">
                <span class="font-mono font-semibold">{{ error.code }}:</span>
                <span class="ml-2">{{ error.when }}</span>
              </li>
            </ul>
          </div>
        </div>
      </section>

      <!-- Engine Support Table -->
      <section>
        <h3 class="text-lg font-semibold text-vp-text-1 mb-3">Engine Support</h3>
        <table class="w-full text-sm">
          <tbody>
          <tr v-for="item in engineSupportItems" :key="item.label" class="border-b border-vp-border">
            <td class="py-2 font-medium text-vp-text-2 w-32">{{ item.label }}</td>
            <td class="py-2">
                                <span
                                    :class="item.supported ? 'bg-green-100 dark:bg-green-900/30 text-green-800 dark:text-green-300' : 'bg-gray-100 dark:bg-gray-800 text-gray-600 dark:text-gray-400'"
                                    class="inline-flex items-center px-2 py-1 rounded text-xs font-semibold"
                                >
                                    {{ item.supported ? 'Supported' : 'Not Supported' }}
                                </span>
            </td>
          </tr>
          </tbody>
        </table>
      </section>

      <!-- Examples -->
      <section>
        <h3 class="text-lg font-semibold text-vp-text-1 mb-3">Usage Examples</h3>
        <AccordionItem v-for="(example, name) in sidecar._examples" :key="name" :title="name">
          <pre class="text-xs overflow-x-auto bg-vp-bg-soft p-4 rounded border border-vp-border"><code>{{
              example
            }}</code></pre>
        </AccordionItem>
      </section>
    </div>
  </div>
</template>

<script lang="ts" setup>
import {computed} from 'vue'
import AccordionItem from '../core/accordion/AccordionItem.vue'
import type {PipeSidecar} from './pipeSidecar.types'

const props = defineProps<{
  sidecar: PipeSidecar
}>()

const metadataItems = computed(() => [
  {label: 'Class', value: props.sidecar._class},
  {label: 'Extends', value: props.sidecar._extends},
])

const engineSupportItems = computed(() => [
  {label: 'On Failure', supported: props.sidecar._engine_support.on_failure},
  {label: 'On Success', supported: props.sidecar._engine_support.on_success},
])

const errorsByType = computed(() => {
  const result: Record<string, any[]> = {}
  if (props.sidecar._errors.fail) result.fail = props.sidecar._errors.fail
  if (props.sidecar._errors.break) result.break = props.sidecar._errors.break
  if (props.sidecar._errors.continue) result.continue = props.sidecar._errors.continue
  return result
})

const getStateClass = (state: string): string => {
  switch (state.toLowerCase()) {
    case 'ok':
      return 'bg-green-100 dark:bg-green-900/30 text-green-800 dark:text-green-300'
    case 'failed':
      return 'bg-red-100 dark:bg-red-900/30 text-red-800 dark:text-red-300'
    case 'skipped':
      return 'bg-yellow-100 dark:bg-yellow-900/30 text-yellow-800 dark:text-yellow-300'
    default:
      return 'bg-gray-100 dark:bg-gray-800 text-gray-600 dark:text-gray-400'
  }
}

const getErrorClass = (type: string): string => {
  switch (type) {
    case 'fail':
      return 'bg-red-50 dark:bg-red-950/20 border-red-200 dark:border-red-800'
    case 'break':
      return 'bg-orange-50 dark:bg-orange-950/20 border-orange-200 dark:border-orange-800'
    case 'continue':
      return 'bg-yellow-50 dark:bg-yellow-950/20 border-yellow-200 dark:border-yellow-800'
    default:
      return ''
  }
}

const getErrorTitle = (type: string): string => {
  switch (type) {
    case 'fail':
      return 'Fail (Pipeline Stops)'
    case 'break':
      return 'Break (Pipeline Interrupted)'
    case 'continue':
      return 'Continue (Skipped, Pipeline Continues)'
    default:
      return type
  }
}
</script>

<style scoped>
.pipe-sidecar {
  max-width: 100%;
}
</style>
