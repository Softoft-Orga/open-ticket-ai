import fs from 'node:fs';
import path from 'node:path';
import yaml from 'js-yaml';
import type { Loader } from 'astro/loaders';

export function localeYamlLoader(options: {
  baseDir: string;
  fileName: string;
}): Loader {
  return {
    name: 'locale-yaml-loader',
    load: async ({ store, logger, parseData }) => {
      const { baseDir, fileName } = options;
      const locales = ['en', 'de'];

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
          
          await parseData({ id, data: entryData });
          store.set({ id, data: entryData });
        }
      }
    },
  };
}
