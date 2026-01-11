<template>
  <Card
    background="surface-dark"
    padding="default"
  >
    <div class="flex gap-4">
      <img
        v-if="avatar"
        :src="avatar"
        :alt="name"
        class="size-16 rounded-full border-2 border-primary/30 object-cover"
      >
      <div
        v-else
        class="flex size-16 items-center justify-center rounded-full border-2 border-primary/30 bg-primary/20 text-primary"
      >
        <UserIcon
          class="w-8 h-8"
          aria-hidden="true"
        />
      </div>
      <div class="flex-1">
        <h4 class="mb-1 text-lg font-bold text-white">
          {{ name }}
        </h4>
        <p
          v-if="role"
          class="mb-2 text-sm text-primary-light"
        >
          {{ role }}
        </p>
        <p class="mb-3 text-sm leading-relaxed text-gray-400">
          {{ bio }}
        </p>
        <div
          v-if="social"
          class="flex gap-3"
        >
          <a
            v-if="social.twitter"
            :href="social.twitter"
            target="_blank"
            rel="noopener noreferrer"
            class="text-text-dim transition-colors hover:text-primary-light"
            aria-label="Twitter"
          >
            <svg
              class="w-5 h-5"
              fill="currentColor"
              viewBox="0 0 24 24"
              aria-hidden="true"
            >
              <path d="M18.244 2.25h3.308l-7.227 8.26 8.502 11.24H16.17l-5.214-6.817L4.99 21.75H1.68l7.73-8.835L1.254 2.25H8.08l4.713 6.231zm-1.161 17.52h1.833L7.084 4.126H5.117z" />
            </svg>
          </a>
          <a
            v-if="social.github"
            :href="social.github"
            target="_blank"
            rel="noopener noreferrer"
            class="text-text-dim transition-colors hover:text-primary-light"
            aria-label="GitHub"
          >
            <CodeBracketIcon
              class="w-5 h-5"
              aria-hidden="true"
            />
          </a>
          <a
            v-if="social.linkedin"
            :href="social.linkedin"
            target="_blank"
            rel="noopener noreferrer"
            class="text-text-dim transition-colors hover:text-primary-light"
            aria-label="LinkedIn"
          >
            <BriefcaseIcon
              class="w-5 h-5"
              aria-hidden="true"
            />
          </a>
        </div>
      </div>
    </div>
  </Card>
</template>

<script lang="ts" setup>
import Card from '../core/basic/Card.vue'
import { UserIcon, CodeBracketIcon, BriefcaseIcon } from '@heroicons/vue/24/outline'

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
