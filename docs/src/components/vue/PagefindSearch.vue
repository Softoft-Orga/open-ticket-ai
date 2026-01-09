<template>
  <div>
    <button
      @click="openModal"
      class="w-full max-w-2xl mx-auto relative group flex items-center bg-card-dark rounded-2xl border border-slate-700 shadow-2xl overflow-hidden cursor-pointer hover:border-primary/50 transition-colors"
      aria-label="Search documentation"
      aria-haspopup="dialog"
    >
      <div class="pl-6 text-slate-500">
        <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24" aria-hidden="true" focusable="false">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
        </svg>
      </div>
      <div class="w-full bg-transparent border-none text-white placeholder:text-slate-600 h-16 px-4 text-lg flex items-center text-left text-slate-600">
        Search documentation (e.g., 'API keys', 'YAML config')...
      </div>
      <div class="hidden sm:flex pr-6 text-xs text-slate-600 font-mono tracking-widest">
        CMD + K
      </div>
    </button>

    <Teleport to="body">
      <div
        v-if="isOpen"
        class="fixed inset-0 z-50 flex items-start justify-center pt-16 px-4"
        role="dialog"
        aria-modal="true"
        aria-label="Search documentation"
        @click="closeModal"
      >
        <div class="fixed inset-0 bg-black/60 backdrop-blur-sm"></div>
        <div
          class="relative w-full max-w-3xl bg-[#1a1a1a] rounded-2xl shadow-2xl border border-slate-700 overflow-hidden"
          @click.stop
        >
          <div ref="searchContainer" class="pagefind-search"></div>
        </div>
      </div>
    </Teleport>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, onUnmounted, watch, nextTick } from 'vue';

interface PagefindUIInstance {
  destroy?: () => void;
}

const isOpen = ref(false);
const searchContainer = ref<HTMLElement | null>(null);
let pagefindUI: PagefindUIInstance | null = null;

const openModal = () => {
  isOpen.value = true;
};

const closeModal = () => {
  isOpen.value = false;
};

const handleKeydown = (e: KeyboardEvent) => {
  if ((e.metaKey || e.ctrlKey) && e.key === 'k') {
    e.preventDefault();
    openModal();
  }
  if (e.key === 'Escape' && isOpen.value) {
    closeModal();
  }
};

onMounted(() => {
  window.addEventListener('keydown', handleKeydown);
});

onUnmounted(() => {
  window.removeEventListener('keydown', handleKeydown);
  
  // Cleanup pagefindUI instance
  if (pagefindUI?.destroy) {
    pagefindUI.destroy();
    pagefindUI = null;
  }
});

watch(isOpen, async (newValue) => {
  if (newValue && searchContainer.value) {
    if (!pagefindUI) {
      try {
        // Load the pagefind UI script and CSS
        const pagefindCss = '/pagefind/pagefind-ui.css';
        
        if (!document.querySelector(`link[href="${pagefindCss}"]`)) {
          const link = document.createElement('link');
          link.rel = 'stylesheet';
          link.href = pagefindCss;
          document.head.appendChild(link);
        }
        
        // Load the pagefind UI script if not already loaded
        if (!(window as any).PagefindUI) {
          const script = document.createElement('script');
          script.src = '/pagefind/pagefind-ui.js';
          
          // Wait for the script to load, with error handling and timeout
          await new Promise<void>((resolve, reject) => {
            const timeoutId = window.setTimeout(() => {
              script.onload = null;
              script.onerror = null;
              reject(new Error('Timed out while loading Pagefind UI script.'));
            }, 15000);

            script.onload = () => {
              window.clearTimeout(timeoutId);
              script.onload = null;
              script.onerror = null;
              resolve();
            };

            script.onerror = () => {
              window.clearTimeout(timeoutId);
              script.onload = null;
              script.onerror = null;
              reject(new Error('Failed to load Pagefind UI script.'));
            };

            document.head.appendChild(script);
          });
        }
        
        // Initialize PagefindUI
        const PagefindUI = (window as any).PagefindUI;
        pagefindUI = new PagefindUI({
          element: searchContainer.value,
          showSubResults: true,
          showImages: false,
          resetStyles: false,
        });

        // Focus the search input after initialization
        await nextTick();
        const searchInput = searchContainer.value?.querySelector('.pagefind-ui__search-input') as HTMLInputElement;
        if (searchInput) {
          searchInput.focus();
        }
      } catch (error) {
        console.error('Failed to load Pagefind UI:', error);
      }
    } else {
      // If pagefindUI already exists, just focus the search input
      await nextTick();
      const searchInput = searchContainer.value?.querySelector('.pagefind-ui__search-input') as HTMLInputElement;
      if (searchInput) {
        searchInput.focus();
      }
    }
  }
});
</script>

<style>
.pagefind-search {
  --pagefind-ui-scale: 1;
  --pagefind-ui-primary: #7c4dff;
  --pagefind-ui-text: #ffffff;
  --pagefind-ui-background: #1a1a1a;
  --pagefind-ui-border: #333;
  --pagefind-ui-tag: #333;
  --pagefind-ui-border-width: 1px;
  --pagefind-ui-border-radius: 8px;
  --pagefind-ui-image-border-radius: 8px;
  --pagefind-ui-image-box-ratio: 3 / 2;
  --pagefind-ui-font: inherit;
}

:deep(.pagefind-ui__search-input) {
  background: #2a2a2a;
  color: white;
  border: 1px solid #333;
  padding: 12px 16px;
  font-size: 16px;
}

:deep(.pagefind-ui__search-input:focus) {
  border-color: #7c4dff;
  outline: none;
}

:deep(.pagefind-ui__result) {
  background: #2a2a2a;
  border: 1px solid #333;
  padding: 16px;
  margin-bottom: 12px;
  border-radius: 8px;
}

:deep(.pagefind-ui__result:hover) {
  background: #333;
  border-color: #7c4dff;
}

:deep(.pagefind-ui__result-title) {
  color: #7c4dff;
  font-weight: 600;
}

:deep(.pagefind-ui__result-excerpt) {
  color: #d1d5db;
}

:deep(.pagefind-ui__message) {
  color: #9ca3af;
}
</style>
