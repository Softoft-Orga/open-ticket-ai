<template>
  <section class="pagefind-wrapper">
    <div class="pagefind-prompt">
      <div aria-hidden="true" class="pagefind-icon">
        <MagnifyingGlassIcon class="w-5 h-5" />
      </div>
      <div class="pagefind-hint">
        <p class="text-sm text-slate-400 font-semibold">Search documentation</p>
        <p class="text-xs text-slate-500">Try “API keys”, “deployment”, or “YAML config”.</p>
      </div>
      <span class="pagefind-shortcut">CMD ⌘ K</span>
    </div>

    <div ref="searchContainer" class="pagefind-search" />

    <p v-if="error" class="pagefind-error">{{ error }}</p>
  </section>
</template>

<script setup lang="ts">
import { ref, onMounted, onUnmounted } from 'vue';
import { MagnifyingGlassIcon } from '@heroicons/vue/24/outline';

type PagefindGlobal = {
  new: (config: { element: HTMLElement; showImages?: boolean; showSubResults?: boolean }) => { destroy?: () => void };
};

type PagefindUIInstance = ReturnType<PagefindGlobal['new']> | null;

const searchContainer = ref<HTMLElement | null>(null);
const error = ref<string | null>(null);
let pagefindInstance: PagefindUIInstance = null;

onMounted(async () => {
  try {
    await loadPagefindAssets();
    if (searchContainer.value && (window as any).PagefindUI) {
      const PagefindUI = (window as any).PagefindUI as PagefindGlobal;
      pagefindInstance = new PagefindUI({
        element: searchContainer.value,
        showImages: false,
        showSubResults: false,
      });
    }
  } catch (err) {
    error.value = err instanceof Error ? err.message : 'Unable to load search right now.';
  }
});

onUnmounted(() => {
  pagefindInstance?.destroy?.();
  pagefindInstance = null;
});

async function loadPagefindAssets() {
  if ((window as any).PagefindUI) return;

  const cssHref = '/pagefind/pagefind-ui.css';
  if (!document.querySelector(`link[href="${cssHref}"]`)) {
    const link = document.createElement('link');
    link.rel = 'stylesheet';
    link.href = cssHref;
    document.head.appendChild(link);
  }

  await new Promise<void>((resolve, reject) => {
    const script = document.createElement('script');
    script.src = '/pagefind/pagefind-ui.js';
    script.onload = () => resolve();
    script.onerror = () => reject(new Error('Could not load Pagefind script.'));
    document.head.appendChild(script);
  });
}
</script>

<style>
.pagefind-wrapper {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.pagefind-prompt {
  display: flex;
  align-items: center;
  gap: 1rem;
  background: rgba(255, 255, 255, 0.02);
  border: 1px solid rgba(255, 255, 255, 0.08);
  border-radius: 1rem;
  padding: 1rem 1.5rem;
}

.pagefind-icon {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 2.5rem;
  height: 2.5rem;
  border-radius: 999px;
  background: rgba(166, 13, 242, 0.1);
  color: #a60df2;
}

.pagefind-shortcut {
  margin-left: auto;
  font-size: 0.75rem;
  color: #94a3b8;
  border: 1px solid rgba(148, 163, 184, 0.3);
  padding: 0.35rem 0.65rem;
  border-radius: 999px;
}

.pagefind-error {
  color: #f87171;
  font-size: 0.875rem;
}

:deep(.pagefind-search) {
  --pagefind-ui-scale: 1;
  --pagefind-ui-primary: #a60df2;
  --pagefind-ui-text: #ffffff;
  --pagefind-ui-background: #110616;
  --pagefind-ui-border: #2d1b36;
  --pagefind-ui-border-width: 1px;
  --pagefind-ui-border-radius: 1rem;
  --pagefind-ui-font: 'Inter', system-ui, -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
}

:deep(.pagefind-ui__result) {
  background: rgba(255, 255, 255, 0.02);
  border: 1px solid rgba(255, 255, 255, 0.05);
}
</style>
