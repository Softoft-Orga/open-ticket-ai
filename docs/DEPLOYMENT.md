# Documentation Deployment Guide

This guide covers deploying the Open Ticket AI documentation to production.

## Deployment Platform

The documentation is deployed on **Netlify** at https://open-ticket-ai.com

## Automatic Deployment

### Continuous Deployment

Netlify is configured for automatic deployments:

- **Production**: Deploys from `main` branch
- **Preview**: Deploys from pull requests and other branches
- **Build Command**: `npm run docs:build`
- **Publish Directory**: `.vitepress/dist`

### Deployment Workflow

1. **Push Changes**: Commit and push to repository
2. **Netlify Build**: Automatically triggered by webhook
3. **Build Process**:
   - Checkout code
   - Install dependencies (`npm install`)
   - Run build (`npm run docs:build`)
   - Generate static files in `.vitepress/dist`
4. **Deploy**: Static files published to CDN
5. **Notification**: Build status notification (success/failure)

## Configuration

### Netlify Configuration

**File**: `netlify.toml` (repository root)

```toml
[build]
base = "docs/vitepress_docs"
command = "npm run docs:build"
publish = ".vitepress/dist"
functions = "netlify/functions"
```

### Build Settings

- **Base Directory**: `docs/vitepress_docs`
- **Build Command**: `npm run docs:build`
- **Publish Directory**: `.vitepress/dist` (relative to base)
- **Node Version**: Automatically detected from `.nvmrc` or uses default

### Environment Variables

No sensitive environment variables are required for building the documentation.

Public variables embedded in config:
- **GA Tracking ID**: G-FBWC3JDZJ4
- **GTM ID**: AW-474755810

## Manual Deployment

### Local Build

To test the production build locally:

```bash
cd docs/vitepress_docs

# Install dependencies
npm install

# Build for production
npm run docs:build

# Preview the build
npm run docs:preview
```

The preview will be available at `http://localhost:4173`

### Deploy to Netlify Manually

Using Netlify CLI:

```bash
# Install Netlify CLI
npm install -g netlify-cli

# Login to Netlify
netlify login

# Deploy to production
cd docs/vitepress_docs
npm run docs:build
netlify deploy --prod --dir=.vitepress/dist
```

## Domain Configuration

### Primary Domain

