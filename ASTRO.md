# Astro Documentation Summary

This document contains the most important information about Astro 5, gathered from the official Astro documentation.

## What is Astro?

Astro is an all-in-one web framework for building fast, content-focused websites. It's designed to help everyone succeed in building sites with a powerful developer experience and lightweight output.

## Core Concepts

### Islands Architecture

Astro pioneered and popularized the **Islands Architecture** pattern - a component-based web architecture optimized for content-driven websites.

**How it works:**
- Renders the majority of your page to fast, static HTML
- Adds smaller "islands" of JavaScript only when interactivity or personalization is needed (e.g., image carousels)
- Avoids monolithic JavaScript payloads that slow down page responsiveness
- Ships **zero JavaScript by default** to minimize what slows your site down

**Benefits:**
- UI-agnostic framework support (React, Preact, Svelte, Vue, Solid, HTMX, web components, and more)
- Server-first approach moves expensive rendering off visitors' devices
- Optimized for content-driven websites

### Output Modes

Astro supports two build output modes:

1. **Static Mode (`output: 'static'`)** - Default mode
   - Prerenders all pages at build time
   - Generates a static site

2. **Server Mode (`output: 'server'`)** - SSR mode
   - Renders pages on-demand using server-side rendering
   - Can opt-in individual pages to prerendering with `export const prerender = true`

**Configuration example:**
```javascript
import { defineConfig } from 'astro/config';

export default defineConfig({
  output: 'static'
})
```

## Routing System

### File-Based Routing

Astro uses **file-based routing** - no separate routing configuration needed!

**How it works:**
- Every file in `src/pages/` automatically becomes a route
- File paths map directly to URLs
- Supports `.astro`, `.md`, and `.mdx` files

**Examples:**
```
src/pages/index.astro        -> mysite.com/
src/pages/about.astro        -> mysite.com/about
src/pages/about/index.astro  -> mysite.com/about
src/pages/about/me.astro     -> mysite.com/about/me
src/pages/posts/1.md         -> mysite.com/posts/1
```

### Dynamic Routes

For dynamic routes, use bracket notation in filenames (e.g., `[post].astro`) and implement `getStaticPaths()`:

```astro
--- 
// In 'server' mode, opt in to prerendering:
// export const prerender = true

export async function getStaticPaths() {
  return [
    { params: { post: '1' } }, // Creates /blog/1
    { params: { post: '2' } }, // Creates /blog/2
  ];
}
--- 
<!-- Your HTML template here. -->
```

## Layouts

Layouts are reusable Astro components for common page structures:

```astro
---
import Layout from '../layouts/Layout.astro';
const pagePathname = Astro.url.pathname
---
<Layout title="Home Page" pathname={pagePathname}>
    <p>Astro</p>
</Layout>
```

## Content Collections

Content collections are the **best way to manage sets of content** in Astro projects.

### Benefits

- Organize and query documents efficiently
- Enable Intellisense and type checking in your editor
- Provide **automatic TypeScript type-safety** for all content
- Performant and scalable with the Content Layer API (introduced in Astro v5.0)

### Defining Collections

Use Zod schemas for type-safe content validation:

```typescript
import { defineCollection } from 'astro:content';
import { glob, file } from 'astro/loaders';
import { z } from 'astro/zod';

const blog = defineCollection({
  loader: glob({ pattern: "**/*.md", base: "./src/data/blog" }),
  schema: z.object({
    title: z.string(),
    description: z.string(),
    pubDate: z.coerce.date(),
    updatedDate: z.coerce.date().optional(),
  })
});

const dogs = defineCollection({
  loader: file("src/data/dogs.json"),
  schema: z.object({
    id: z.string(),
    breed: z.string(),
    temperament: z.array(z.string()),
  }),
});

export const collections = { blog, dogs };
```

### Querying Collections

Import and use collection APIs:

```javascript
import { getCollection, getEntry } from 'astro:content';

// Get all entries from a collection
const allBlogPosts = await getCollection('blog');

// Get a single entry
const poodleData = await getEntry('dogs', 'poodle');
```

### Displaying Collection Data

```astro
---
import { getCollection } from 'astro:content';
const posts = await getCollection('blog');
---
<h1>My posts</h1>
<ul>
  {posts.map(post => (
    <li><a href={`/blog/${post.id}`}>{post.data.title}</a></li>
  ))}
</ul>
```

## Working with Images

Astro provides optimized image handling through the `Image` component:

### Rendering Images from Content Collections

```astro
---
import { Image } from "astro:assets";
import { getCollection } from "astro:content";
const allBlogPosts = await getCollection("blog");
---

{
	allBlogPosts.map((post) => (
		<div>
			<Image src={post.data.cover} alt={post.data.coverAlt} />
			<h2>
				<a href={"/blog/" + post.slug}>{post.data.title}</a>
			</h2>
		</div>
	))
}
```

## Key Features to Explore

1. **Project Structure** - Understanding Astro's file organization
2. **Content Collections** - Content management with frontmatter validation and type-safety
3. **View Transitions** - Seamless page transitions and animations
4. **Islands Architecture** - Fundamental approach to building performant web applications
5. **Component Support** - Use components from multiple frameworks in one project

## Why Choose Astro?

- **Performance-focused**: Zero JavaScript by default, ships only what you need
- **Developer-friendly**: Great DX with TypeScript support and modern tooling
- **Flexible**: Bring your own UI framework (or use none)
- **Content-first**: Optimized for blogs, documentation, marketing sites, and portfolios
- **Modern**: Built on Vite for fast development and optimized builds

## Content Layer API (v5.0)

The Content Layer API provides:
- Built-in content loaders for local collections
- Support for remote content via third-party loaders
- Ability to create custom loaders for any data source
- Performance and scalability improvements

---

*This documentation summary was generated using Context7 on 2026-01-12 and reflects the latest Astro 5 features and best practices.*
