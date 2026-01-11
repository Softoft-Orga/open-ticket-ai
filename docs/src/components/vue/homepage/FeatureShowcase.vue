<template>
  <section class="w-full px-4 md:px-10 lg:px-20 xl:px-40 py-24 bg-background-dark">
    <div class="w-full max-w-7xl mx-auto">
      <Card 
        background="surface-dark" 
        padding="lg" 
        hoverable
        class="relative overflow-hidden"
      >
        <!-- Decorative glow effect -->
        <div class="absolute -right-20 -top-20 w-96 h-96 bg-secondary/10 rounded-full blur-[100px]" />

        <div class="flex flex-col lg:flex-row gap-16 items-center">
          <!-- Image/Visual Side -->
          <Transition
            enter-active-class="transition-all duration-500 ease-out motion-reduce:transition-none motion-reduce:transform-none"
            enter-from-class="opacity-0 -translate-x-8"
            enter-to-class="opacity-100 translate-x-0"
          >
            <div
              v-if="mounted"
              class="w-full lg:w-1/2 order-2 lg:order-1 z-10"
            >
              <div class="relative group">
                <div class="absolute -inset-1 bg-gradient-to-r from-primary to-secondary rounded-xl blur opacity-20 group-hover:opacity-40 transition duration-1000" />
                <Card
                  background="surface-dark"
                  padding="none"
                  class="relative"
                >
                  <img 
                    v-if="imageSrc" 
                    :src="imageSrc" 
                    :alt="imageAlt || title"
                    class="w-full h-auto"
                  >
                  <div
                    v-else
                    class="w-full aspect-video bg-gradient-to-br from-primary/20 to-secondary/20 flex items-center justify-center"
                  >
                    <component
                      :is="iconComponent"
                      class="w-24 h-24 text-primary/50"
                    />
                  </div>
                </Card>
              </div>
            </div>
          </Transition>

          <!-- Content Side -->
          <Transition
            enter-active-class="transition-all duration-500 ease-out delay-100 motion-reduce:transition-none motion-reduce:transform-none"
            enter-from-class="opacity-0 translate-x-8"
            enter-to-class="opacity-100 translate-x-0"
          >
            <div
              v-if="mounted"
              class="w-full lg:w-1/2 flex flex-col gap-6 order-1 lg:order-2 z-10"
            >
              <Badge
                v-if="badge"
                type="primary"
                class="w-fit uppercase tracking-wider"
              >
                {{ badge }}
              </Badge>
              
              <h2 class="font-display text-4xl font-bold text-white leading-tight">
                {{ title }}
              </h2>
              
              <p class="text-text-dim text-xl leading-relaxed">
                {{ description }}
              </p>

              <div
                v-if="features && features.length > 0"
                class="flex flex-col gap-3 mt-4"
              >
                <Transition
                  v-for="(feature, idx) in features"
                  :key="idx"
                  :enter-active-class="`transition-all duration-300 ease-out motion-reduce:transition-none motion-reduce:transform-none delay-[${200 + idx * 50}ms]`"
                  enter-from-class="opacity-0 translate-y-2"
                  enter-to-class="opacity-100 translate-y-0"
                >
                  <div 
                    v-if="mounted"
                    class="flex items-start gap-3 hover:translate-x-1 transition-transform duration-200"
                  >
                    <div class="w-6 h-6 rounded-full bg-primary/20 flex items-center justify-center flex-shrink-0 mt-1">
                      <CheckIcon class="w-4 h-4 text-primary" />
                    </div>
                    <div class="flex flex-col gap-1">
                      <span class="text-white font-semibold">{{ feature.title }}</span>
                      <span
                        v-if="feature.description"
                        class="text-text-dim text-sm"
                      >{{ feature.description }}</span>
                    </div>
                  </div>
                </Transition>
              </div>

              <div
                v-if="ctaText"
                class="flex items-center gap-2 text-primary font-bold text-lg cursor-pointer group hover:text-white transition-colors mt-4"
              >
                <span>{{ ctaText }}</span>
                <ArrowRightIcon
                  class="w-6 h-6 transition-transform group-hover:translate-x-1"
                  aria-hidden="true"
                />
              </div>
            </div>
          </Transition>
        </div>
      </Card>
    </div>
  </section>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue';
import { ArrowRightIcon, CheckIcon } from '@heroicons/vue/24/outline';
import { CpuChipIcon } from '@heroicons/vue/24/outline';
import Card from '../core/basic/Card.vue';
import Badge from '../core/basic/Badge.vue';

interface Feature {
  title: string;
  description?: string;
}

const props = defineProps<{
  badge?: string;
  title: string;
  description: string;
  features?: Feature[];
  imageSrc?: string;
  imageAlt?: string;
  ctaText?: string;
}>();

console.log(props)

const iconComponent = computed(() => CpuChipIcon);
const mounted = ref(false);

onMounted(() => {
  // Trigger transitions on mount
  mounted.value = true;
});
</script>
