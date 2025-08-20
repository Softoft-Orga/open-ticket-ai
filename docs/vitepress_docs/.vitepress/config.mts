import {defineConfig} from "vitepress";
import {NavGenerator, NavGeneratorOptions} from "./util/navgen.ts";
import viteCompression from 'vite-plugin-compression'

var __VUE_PROD_DEVTOOLS__ = false
console.log(__VUE_PROD_DEVTOOLS__)
const navGeneratorOptions: NavGeneratorOptions = {
    rootPath: './docs_src',
    allowedExtensions: ['.md'],
    excludePatterns: [/^_/, /\/_/, /\/\./],
    hideHiddenEntries: true,
    includeIndexAsFolderLink: false,
    includeEmptyDirectories: false,
    stripExtensionsInLinks: true,
    sidebarCollapsible: true,
    sidebarCollapsed: true,
    sortComparator: (a: string, b: string) => a.localeCompare(b, undefined, {numeric: true, sensitivity: 'base'})
}
const navGenerator = new NavGenerator(navGeneratorOptions);
const gaId = 'G-FBWC3JDZJ4'
export default defineConfig({

    title: 'Open Ticket AI',
    srcDir: './docs_src',
    appearance: 'force-dark',
    head: [
        [
            'link',
            {
                rel: 'icon',
                href: 'https://softoft.sirv.com/Images/atc-logo-2024-blue.png?w=84&q=90&lightness=100&colorlevel.white=100'
            }
        ],
        ['script', {}, `
            (() => {
              let id='${gaId}'
              let loaded=false
              function load(){
                if(loaded) return; loaded=true
                let s=document.createElement('script'); s.src='https://www.googletagmanager.com/gtag/js?id='+id; s.async=true; document.head.appendChild(s)
                window.dataLayer=window.dataLayer||[]
                function gtag(){dataLayer.push(arguments)}
                gtag('js', new Date())
                gtag('config', id, {send_page_view:false})
              }
              if('requestIdleCallback' in window) requestIdleCallback(load,{timeout:4000}); else setTimeout(load,2000)
              let fired=false;
              ['scroll','pointerdown','keydown','touchstart'].forEach((ev) =>{
                addEventListener(ev,function(){ if(fired) return; fired=true; load() },{passive:true, once:true})
              })
            })();
    `]
    ],
    description: 'Open Ticket AI is an open-source, on-premise solution that auto-classifies support tickets by queue and priority—integrates with OTOBO, Znuny, and OTRS.',
    lastUpdated: true,
    cleanUrls: true,
    sitemap: {
        hostname: 'https://open-ticket-ai.com',
    },
    locales: {
        root: {
            label: 'English',
            lang: 'en',
            link: '/en/',
            themeConfig: {
                nav: [
                    ...navGenerator.generateNavbar('en'),
                ],
                sidebar: navGenerator.generateSidebar("en")
            }
        },
        de: {
            label: 'Deutsch',
            lang: 'de',
            link: '/de/',
            themeConfig: {
                nav: [
                    ...navGenerator.generateNavbar('de'),
                ],
                sidebar: navGenerator.generateSidebar("de")
            }
        },
        fr: {
            label: 'French',
            lang: 'fr',
            link: '/fr/',
            themeConfig: {
                nav: [
                    ...navGenerator.generateNavbar('fr'),
                ],
                sidebar: navGenerator.generateSidebar("fr")
            }
        },
        es: {
            label: 'Spanish',
            lang: 'es',
            link: '/es/',
            themeConfig: {
                nav: [
                    ...navGenerator.generateNavbar('es'),
                ],
                sidebar: navGenerator.generateSidebar("es")
            }
        }

    },
    themeConfig: {
        footer: {
            message: '<b>OTAI</b> - Open Ticket AI',
            copyright: "by <a href='https://www.softoft.de' target='_blank'>Softoft, Tobias Bück Einzelunternehmen</a>"
        }
    },
    vite: {
        build: {
            cssCodeSplit: true,
        },
        plugins: [
            viteCompression({algorithm: 'brotliCompress'}),
            viteCompression({algorithm: 'gzip'})
        ],
        define: {
            __VUE_PROD_DEVTOOLS__: 'false',
        },
        ssr: {
            noExternal: [
                'vue-i18n',
                '@intlify/message-compiler',
                '@intlify/shared'
            ]
        },
    },
})
