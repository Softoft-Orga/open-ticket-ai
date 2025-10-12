<template>
    <!-- Render only header and body; no nested Accordion -->
    <div class="space-y-2 border-gray-700 rounded">
        <div class="flex items-center space-x-2 cursor-pointer">
            <Badge v-if="func.is_async" type="warning">async</Badge>
            <span class="font-mono font-bold text-lg">
                <h3 class="inline">{{ func.name }}</h3>
                <span class="text-gray-200">{{ func.signature }}</span>
            </span>
        </div>
        <div class="mt-2">
            <Docstring :doc="func.docstring"/>
        </div>
    </div>
</template>

<script lang="ts" setup>
import type {FunctionData} from '../../composables/useApiDocs'
import Badge from '../core/basic/Badge.vue'
import Docstring from './Docstring.vue'

defineProps<{ func: FunctionData }>()
</script>
