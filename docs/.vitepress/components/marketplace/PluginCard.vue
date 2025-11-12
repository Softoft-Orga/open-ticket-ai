<template>
  <article class="flex flex-col gap-4 rounded-2xl border border-slate-800 bg-slate-950/60 p-5 shadow shadow-slate-900/40">
    <div class="flex items-start justify-between gap-4">
      <div class="space-y-1">
        <h3 class="text-lg font-semibold text-white">{{ plugin.name }}</h3>
        <p class="text-sm text-slate-300">{{ plugin.summary }}</p>
      </div>
      <span class="rounded-full bg-sky-500/20 px-3 py-1 text-xs font-semibold uppercase tracking-wide text-sky-200">
        v{{ plugin.version }}
      </span>
    </div>
    <div class="flex flex-wrap items-center gap-4 text-xs text-slate-300">
      <span class="flex items-center gap-1">
        <span aria-hidden="true">⭐</span>
        {{ plugin.starCount }}
      </span>
      <span class="flex items-center gap-1">
        Last release: {{ formattedDate }}
      </span>
      <span v-if="plugin.license" class="flex items-center gap-1">
        License: {{ plugin.license }}
      </span>
    </div>
    <div v-if="plugin.author" class="text-xs text-slate-400">
      Author: {{ plugin.author }}
    </div>
    <div class="flex flex-wrap gap-2 text-sm">
      <a
        :href="plugin.pypiUrl"
        class="inline-flex items-center justify-center gap-2 rounded-full border border-slate-700 px-3 py-1 text-slate-100 transition hover:border-sky-500 hover:text-sky-200"
        target="_blank"
        rel="noopener"
      >
        PyPI
      </a>
      <a
        v-if="plugin.repositoryUrl"
        :href="plugin.repositoryUrl"
        class="inline-flex items-center justify-center gap-2 rounded-full border border-slate-700 px-3 py-1 text-slate-100 transition hover:border-sky-500 hover:text-sky-200"
        target="_blank"
        rel="noopener"
      >
        Repository
      </a>
      <a
        v-if="plugin.homepage"
        :href="plugin.homepage"
        class="inline-flex items-center justify-center gap-2 rounded-full border border-slate-700 px-3 py-1 text-slate-100 transition hover:border-sky-500 hover:text-sky-200"
        target="_blank"
        rel="noopener"
      >
        Homepage
      </a>
    </div>
    <div class="rounded-xl bg-slate-900/80 px-3 py-2 font-mono text-xs text-slate-200">
      <span class="text-slate-500">pip install</span>
      {{ plugin.name }}
    </div>
  </article>
</template>

<script lang="ts" setup>
import type { Plugin } from "./pluginModels";

defineProps<{
  readonly plugin: Plugin;
  readonly formattedDate: string;
}>();
</script>
