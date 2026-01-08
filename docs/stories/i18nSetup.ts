import {createI18n} from 'vue-i18n'
import en from '../src/i18n/en/messages'

export const i18n = createI18n({
    legacy: false,
    locale: 'en',
    fallbackLocale: 'en',
    messages: {
        en,
    },
})
