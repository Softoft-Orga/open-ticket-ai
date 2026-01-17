try {
  const path = import.meta.resolve('astro-seo-schema');
  console.log('Resolved to:', path);
} catch (e) {
  console.error('Failed to resolve:', e.message);
}

