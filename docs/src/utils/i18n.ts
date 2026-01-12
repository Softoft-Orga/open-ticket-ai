import { getCollection, getEntry, type CollectionKey, type CollectionEntry } from 'astro:content'

const extractLocaleFromId = (id: string): string | null => {
  const m = id.match(/^([a-z]{2}(?:-[A-Z]{2})?)\//)
  return m ? m[1] : null
}

export const createLocalizedContent = (locale: string, fallbackLocale = 'en') => {
    const target = (locale || fallbackLocale).toLowerCase()

    const getLocalizedCollection = async <T extends CollectionKey>(
        collection: T,
    ): Promise<CollectionEntry<T>[]> => {
        const all = await getCollection(collection)
        return all.filter((e) => {
            const l = extractLocaleFromId(e.id)
            if (!l) return true
            return l.toLowerCase() === target
        })
    }

    const getLocalizedEntry = async <T extends CollectionKey>(
        collection: T,
        id: string,
    ): Promise<CollectionEntry<T> | undefined> => {
        const withLocale = `${target}/${id}`
        const direct = await getEntry(collection, withLocale as any)
        if (direct) {
            return direct
        }
        if (target !== fallbackLocale.toLowerCase()) {
            const fb = `${fallbackLocale}/${id}`
            return getEntry(collection, fb as any)
        }
        return undefined
    }

    const getLocalizedSingleton = async <T extends CollectionKey>(
        collection: T,
    ): Promise<CollectionEntry<T> | undefined> => {
        const items = await getLocalizedCollection(collection)
        return items[0]
    }

    return { getLocalizedCollection, getLocalizedEntry, getLocalizedSingleton }
}
