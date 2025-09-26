<template>
  <div class="my-8">
    <h2 class="!mb-6 !text-2xl font-bold text-center">{{ title }}</h2>
    <div class="grid gap-6 grid-cols-1 xl:grid-cols-3 ">
      <ProductCard
        v-for="product in products"
        :key="product.name"
        :product="product"
        class="md:px-16 md:max-w-sm w-full md:mx-auto lg:max-w-md xl:max-w-none xl:px-0 xl:mx-0"
      />
    </div>
  </div>
</template>

<script setup lang="ts">
import ProductCard from './ProductCard.vue'
import {Product} from "./product.types";

const props = defineProps<{
  products: Product[]
  title: string
}>()
</script>
