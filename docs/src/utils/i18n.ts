import { getCollection } from 'astro:content';
import type { CollectionEntry } from 'astro:content';
import { i18n } from 'astro:config/server';

function extractLocaleFromId(id: string): string | null {
  // Match locale codes like 'en', 'de', 'en-US', case-insensitive
  const match = id.match(/^([a-z]{2}(-[A-Z]{2})?)\//i);
  return match ? match[1].toLowerCase() : null;
}

function getDefaultLocale(): string {
  if (!i18n) return 'en';
  return i18n.defaultLocale || 'en';
}

export async function getLocalizedCollection<T extends 'products' | 'services' | 'site'>(
  collection: T,
  locale?: string
): Promise<CollectionEntry<T>[]> {
  const allEntries = await getCollection(collection);
  
  const targetLocale = locale || getDefaultLocale();
  
  return allEntries.filter(entry => {
    const entryLocale = extractLocaleFromId(entry.id);
    return entryLocale === targetLocale;
  });
}

export async function getLocalizedSiteConfig(locale?: string) {
  const siteEntries = await getLocalizedCollection('site', locale);
  return siteEntries.find(entry => entry.data.slug === 'main');
}

export async function getLocalizedProducts(locale?: string) {
  return getLocalizedCollection('products', locale);
}

export async function getLocalizedServices(locale?: string) {
  return getLocalizedCollection('services', locale);
}
