import {defineAsyncComponent, h, watch} from 'vue'
import type {Theme} from 'vitepress'
import {useData} from 'vitepress'
import DefaultTheme from 'vitepress/theme'
import './styles/index.css'

import {createI18n, useI18n} from 'vue-i18n'
import enMessages from '../../docs_src/en/messages'
import Layout from './Layout.vue'

const i18n = createI18n({
    locale: 'en',
    fallbackLocale: 'en',
    messages: {en: enMessages}
})

export default {
    extends: DefaultTheme,
    Layout: () => h(Layout),
    enhanceApp({app}) {
        app.use(i18n)
        app.component('ProductCards', defineAsyncComponent(() => import('../components/product/ProductCards.vue')))
        app.component('OTAIPredictionDemo', defineAsyncComponent(() => import('../components/predictionDemo/OTAIPredictionDemo.vue')))
        app.component('ServicePackages', defineAsyncComponent(() => import('../components/product/ServicePackages.vue')))
        app.component('SupportPlans', defineAsyncComponent(() => import('../components/product/SupportPlans.vue')))
        app.component('LatestNews', defineAsyncComponent(() => import('../components/news/LatestNews.vue')))
        app.component('AppTabs', defineAsyncComponent(() => import('../components/core/basic/Tabs.vue')))
        app.component('Table', defineAsyncComponent(() => import('../components/core/table/Table.vue')))
        app.component('Row', defineAsyncComponent(() => import('../components/core/table/Row.vue')))
        app.component('C', defineAsyncComponent(() => import('../components/core/table/C.vue')))
        app.component('FeatureGrid', defineAsyncComponent(() => import('../components/core/basic/FeatureGrid.vue')))
        app.component('Accordion', defineAsyncComponent(() => import('../components/core/accordion/Accordion.vue')))
        app.component('AccordionItem', defineAsyncComponent(() => import('../components/core/accordion/AccordionItem.vue')))
        app.component('LoadingComponent', defineAsyncComponent(() => import('../components/core/LoadingComponent.vue')))
        app.component('Link', defineAsyncComponent(() => import('../components/core/basic/Link.vue')))
        app.component('AIClassificationAnimation', defineAsyncComponent(() => import('../components/animation/AIClassificationAnimation.vue')))
        app.component('WaitlistSignupForm', defineAsyncComponent(() => import('../components/forms/WaitlistSignupForm.vue')))
        app.component('ContactForm', defineAsyncComponent(() => import('../components/forms/ContactForm.vue')))
        app.component('YoutubeVideo', defineAsyncComponent(() => import('../components/YoutubeVideo.vue')))
        app.component('ArchitectureOverview', defineAsyncComponent(() => import('../components/ArchitectureOverview.vue')))
        app.component('PipeSidecar', defineAsyncComponent(() => import('../components/pipe/PipeSidecar.vue')))
        app.component('ExamplesGallery', defineAsyncComponent(() => import('../components/configExamples/ExamplesGallery.vue')))
        app.component('ExamplePage', defineAsyncComponent(() => import('../components/configExamples/ExamplePage.vue')))
        app.component('InlineExample', defineAsyncComponent(() => import('../components/configExamples/InlineExample.vue')))
        app.component('PluginsMarketplace', defineAsyncComponent(() => import('../components/marketplace/PluginsMarketplace.vue')))
        app.mixin({
            computed: {
                lang() {
                    return i18n.global.locale.value
                },
                $lang() {
                    return i18n.global.locale.value
                }
            }
        })
    },
    setup() {
        const {lang} = useData()
        const {locale} = useI18n()
        watch(lang, l => {
            locale.value = l
        }, {immediate: true})
    }
} satisfies Theme
