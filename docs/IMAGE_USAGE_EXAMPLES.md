# Astro Image Component Usage Examples

This document provides examples of how to use the Astro `<Image>` component in this project.

## Configuration

Image optimization is configured in `docs/astro.config.mjs`:
- **Image Service**: Sharp (configured to allow processing of large images)
- **Authorized Domains**: `astro.build`, `doc.otobo.org`, `softoft.sirv.com`
- **Remote Patterns**: `**.githubusercontent.com`, `**.sirv.com`

## Storage Locations

### Local Assets (Optimized)
Store in `docs/src/assets/` for images that need optimization:
```
docs/src/assets/
  ├── logos/
  ├── screenshots/
  └── diagrams/
```

### Public Static Files
Store in `docs/public/` for static images served as-is:
```
docs/public/
  ├── assets/
  ├── images/
  └── icons/
```

## Usage Examples

### 1. Local Image from `src/assets/`

Images imported from `src/assets/` are automatically optimized and dimensions are inferred:

```astro
---
import { Image } from 'astro:assets';
import logo from '../assets/logos/company-logo.png';
---

<Image src={logo} alt="Company Logo" />
```

**Benefits:**
- Automatic format optimization (WebP, AVIF)
- Automatic width/height inference
- Build-time image processing

### 2. Public Folder Image

Images from the `public/` folder require explicit dimensions:

```astro
---
import { Image } from 'astro:assets';
---

<Image 
  src="/assets/feature-screenshot.png" 
  alt="Product feature screenshot" 
  width="800" 
  height="600" 
/>
```

**When to use:**
- Images that shouldn't be processed
- SVG files that don't need optimization
- Very small images

### 3. Remote Image from Authorized Domain

Remote images from authorized domains can be optimized:

```astro
---
import { Image } from 'astro:assets';
---

<Image 
  src="https://doc.otobo.org/manual/admin/10.0/en/_images/agent-add.png" 
  alt="OTOBO admin panel" 
  width="1200" 
  height="800" 
/>
```

**Authorized domains:**
- `astro.build`
- `doc.otobo.org`
- `softoft.sirv.com`
- `**.githubusercontent.com`
- `**.sirv.com`

### 4. Markdown/MDX Content

In Markdown or MDX files, use standard markdown syntax. Astro will automatically optimize these:

```markdown
![Alt text](/images/diagram.png)

![Remote image](https://softoft.sirv.com/open-ticket-ai/banner.png)
```

### 5. Responsive Images with Picture Component

For art direction or different images at different breakpoints:

```astro
---
import { Picture } from 'astro:assets';
import mobileImage from '../assets/mobile-hero.jpg';
import desktopImage from '../assets/desktop-hero.jpg';
---

<Picture 
  src={desktopImage} 
  formats={['avif', 'webp']}
  alt="Hero banner"
  widths={[400, 800, 1200]}
/>
```

## Best Practices

1. **Always include `alt` attributes** for accessibility
2. **Use local imports for project images** to get automatic optimization
3. **Provide explicit dimensions for public/remote images** to prevent layout shift
4. **Use WebP/AVIF formats** for better compression (automatic with `<Image>`)
5. **Organize images logically** in subdirectories (logos/, screenshots/, etc.)

## Common Patterns

### Card with Image
```astro
---
import { Image } from 'astro:assets';
import cardImage from '../assets/products/product-1.jpg';
---

<div class="card">
  <Image src={cardImage} alt="Product 1" />
  <h3>Product Name</h3>
  <p>Description...</p>
</div>
```

### Blog Post Header
```astro
---
import { Image } from 'astro:assets';
const { frontmatter } = Astro.props;
---

<article>
  <Image 
    src={frontmatter.coverImage} 
    alt={frontmatter.coverImageAlt} 
  />
  <h1>{frontmatter.title}</h1>
</article>
```

### Gallery with Multiple Images
```astro
---
import { Image } from 'astro:assets';
const images = await Astro.glob('../assets/gallery/*.{png,jpg}');
---

<div class="gallery">
  {images.map((image) => (
    <Image 
      src={image.default} 
      alt="Gallery image" 
      width="400" 
      height="300" 
    />
  ))}
</div>
```

## Troubleshooting

### Image not found
- Check the path is correct relative to the current file
- Ensure the image exists in the expected location

### Remote image not optimizing
- Verify the domain is listed in `astro.config.mjs` under `image.domains` or `image.remotePatterns`
- Check that width and height are provided

### Build errors
- Run `npm run docs:check` to validate the Astro configuration
- Check console for specific error messages about missing images
