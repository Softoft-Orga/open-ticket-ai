import { describe, expect, it } from 'vitest';
import { getCollection, getEntry } from 'astro:content';

describe('Content Collections', () => {
  describe('docs collection', () => {
    it('should load docs entries', async () => {
      const docs = await getCollection('docs');
      expect(docs).toBeDefined();
      expect(Array.isArray(docs)).toBe(true);
    });

    it('should validate docs schema', async () => {
      const entry = await getEntry('docs', 'getting-started');
      expect(entry).toBeDefined();
      expect(entry?.data.title).toBe('Getting Started');
      expect(entry?.data.lang).toBe('en');
    });

    it('should have navigation metadata', async () => {
      const entry = await getEntry('docs', 'getting-started');
      expect(entry?.data.nav).toBeDefined();
      expect(entry?.data.nav?.group).toBe('Introduction');
      expect(entry?.data.nav?.order).toBe(1);
    });
  });

  describe('blog collection', () => {
    it('should load blog entries', async () => {
      const blog = await getCollection('blog');
      expect(blog).toBeDefined();
      expect(Array.isArray(blog)).toBe(true);
    });

    it('should validate blog schema with date', async () => {
      const entry = await getEntry('blog', 'introducing-open-ticket-ai');
      expect(entry).toBeDefined();
      expect(entry?.data.title).toBe('Introducing Open Ticket AI');
      expect(entry?.data.date).toBeInstanceOf(Date);
      expect(entry?.data.tags).toContain('announcement');
    });

    it('should have category field', async () => {
      const entry = await getEntry('blog', 'introducing-open-ticket-ai');
      expect(entry?.data.category).toBe('News');
    });
  });

  describe('products collection', () => {
    it('should load products entries', async () => {
      const products = await getCollection('products');
      expect(products).toBeDefined();
      expect(Array.isArray(products)).toBe(true);
    });

    it('should validate products schema', async () => {
      const entry = await getEntry('products', 'open-ticket-ai-lite');
      expect(entry).toBeDefined();
      expect(entry?.data.slug).toBe('open-ticket-ai-lite');
      expect(entry?.data.title).toBe('Open Ticket AI Lite');
      expect(entry?.data.tier).toBe('lite');
    });

    it('should have features array', async () => {
      const entry = await getEntry('products', 'open-ticket-ai-lite');
      expect(Array.isArray(entry?.data.features)).toBe(true);
      expect(entry?.data.features?.length).toBeGreaterThan(0);
    });

    it('should validate tier enum', async () => {
      const entry = await getEntry('products', 'open-ticket-ai-pro');
      expect(['lite', 'pro', 'enterprise']).toContain(entry?.data.tier);
    });
  });

  describe('services collection', () => {
    it('should load services entries', async () => {
      const services = await getCollection('services');
      expect(services).toBeDefined();
      expect(Array.isArray(services)).toBe(true);
    });

    it('should validate services schema', async () => {
      const entry = await getEntry('services', 'implementation-support');
      expect(entry).toBeDefined();
      expect(entry?.data.slug).toBe('implementation-support');
      expect(entry?.data.title).toBe('Implementation Support');
    });

    it('should have outcomes and pricing', async () => {
      const entry = await getEntry('services', 'implementation-support');
      expect(Array.isArray(entry?.data.outcomes)).toBe(true);
      expect(typeof entry?.data.startingPrice).toBe('number');
      expect(entry?.data.startingPrice).toBe(5000);
    });

    it('should have oneLiner field', async () => {
      const entry = await getEntry('services', 'consulting');
      expect(entry?.data.oneLiner).toBeDefined();
      expect(typeof entry?.data.oneLiner).toBe('string');
    });
  });

  describe('navigation metadata', () => {
    it('should support navigation ordering across collections', async () => {
      const docs = await getCollection('docs');
      const withNav = docs.filter((doc) => doc.data.nav?.order !== undefined);
      expect(withNav.length).toBeGreaterThan(0);
    });

    it('should support hidden navigation items', async () => {
      const products = await getCollection('products');
      const visibleProducts = products.filter((p) => !p.data.nav?.hidden);
      expect(visibleProducts.length).toBeGreaterThan(0);
    });
  });

  describe('language support', () => {
    it('should default to English', async () => {
      const entry = await getEntry('docs', 'getting-started');
      expect(entry?.data.lang).toBe('en');
    });
  });

  describe('draft support', () => {
    it('should support draft field in docs', async () => {
      const entry = await getEntry('docs', 'getting-started');
      expect(typeof entry?.data.draft).toBe('boolean');
      expect(entry?.data.draft).toBe(false);
    });

    it('should support draft field in blog', async () => {
      const entry = await getEntry('blog', 'introducing-open-ticket-ai');
      expect(typeof entry?.data.draft).toBe('boolean');
    });
  });
});
