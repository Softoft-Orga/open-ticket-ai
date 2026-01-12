/// <reference types="astro/client" />

import type {CollectionEntry, CollectionKey} from 'astro:content'

type LocalizedContentApi = {
    getLocalizedCollection: <T extends CollectionKey>(collection: T) => Promise<CollectionEntry<T>[]>
    getLocalizedEntry: <T extends CollectionKey>(collection: T, id: string) => Promise<CollectionEntry<T> | undefined>
    getLocalizedSingleton: <T extends CollectionKey>(collection: T) => Promise<CollectionEntry<T> | undefined>
}

declare namespace App {
    interface Locals {
        locale: string
        content: LocalizedContentApi
    }
}