- **Domain**: https://open-ticket-ai.com
- **SSL**: Automatically managed by Netlify (Let's Encrypt)

### Redirects

**Old Domain Redirect** (configured in `netlify.toml`):
```toml
[[redirects]]
from = "https://ticket-classification.softoft.de/*"
to = "https://open-ticket-ai.com/:splat"
status = 301
force = true
```

### Language-Based Redirects

Automatic language detection redirects users to their preferred language:

```toml
# Redirect to German for German browsers
[[redirects]]
from = "/"
to = "/de"
status = 302
conditions = { Language = ["de"] }

# Redirect to English for English browsers
[[redirects]]
from = "/"
to = "/en"
status = 302
conditions = { Language = ["en"] }

# ... similar for es, fr
# Fallback to English for other languages
```

## Caching & Performance

### Asset Caching

Configured in `netlify.toml`:

```toml
# JavaScript files - long-term cache (immutable)
[[headers]]
for = "/assets/*.js"
[headers.values]
Cache-Control = "public, max-age=31536000, immutable"

# CSS files - long-term cache (immutable)
[[headers]]
for = "/assets/*.css"
[headers.values]
Cache-Control = "public, max-age=31536000, immutable"

# API reference - moderate cache
[[headers]]
for = "/api_reference.json"
[headers.values]
Cache-Control = "public, max-age=3600, immutable"
```

### Compression

VitePress build includes:
- **Brotli compression** for supported browsers
- **Gzip compression** as fallback

Configured in `.vitepress/config.mts`:
```typescript
vite: {
  plugins: [
    viteCompression({algorithm: 'brotliCompress'}),
    viteCompression({algorithm: 'gzip'})
  ]
}
```

## API Functions

Netlify Functions are used for dynamic API endpoints:

**Location**: `docs/vitepress_docs/netlify/functions/`

### Classification API

```toml
[[redirects]]
from = "/api/german_prediction/v1/classify"
to = "/.netlify/functions/classify"
status = 200
```

This allows the documentation site to provide an interactive API demo.

## Build Optimization

### Build Performance

VitePress build is optimized with:
- **Code splitting**: Separate chunks for each page
- **CSS code splitting**: Minimizes CSS payload per page
- **Tree shaking**: Removes unused code
- **Minification**: All assets minified for production

### Build Time

Typical build times:
- **Clean Build**: ~2-3 minutes
- **Incremental Build**: ~30-60 seconds
- **Cache-enabled Build**: ~20-30 seconds

### Build Cache

Netlify caches:
- `node_modules/` (dependencies)
- `.vitepress/cache/` (VitePress cache)

## Monitoring & Debugging

### Build Logs

Access build logs in Netlify dashboard:
1. Login to Netlify
2. Select the site
3. Go to "Deploys"
4. Click on a specific deploy to view logs

### Deploy Previews

Every pull request gets a unique deploy preview URL:
- **Format**: `deploy-preview-{PR-number}--open-ticket-ai.netlify.app`
- **Purpose**: Test changes before merging
- **Automatic Cleanup**: Previews cleaned up after PR merge/close

### Failed Builds

Common build failure causes:

1. **Dependency Issues**:
   - Missing dependencies in `package.json`
   - Incompatible package versions
   - Solution: Update `package.json` and test locally

2. **Broken Links**:
   - Dead links in documentation
   - Missing referenced files
   - Solution: Fix or remove broken links

3. **Syntax Errors**:
   - Invalid Markdown syntax
   - Invalid Vue component usage
   - Solution: Validate Markdown and Vue syntax

4. **Out of Memory**:
   - Large builds exceeding Netlify limits
   - Solution: Optimize images, reduce bundle size

## Analytics & Tracking

### Google Analytics

Configured for tracking site usage:
- **Property ID**: G-FBWC3JDZJ4
- **Implementation**: Google Tag Manager
- **Privacy**: Respects Do Not Track settings

### Metrics Tracked

- Page views
- User sessions
- Navigation patterns
- Search queries (if search is enabled)
- Exit pages

## SEO Configuration

### Sitemap

Automatically generated by VitePress:
```typescript
sitemap: {
  hostname: 'https://open-ticket-ai.com',
}
```

Sitemap available at: https://open-ticket-ai.com/sitemap.xml

### Meta Tags

Each page includes:
- Title tag (from frontmatter or auto-generated)
- Description meta tag
- Open Graph tags for social sharing
- Language tags for multi-lingual support

### robots.txt

Standard robots.txt allows all crawlers:
```
User-agent: *
Allow: /
Sitemap: https://open-ticket-ai.com/sitemap.xml
```

## Rollback Procedures

### Rollback to Previous Version

In Netlify dashboard:
1. Go to "Deploys"
2. Find the previous successful deploy
3. Click "Publish deploy"

### Emergency Rollback

Using Netlify CLI:
```bash
# List recent deploys
netlify deploy:list

# Rollback to specific deploy
netlify deploy:rollback <deploy-id>
```

## Troubleshooting

### Build Failures

**Symptom**: Build fails with "Command failed"
**Solution**:
1. Check build logs for specific error
2. Test build locally: `npm run docs:build`
3. Verify all dependencies are in `package.json`
4. Clear Netlify cache and retry

**Symptom**: Out of memory during build
**Solution**:
1. Optimize large images
2. Reduce bundle size
3. Contact Netlify support for memory increase

### Deployment Issues

**Symptom**: Site shows old content after deploy
**Solution**:
1. Clear browser cache
2. Purge Netlify CDN cache
3. Check if deploy actually succeeded

**Symptom**: 404 errors on pages
**Solution**:
1. Verify clean URLs are working
2. Check redirects in `netlify.toml`
3. Ensure all pages are in build output

### Performance Issues

**Symptom**: Slow page load times
**Solution**:
1. Check image sizes and optimize
2. Review bundle size in build output
3. Enable compression (should be automatic)
4. Use Lighthouse to identify bottlenecks

## Best Practices

1. **Test Locally**: Always build and preview locally before pushing
2. **Use Deploy Previews**: Review deploy preview URLs before merging PRs
3. **Monitor Build Times**: Watch for increasing build times indicating issues
4. **Keep Dependencies Updated**: Regularly update VitePress and plugins
5. **Optimize Assets**: Compress images, minimize large files
6. **Check Analytics**: Review analytics to identify popular content
7. **Document Changes**: Keep CHANGELOG.md updated for major changes

## Additional Resources

- **Netlify Documentation**: https://docs.netlify.com/
- **VitePress Deployment**: https://vitepress.dev/guide/deploy
- **Domain Management**: Netlify dashboard → Domain settings
- **Build Hooks**: Netlify dashboard → Build & deploy → Build hooks

## Support

For deployment issues:
1. Check Netlify status page: https://www.netlifystatus.com/
2. Review Netlify community forums
3. Contact Netlify support (if on paid plan)
4. Open GitHub issue for project-specific problems
