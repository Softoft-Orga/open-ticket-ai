import type { CollectionEntry, CollectionKey } from 'astro:content';
import { getCollection } from 'astro:content';

type StaticPath<T extends CollectionKey> = {
  params: { slug: string | undefined };
  props: { entry: CollectionEntry<T> };
};

const stripLocalePrefix = (id: string) => id.replace(/^([a-z]{2}(?:-[A-Z]{2})?)\//i, '');
const stripFileExtension = (id: string) => id.replace(/\.(md|mdx)$/, '');
const stripIndex = (id: string) => id.replace(/\/?index$/, '');

/**
 * Filters blog posts to exclude drafts and posts with future release dates
 */
export const filterPublishedBlogPosts = (
  posts: CollectionEntry<'blog'>[]
): CollectionEntry<'blog'>[] => {
  const now = new Date();
  return posts.filter(({ data }) => {
    // Filter out drafts
    if (data.draft) return false;
    // Filter out posts with futureReleaseDate that is in the future
    if (data.futureReleaseDate && data.futureReleaseDate > now) return false;
    return true;
  });
};

export const getLocalizedCatchAllStaticPaths = async <T extends CollectionKey>(
  collection: T
): Promise<StaticPath<T>[]> => {
  const entries = await getCollection(collection);
  const now = new Date();

  // Filter out future-dated blog posts
  const filteredEntries = (entries as CollectionEntry<T>[]).filter(entry => {
    // Only apply futureReleaseDate filtering to blog collection
    if (collection === 'blog') {
      const blogEntry = entry as CollectionEntry<'blog'>;
      // Filter out posts with futureReleaseDate that is in the future
      if (blogEntry.data.futureReleaseDate && blogEntry.data.futureReleaseDate > now) {
        return false;
      }
    }
    return true;
  });

  return filteredEntries.map(entry => {
    const cleanId = stripIndex(stripFileExtension(stripLocalePrefix(entry.id)));
    return {
      params: {
        slug: cleanId || undefined,
      },
      props: { entry },
    };
  });
};
