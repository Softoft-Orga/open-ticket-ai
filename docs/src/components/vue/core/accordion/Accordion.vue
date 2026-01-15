<template>
  <div :class="containerClasses">
    <!-- Items-based rendering with slot support -->
    <template v-if="items && items.length > 0">
      <AccordionItem
        v-for="(it, i) in items"
        :id="it.id || `item-${i}`"
        :key="it.id || i"
        :title="it.title"
        :default-open="isItemOpen(it.id || `item-${i}`)"
        :variant="variant"
        :disabled="it.disabled"
      >
        <!-- Custom title slot -->
        <template #title="{ open }">
          <slot name="title" :item="it" :index="i" :open="open">
            <span class="text-lg font-semibold text-white">{{ it.title }}</span>
          </slot>
        </template>

        <!-- Content slot -->
        <template #default="{ open }">
          <slot :item="it" :index="i" :open="open">
            {{ it.content }}
          </slot>
        </template>
      </AccordionItem>
    </template>

    <!-- Manual composition: render slot content directly -->
    <template v-else>
      <slot />
    </template>
  </div>
</template>

<script lang="ts" setup>
import { computed, provide, ref, watch } from 'vue';
import AccordionItem from './AccordionItem.vue';

type Variant = 'default' | 'ghost' | 'bordered' | 'gradient';

interface Item {
  id?: string;
  title: string;
  content?: string;
  defaultOpen?: boolean;
  disabled?: boolean;
}

interface Props {
  items?: Item[];
  variant?: Variant;
  multiple?: boolean;
  modelValue?: string[] | string;
}

const props = withDefaults(defineProps<Props>(), {
  items: undefined,
  variant: 'default',
  multiple: false,
  modelValue: undefined,
});

const emit = defineEmits<{
  'update:modelValue': [value: string[] | string];
}>();

// Internal state for open items
const openItems = ref<Set<string>>(new Set());

// Initialize open items from modelValue or defaultOpen
const initializeOpenItems = () => {
  if (props.modelValue !== undefined) {
    // Use modelValue if provided
    if (Array.isArray(props.modelValue)) {
      openItems.value = new Set(props.modelValue);
    } else if (props.modelValue) {
      openItems.value = new Set([props.modelValue]);
    }
  } else if (props.items) {
    // Otherwise use defaultOpen from items
    const defaultOpenIds = props.items
      .filter(item => item.defaultOpen)
      .map((item, i) => item.id || `item-${i}`);
    openItems.value = new Set(defaultOpenIds);
  }
};

// Initialize on mount
initializeOpenItems();

// Watch modelValue changes
watch(
  () => props.modelValue,
  newValue => {
    if (newValue !== undefined) {
      if (Array.isArray(newValue)) {
        openItems.value = new Set(newValue);
      } else if (newValue) {
        openItems.value = new Set([newValue]);
      } else {
        openItems.value = new Set();
      }
    }
  },
  { deep: true }
);

// Check if an item is open
const isItemOpen = (itemId: string) => {
  return openItems.value.has(itemId);
};

// Provide accordion context for manual composition
provide('accordion', {
  variant: computed(() => props.variant),
  multiple: computed(() => props.multiple),
  toggleItem: (itemId: string) => {
    const newOpenItems = new Set(openItems.value);

    if (newOpenItems.has(itemId)) {
      newOpenItems.delete(itemId);
    } else {
      if (!props.multiple) {
        newOpenItems.clear();
      }
      newOpenItems.add(itemId);
    }

    openItems.value = newOpenItems;

    // Emit update:modelValue
    if (props.multiple) {
      emit('update:modelValue', Array.from(newOpenItems));
    } else {
      emit('update:modelValue', newOpenItems.size > 0 ? Array.from(newOpenItems)[0] : '');
    }
  },
});

const containerClasses = computed(() => {
  const variants = {
    default: 'divide-y divide-border-dark',
    ghost: 'space-y-1',
    bordered: '',
    gradient: '',
  };

  return variants[props.variant];
});
</script>
