<script lang="ts" setup>
var __VUE_PROD_DEVTOOLS__ = false

import {computed} from 'vue'
import {useI18n} from 'vue-i18n'
import ProductCards from './ProductCards.vue'

const {t} = useI18n()

// servicePackages is now a computed property to be reactive to language changes
const servicePackages = computed(() => [
  {
    name: t('servicePackages.essential.name'),
    price: 2000,
    description: t('servicePackages.essential.description'),
    features: [
      {text: t('servicePackages.features.coreInstall'), icon: 'fa-rocket'},
      {text: t('servicePackages.features.standardModel'), icon: 'fa-brain'},
      {text: t('servicePackages.features.prioEngine'), icon: 'fa-sort-amount-up'},
      {text: t('servicePackages.features.queueClassification'), icon: 'fa-sitemap'},
    ]
  },
  {
    name: t('servicePackages.professional.name'),
    price: 5000,
    description: t('servicePackages.professional.description'),
    features: [
      {text: t('servicePackages.features.coreInstall'), icon: 'fa-rocket'},
      {text: t('servicePackages.features.trainingQueue'), icon: 'fa-brain'},
      {text: t('servicePackages.features.trainingPrio'), icon: 'fa-brain'},
      {text: t('servicePackages.features.prioEngine'), icon: 'fa-sort-amount-up'},
      {text: t('servicePackages.features.queueClassification'), icon: 'fa-sitemap'},
    ]
  },
  {
    name: t('servicePackages.enterprise.name'),
    price: 12000,
    description: t('servicePackages.enterprise.description'),
    features: [
      {text: t('servicePackages.features.coreInstall'), icon: 'fa-rocket'},
      {text: t('servicePackages.features.trainingQueue'), icon: 'fa-brain'},
      {text: t('servicePackages.features.trainingPrio'), icon: 'fa-brain'},
      {text: t('servicePackages.features.prioEngine'), icon: 'fa-sort-amount-up'},
      {text: t('servicePackages.features.queueClassification'), icon: 'fa-sitemap'},
      {text: t('servicePackages.features.thirdPartyIntegration'), icon: 'fa-project-diagram'},
      {text: t('servicePackages.features.customAttributePrediction'), icon: 'fa-magic'},
      {
        text: t('servicePackages.features.additionalAttributePrediction'),
        icon: 'fa-plus-circle'
      },
      {text: t('servicePackages.features.bespokeDevelopment'), icon: 'fa-code-branch'},
    ]
  }
]);


</script>

<template>
  <ProductCards
      :buttonText="t('servicePackages.buttonText')"
      :products="servicePackages"
      :title="t('servicePackages.title')"
  />
</template>

<style scoped>
/* Your styles here */
</style>
