<!-- Table.vue -->
<template>
    <div class="w-full overflow-x-auto rounded-2xl border border-slate-700">
        <table class="min-w-full text-sm text-slate-300 !m-0 !p-0">
            <tbody class="divide-y divide-slate-700">
            <slot/>
            </tbody>
        </table>
    </div>
</template>

<script lang="ts" setup>
import {provide, toRef, withDefaults} from 'vue'

const props = withDefaults(defineProps<{ striped?: boolean; dense?: boolean }>(), {
    striped: true,
    dense: false
})

provide('tableStriped', toRef(props, 'striped'))
provide('tableDense', toRef(props, 'dense'))
</script>
