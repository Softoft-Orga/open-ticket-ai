<script setup lang="ts">
import DefaultTheme from 'vitepress/theme'
import RecentNewsToast from '../components/RecentNewsToast.vue'

const {Layout: DefaultLayout} = DefaultTheme
</script>

<template>
  <DefaultLayout>
    <template #home-hero-before>
      <RecentNewsToast/>
    </template>
    <template #doc-top>
      <RecentNewsToast class="mb-4"/>
    </template>
  </DefaultLayout>
</template>
