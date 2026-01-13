import type { CollectionEntry, CollectionKey } from 'astro:content'
import { getCollection } from 'astro:content'

type StaticPath<T extends CollectionKey> = {
  params: { slug: string | undefined }
  props: { entry: CollectionEntry<T> }
}

const stripLocalePrefix = (id: string) => id.replace(/^([a-z]{2}(?:-[A-Z]{2})?)\//i, '')
const stripFileExtension = (id: string) => id.replace(/\.(md|mdx)$/, '')
const stripIndex = (id: string) => id.replace(/\/?index$/, '')

export const getLocalizedCatchAllStaticPaths = async <T extends CollectionKey>(
  collection: T,
): Promise<StaticPath<T>[]> => {
  const entries = await getCollection(collection)

  return (entries as CollectionEntry<T>[]).map((entry) => {
    const cleanId = stripIndex(stripFileExtension(stripLocalePrefix(entry.id)))
    return {
      params: {
        slug: cleanId || undefined,
      },
      props: { entry },
    }
  })
}
