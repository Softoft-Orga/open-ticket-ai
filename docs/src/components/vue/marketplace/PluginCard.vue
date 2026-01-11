<template>
  <Card
    variant="primary"
    size="md"
    radius="2xl"
    elevation="sm"
  >
    <template #header>
      <div class="flex items-start justify-between gap-4">
        <div class="flex-1 space-y-2">
          <h3 class="text-lg font-semibold text-white">
            {{ plugin.name }}
          </h3>
          <p class="text-sm text-text-dim min-h-[5rem]">
            {{ plugin.summary }}
          </p>
        </div>
        <span class="shrink-0 rounded-full bg-info/20 px-3 py-1 text-xs font-semibold uppercase tracking-wide text-info border border-info/30">
          v{{ plugin.version }}
        </span>
      </div>
    </template>

    <div class="space-y-3">
      <div class="flex flex-wrap items-center gap-4 text-xs text-text-dim">
        <span class="flex items-center gap-1.5">
          <StarIcon class="w-4 h-4" />
          {{ plugin.starCount }}
        </span>
        <span class="flex items-center gap-1.5">
          <ClockIcon class="w-4 h-4" />
          Last release: {{ formattedDate }}
        </span>
        <span
          v-if="plugin.license"
          class="flex items-center gap-1.5"
        >
          <DocumentTextIcon class="w-4 h-4" />
          License: {{ plugin.license }}
        </span>
      </div>
      
      <div
        v-if="plugin.author"
        class="text-xs text-text-dim flex items-center gap-1.5"
      >
        <UserIcon class="w-4 h-4" />
        Author: {{ plugin.author }}
      </div>
    </div>

    <template #actions>
      <div class="flex flex-wrap gap-2">
        <a
          :href="plugin.pypiUrl"
          target="_blank"
          rel="noopener"
          class="inline-block"
        >
          <Button
            variant="outline"
            size="sm"
            radius="2xl"
          >
            <CubeIcon class="w-4 h-4 mr-2" />
            PyPI
          </Button>
        </a>
        <a
          v-if="plugin.repositoryUrl"
          :href="plugin.repositoryUrl"
          target="_blank"
          rel="noopener"
          class="inline-block"
        >
          <Button
            variant="outline"
            size="sm"
            radius="2xl"
          >
            <CodeBracketIcon class="w-4 h-4 mr-2" />
            Repository
          </Button>
        </a>
        <a
          v-if="plugin.homepage"
          :href="plugin.homepage"
          target="_blank"
          rel="noopener"
          class="inline-block"
        >
          <Button
            variant="outline"
            size="sm"
            radius="2xl"
          >
            <GlobeAltIcon class="w-4 h-4 mr-2" />
            Homepage
          </Button>
        </a>
      </div>
    </template>

    <template #footer>
      <div class="rounded-xl bg-surface-lighter px-4 py-2.5 font-mono text-xs text-white border border-border-dark">
        <span class="text-text-dim">pip install</span>
        <span class="ml-1">{{ plugin.name }}</span>
      </div>
    </template>
  </Card>
</template>

<script lang="ts" setup>
import type { Plugin } from "./pluginModels";
import Card from "../core/basic/Card.vue";
import Button from "../core/basic/Button.vue";
import { 
  StarIcon, 
  ClockIcon, 
  DocumentTextIcon, 
  UserIcon,
  CubeIcon,
  CodeBracketIcon,
  GlobeAltIcon 
} from '@heroicons/vue/24/outline';

defineProps<{
  readonly plugin: Plugin;
  readonly formattedDate: string;
}>();
</script>
