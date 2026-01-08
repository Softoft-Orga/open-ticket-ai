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
        app.component('ProductCards', defineAsyncComponent(() => import('../../src/components/vue/product/ProductCards.vue')))
        app.component('OTAIPredictionDemo', defineAsyncComponent(() => import('../../src/components/vue/predictionDemo/OTAIPredictionDemo.vue')))
        app.component('ServicePackages', defineAsyncComponent(() => import('../../src/components/vue/product/ServicePackages.vue')))
        app.component('SupportPlans', defineAsyncComponent(() => import('../../src/components/vue/product/SupportPlans.vue')))
        app.component('LatestNews', defineAsyncComponent(() => import('../../src/components/vue/news/LatestNews.vue')))
        app.component('AppTabs', defineAsyncComponent(() => import('../../src/components/vue/core/basic/Tabs.vue')))
        app.component('Table', defineAsyncComponent(() => import('../../src/components/vue/core/table/Table.vue')))
        app.component('Row', defineAsyncComponent(() => import('../../src/components/vue/core/table/Row.vue')))
        app.component('C', defineAsyncComponent(() => import('../../src/components/vue/core/table/C.vue')))
        app.component('FeatureGrid', defineAsyncComponent(() => import('../../src/components/vue/core/basic/FeatureGrid.vue')))
        app.component('Accordion', defineAsyncComponent(() => import('../../src/components/vue/core/accordion/Accordion.vue')))
        app.component('AccordionItem', defineAsyncComponent(() => import('../../src/components/vue/core/accordion/AccordionItem.vue')))
        app.component('LoadingComponent', defineAsyncComponent(() => import('../../src/components/vue/core/LoadingComponent.vue')))
        app.component('Link', defineAsyncComponent(() => import('../../src/components/vue/core/basic/Link.vue')))
        app.component('AIClassificationAnimation', defineAsyncComponent(() => import('../../src/components/vue/animation/AIClassificationAnimation.vue')))
        app.component('WaitlistSignupForm', defineAsyncComponent(() => import('../../src/components/vue/forms/WaitlistSignupForm.vue')))
        app.component('ContactForm', defineAsyncComponent(() => import('../../src/components/vue/forms/ContactForm.vue')))
        app.component('YoutubeVideo', defineAsyncComponent(() => import('../../src/components/vue/YoutubeVideo.vue')))
        app.component('ArchitectureOverview', defineAsyncComponent(() => import('../../src/components/vue/ArchitectureOverview.vue')))
        app.component('PipeSidecar', defineAsyncComponent(() => import('../../src/components/vue/pipe/PipeSidecar.vue')))
        app.component('ExamplesGallery', defineAsyncComponent(() => import('../../src/components/vue/configExamples/ExamplesGallery.vue')))
        app.component('ExamplePage', defineAsyncComponent(() => import('../../src/components/vue/configExamples/ExamplePage.vue')))
        app.component('InlineExample', defineAsyncComponent(() => import('../../src/components/vue/configExamples/InlineExample.vue')))
        app.component('PluginsMarketplace', defineAsyncComponent(() => import('../../src/components/vue/marketplace/PluginsMarketplace.vue')))
        app.component('MultiTagPredictionDemo', defineAsyncComponent(() => import('../../src/components/vue/multiTagDemo/MultiTagPredictionDemo.vue')))
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
