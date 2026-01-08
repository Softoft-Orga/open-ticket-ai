// Define global constants for vue-i18n during SSR
if (typeof window === 'undefined') {
    global.__VUE_PROD_DEVTOOLS__ = false;
}

import { createI18n } from 'vue-i18n';
import en from './i18n/en/messages';

const i18n = createI18n({
    legacy: false,
    locale: 'en',
    fallbackLocale: 'en',
    messages: {
        en,
    },
});

export default (app) => {
    app.use(i18n);
};
