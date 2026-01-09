<template>
  <div class="rounded-xl border border-surface-lighter bg-surface-dark p-6">
    <div class="flex gap-4">
      <img
        v-if="avatar"
        :src="avatar"
        :alt="name"
        class="size-16 rounded-full border-2 border-primary/30 object-cover"
      />
      <div v-else class="flex size-16 items-center justify-center rounded-full border-2 border-primary/30 bg-primary/20 text-primary">
        <span class="material-symbols-outlined text-2xl">person</span>
      </div>
      <div class="flex-1">
        <h4 class="mb-1 text-lg font-bold text-white">{{ name }}</h4>
        <p v-if="role" class="mb-2 text-sm text-primary-light">{{ role }}</p>
        <p class="mb-3 text-sm leading-relaxed text-gray-400">{{ bio }}</p>
        <div v-if="social" class="flex gap-3">
          <a
            v-if="social.twitter"
            :href="social.twitter"
            target="_blank"
            rel="noopener noreferrer"
            class="text-text-dim transition-colors hover:text-primary-light"
            aria-label="Twitter"
          >
            <span class="material-symbols-outlined text-xl">X</span>
          </a>
          <a
            v-if="social.github"
            :href="social.github"
            target="_blank"
            rel="noopener noreferrer"
            class="text-text-dim transition-colors hover:text-primary-light"
            aria-label="GitHub"
          >
            <span class="material-symbols-outlined text-xl">code</span>
          </a>
          <a
            v-if="social.linkedin"
            :href="social.linkedin"
            target="_blank"
            rel="noopener noreferrer"
            class="text-text-dim transition-colors hover:text-primary-light"
            aria-label="LinkedIn"
          >
            <span class="material-symbols-outlined text-xl">business_center</span>
          </a>
        </div>
      </div>
    </div>
  </div>
</template>

<script lang="ts" setup>
interface Social {
  twitter?: string
  github?: string
  linkedin?: string
}

interface Props {
  name: string
  role?: string
  bio: string
  avatar?: string
  social?: Social
}

defineProps<Props>()
</script>
