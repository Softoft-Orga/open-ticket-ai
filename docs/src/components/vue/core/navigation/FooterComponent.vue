<template>
  <footer class="border-t border-white/5 bg-background-dark py-24">
    <div class="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
      <div class="mb-16 grid grid-cols-1 gap-12 md:grid-cols-4">
        <div class="md:col-span-1">
          <div class="mb-6 flex items-center gap-2">
            <div class="flex size-8 items-center justify-center rounded bg-link/20 text-link">
              <TicketIcon class="h-5 w-5" />
            </div>
            <span class="font-display text-lg font-bold tracking-tight text-white">{{
              brandName
            }}</span>
          </div>
          <p class="max-w-xs text-sm leading-relaxed text-slate-500">
            {{ brandTagline }}
          </p>
        </div>

        <div v-for="(section, index) in sections" :key="index">
          <h4 class="mb-6 text-sm font-bold uppercase tracking-widest text-white">
            {{ section.title }}
          </h4>
          <ul class="space-y-4 text-sm text-slate-500">
            <li v-for="(link, linkIndex) in section.links" :key="linkIndex">
              <a :href="link.url" class="text-primary transition-colors hover:text-primary-light">{{
                link.label
              }}</a>
            </li>
          </ul>
        </div>

        <div v-if="social.length > 0">
          <h4 class="mb-6 text-sm font-bold uppercase tracking-widest text-white">
            {{ socialHeading }}
          </h4>
          <div class="flex gap-4 text-primary">
            <a
              v-for="(socialLink, index) in social"
              :key="index"
              :href="socialLink.url"
              :aria-label="socialLink.ariaLabel"
              class="transition-colors hover:text-primary-light"
            >
              <SocialIcon :platform="socialLink.platform" />
            </a>
          </div>
        </div>
      </div>

      <div
        class="flex flex-col items-center justify-between gap-6 border-t border-white/5 pt-8 md:flex-row"
      >
        <div class="text-xs text-slate-600">© {{ year }} {{ copyright }}</div>
        <div v-if="legal.length > 0" class="flex gap-8 text-xs text-primary">
          <a
            v-for="(legalLink, index) in legal"
            :key="index"
            :href="legalLink.url"
            class="transition-colors hover:text-primary-light"
            >{{ legalLink.label }}</a
          >
        </div>
      </div>
    </div>
  </footer>
</template>

<script lang="ts" setup>
import { computed } from 'vue';
import { TicketIcon } from '@heroicons/vue/24/outline';
import SocialIcon from '../icons/SocialIcon.vue';

type FooterLink = {
  label: string;
  url: string;
};

type FooterSection = {
  title: string;
  links: FooterLink[];
};

type SocialLink = {
  platform: 'github' | 'linkedin' | 'youtube' | 'huggingface';
  url: string;
  ariaLabel: string;
};

type FooterData = {
  brandName?: string;
  brandTagline?: string;
  socialHeading?: string;
  sections: FooterSection[];
  social: SocialLink[];
  legal: FooterLink[];
  copyright: string;
};

type Props = {
  footerData?: FooterData;
};

const props = defineProps<Props>();

const sections = computed(() => props.footerData?.sections || []);
const social = computed(() => props.footerData?.social || []);
const legal = computed(() => props.footerData?.legal || []);
const copyright = computed(
  () => props.footerData?.copyright || 'Open Ticket AI UG. All rights reserved.'
);
const brandName = computed(() => props.footerData?.brandName || 'Open Ticket AI');
const brandTagline = computed(
  () =>
    props.footerData?.brandTagline ||
    'Intelligent automation for OTRS, Znuny, and Zammad. German Engineering.'
);
const socialHeading = computed(() => props.footerData?.socialHeading || 'Connect');
const year = computed(() => new Date().getFullYear());
</script>
