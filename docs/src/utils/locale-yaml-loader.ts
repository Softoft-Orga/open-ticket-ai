import fs from 'node:fs';
import path from 'node:path';
import yaml from 'js-yaml';
import type { Loader } from 'astro/loaders';
import { i18n } from 'astro:config/server';
import { toCodes } from 'astro:i18n';

export function localeYamlLoader(options: {
  baseDir: string;
  fileName: string;
}): Loader {
  return {
    name: 'locale-yaml-loader',
    load: async ({ store, logger, parseData }) => {
      const { baseDir, fileName } = options;
      
      // Dynamically get locales from Astro i18n config
      if (!i18n) {
        logger.error('i18n is not configured in astro.config.mjs');
        return;
      }
      
      const locales = toCodes(i18n.locales);

      for (const locale of locales) {
        const filePath = path.join(baseDir, locale, fileName);

        if (!fs.existsSync(filePath)) {
          logger.warn(`File not found: ${filePath}`);
          continue;
        }

        const fileContent = fs.readFileSync(filePath, 'utf-8');
        const data = yaml.load(fileContent);

        if (!Array.isArray(data)) {
          logger.error(`${filePath} must contain an array of items`);
          continue;
        }

        for (const item of data) {
          const id = `${locale}/${item.slug || item.id}`;
          const entryData = { ...item, lang: locale };
          
          // parseData internally calls store.set after validation
          await parseData({ id, data: entryData });
        }
      }
    },
  };
}
