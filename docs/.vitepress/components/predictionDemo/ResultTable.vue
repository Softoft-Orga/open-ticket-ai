<template>
    <div v-if="queueResult && prioResult" class="mt-6">
        <span class="text-2xl font-semibold text-center text-vp-text my-6">
            {{ t('otai_prediction_demo_component.resultTitle') }}
        </span>

        <div class="grid grid-cols-1 gap-6 md:grid-cols-2 mt-5">
            <PredictionCard :confidence="queueResult[0].score"
                            :heading="t('otai_prediction_demo_component.queueRowHeader')">
                <span class="flex-1 text-xl font-bold text-gray-900 dark:text-gray-100 mb-1">
                        {{ mainQueue }}
                </span>
                <br/>
                <span class="flex-1 text-md font-bold text-gray-900 dark:text-gray-100 mb-4">
                        > {{ subQueue }}
                </span>
            </PredictionCard>
            <PredictionCard :confidence="prioResult[0].score"
                            :heading="t('otai_prediction_demo_component.priorityRowHeader')">
                <span class="flex-1 text-xl font-bold text-gray-900 dark:text-gray-100 mb-1">
                    {{ prioResult[0].label }}
                </span>
            </PredictionCard>
        </div>
    </div>
</template>

<script lang="ts" setup>
import {computed} from 'vue'
import {useI18n} from 'vue-i18n'
import PredictionCard from "./PredictionCard.vue";

const {queueResult, prioResult} = defineProps<{
    queueResult: { label: string; score: number }[] | null
    prioResult: { label: string; score: number }[] | null
}>()

const {t} = useI18n()

function asPercent(s: number) {
    return `${(s * 100).toFixed(1)}%`
}

const mainQueue = computed(() => {
    if (!queueResult || queueResult.length === 0) return null
    return queueResult[0].label.split('/')[0]
})

const subQueue = computed(() => {
    if (!queueResult || queueResult.length === 0) return null
    const parts = queueResult[0].label.split('/')
    return parts.length > 1 ? parts.slice(1).join('/') : null
})

function badgeClass(s: number) {
    const p = s * 100
    if (p > 90) return 'success'
    if (p > 80) return 'secondary'
    if (p > 50) return 'warning'
    return 'danger'
}
</script>
