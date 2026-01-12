import { defineMiddleware } from 'astro:middleware'
import { createLocalizedContent } from './utils/i18n'

export const onRequest = defineMiddleware(async (context, next) => {
  const locale = (context.currentLocale ?? context.preferredLocale ?? 'en').toLowerCase()
  context.locals.locale = locale
  context.locals.content = createLocalizedContent(locale, 'en')
  return next()
})
