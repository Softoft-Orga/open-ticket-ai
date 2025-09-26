<script lang="ts" setup>
var __VUE_PROD_DEVTOOLS__ = false

import {computed} from 'vue'
import {useI18n} from 'vue-i18n'
import ProductCards from './ProductCards.vue' // Assuming ProductCards component is in the same directory

const {t} = useI18n()

// supportPlans is now a computed property for reactivity
const supportPlans = computed(() => [
    {
        name: t('supportPlans.basic.name'),
        price: 250,
        pricePeriod: t('supportPlans.pricePeriod'),
        description: t('supportPlans.basic.description'),
        features: [
            {text: t('supportPlans.features.systemUpdates'), icon: 'fa-sync-alt'},
            {text: t('supportPlans.features.uptimeMonitoring'), icon: 'fa-chart-line'},
            {text: t('supportPlans.features.monthlyHealthCheck'), icon: 'fa-calendar-check'},
            {text: t('supportPlans.features.responseTime'), icon: 'fa-clock'},
        ],
    },
    {
        name: t('supportPlans.proactive.name'),
        price: 500,
        pricePeriod: t('supportPlans.pricePeriod'),
        description: t('supportPlans.proactive.description'),
        features: [
            {text: t('supportPlans.features.allBasic'), icon: 'fa-star'},
            {text: t('supportPlans.features.weeklyMonitoring'), icon: 'fa-tachometer-alt'},
            {text: t('supportPlans.features.monthlyReports'), icon: 'fa-file-alt'},
            {text: t('supportPlans.features.priorityResponse'), icon: 'fa-clock'},
        ],
    },
    {
        name: t('supportPlans.enterprise.name'),
        price: 2500,
        pricePeriod: t('supportPlans.pricePeriod'),
        description: t('supportPlans.enterprise.description'),
        features: [
            {text: t('supportPlans.features.allProactive'), icon: 'fa-star'},
            {text: t('supportPlans.features.realtimeAlerts'), icon: 'fa-bell'},
            {text: t('supportPlans.features.strategicReview'), icon: 'fa-chart-bar'},
            {text: t('supportPlans.features.guaranteedResponse'), icon: 'fa-clock'},
        ],
    },
]);

</script>

<template>
    <ProductCards
        :buttonText="t('supportPlans.buttonText')"
        :products="supportPlans"
        :title="t('supportPlans.title')"
    />
</template>

<style scoped>

</style>
