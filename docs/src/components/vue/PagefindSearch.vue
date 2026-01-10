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
let pagefindLoadPromise: Promise<void> | null = null;

const PAGEFIND_SCRIPT_ID = 'pagefind-ui-script';
const PAGEFIND_STYLES_SELECTOR = 'link[data-pagefind-ui="true"]';

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
  if (pagefindLoadPromise) {
    return pagefindLoadPromise;
  }

  ensurePagefindStyles();

  pagefindLoadPromise = new Promise<void>((resolve, reject) => {
    const existingScript = document.getElementById(PAGEFIND_SCRIPT_ID) as HTMLScriptElement | null;
    if (existingScript) {
      existingScript.addEventListener('load', () => resolve(), { once: true });
      existingScript.addEventListener('error', () => reject(new Error('Could not load Pagefind script.')), { once: true });
      return;
    }

    const script = document.createElement('script');
    script.id = PAGEFIND_SCRIPT_ID;
    script.src = '/pagefind/pagefind-ui.js';
    script.onload = () => resolve();
    script.onerror = () => reject(new Error('Could not load Pagefind script.'));
    document.head.appendChild(script);
  });

  return pagefindLoadPromise;
}

function ensurePagefindStyles() {
  if (document.querySelector(PAGEFIND_STYLES_SELECTOR)) return;
  const link = document.createElement('link');
  link.rel = 'stylesheet';
  link.href = '/pagefind/pagefind-ui.css';
  link.dataset.pagefindUi = 'true';
  document.head.appendChild(link);
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
  background: rgba(29, 16, 35, 0.6);
  border: 1px solid #3c2249;
  border-radius: 1rem;
  padding: 1rem 1.5rem;
  backdrop-filter: blur(10px);
  transition: all 0.3s ease;
}

.pagefind-prompt:hover {
  border-color: #a60df2;
  box-shadow: 0 0 20px rgba(166, 13, 242, 0.2);
}

.pagefind-icon {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 2.5rem;
  height: 2.5rem;
  border-radius: 999px;
  background: linear-gradient(135deg, rgba(166, 13, 242, 0.2), rgba(0, 240, 255, 0.1));
  color: #d475fd;
  transition: all 0.3s ease;
}

.pagefind-prompt:hover .pagefind-icon {
  box-shadow: 0 0 15px rgba(166, 13, 242, 0.4);
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
  --pagefind-ui-text: #e6e7ea;
  --pagefind-ui-background: rgba(29, 16, 35, 0.6);
  --pagefind-ui-border: #3c2249;
  --pagefind-ui-border-width: 1px;
  --pagefind-ui-border-radius: 1rem;
  --pagefind-ui-font: 'Inter', system-ui, -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
}

:deep(.pagefind-ui__result) {
  background: rgba(29, 16, 35, 0.4);
  border: 1px solid rgba(60, 34, 73, 0.5);
  transition: all 0.3s ease;
}

:deep(.pagefind-ui__result:hover) {
  background: rgba(29, 16, 35, 0.7);
  border-color: #a60df2;
  box-shadow: 0 0 20px rgba(166, 13, 242, 0.3);
}

:deep(.pagefind-ui__result-title),
:deep(.pagefind-ui__result-excerpt) {
  color: #e6e7ea !important;
}

:deep(.pagefind-ui__result-link) {
  color: #e6e7ea !important;
}

:deep(.pagefind-ui__result-link:hover) {
  color: #d475fd !important;
}

:deep(mark) {
  background: rgba(166, 13, 242, 0.3) !important;
  color: #d475fd !important;
  padding: 0.1em 0.2em;
  border-radius: 0.25rem;
  font-weight: 600;
}

:deep(.pagefind-ui__message) {
  color: #b790cb !important;
}

:deep(.pagefind-ui__search-input) {
  background: rgba(29, 16, 35, 0.6) !important;
  border: 1px solid #3c2249 !important;
  color: #e6e7ea !important;
  padding: 0.875rem 1.25rem !important;
  font-size: 0.95rem !important;
}

:deep(.pagefind-ui__search-input::placeholder) {
  color: #b790cb !important;
}

:deep(.pagefind-ui__search-input:focus) {
  border-color: #a60df2 !important;
  box-shadow: 0 0 0 3px rgba(166, 13, 242, 0.1), 0 0 20px rgba(166, 13, 242, 0.2) !important;
  outline: none !important;
}
</style>
