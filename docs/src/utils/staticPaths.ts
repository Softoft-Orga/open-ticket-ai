import type { CollectionEntry, CollectionKey } from 'astro:content'
import { getCollection } from 'astro:content'

type StaticPath = {
  params: { slug: string[] }
  props: { id: string }
}

const stripLocalePrefix = (id: string) => id.replace(/^([a-z]{2}(?:-[A-Z]{2})?)\//i, '')

export const getLocalizedCatchAllStaticPaths = async <T extends CollectionKey>(
  collection: T,
): Promise<StaticPath[]> => {
  const entries = await getCollection(collection)

  return (entries as CollectionEntry<T>[]).map((entry) => ({
    params: {
      slug: stripLocalePrefix(entry.id).split('/').filter(Boolean),
    },
    props: { id: entry.id },
  }))
}
