<script setup lang="ts">
import DefaultTheme from 'vitepress/theme'
import RecentNewsToast from '../components/RecentNewsToast.vue'

const {Layout: DefaultLayout} = DefaultTheme
</script>

<template>
  <DefaultLayout>
    <template #layout-top>
      <RecentNewsToast/>
    </template>
  </DefaultLayout>
</template>
