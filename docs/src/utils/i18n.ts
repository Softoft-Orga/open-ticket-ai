import { getCollection } from 'astro:content';
import type { CollectionEntry } from 'astro:content';

type LocaleCode = 'en' | 'de';

function extractLocaleFromId(id: string): LocaleCode | null {
  const match = id.match(/^([a-z]{2})\//);
  return match ? (match[1] as LocaleCode) : null;
}

export async function getLocalizedCollection<T extends 'products' | 'services' | 'site'>(
  collection: T,
  locale?: LocaleCode
): Promise<CollectionEntry<T>[]> {
  const allEntries = await getCollection(collection);
  
  const targetLocale = locale || 'en';
  
  return allEntries.filter(entry => {
    const entryLocale = extractLocaleFromId(entry.id);
    return entryLocale === targetLocale;
  });
}

export async function getLocalizedSiteConfig(locale?: LocaleCode) {
  const siteEntries = await getLocalizedCollection('site', locale);
  return siteEntries.find(entry => entry.data.slug === 'main');
}

export async function getLocalizedProducts(locale?: LocaleCode) {
  return getLocalizedCollection('products', locale);
}

export async function getLocalizedServices(locale?: LocaleCode) {
  return getLocalizedCollection('services', locale);
}
