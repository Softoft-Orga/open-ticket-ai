import {NavGenerator, NavGeneratorOptions} from "./util/navgen.ts";
import viteCompression from 'vite-plugin-compression'
import {withMermaid} from "vitepress-plugin-mermaid";

const __VUE_PROD_DEVTOOLS__ = false;
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
export default withMermaid({

    title: 'Open Ticket AI',
    srcDir: './docs_src',
    appearance: 'force-dark',
    ignoreDeadLinks: true,
    mermaid: {
        startOnLoad: true,
        theme: 'base',
        themeVariables: {
            fontFamily:
                'Inter, ui-sans-serif, system-ui, Segoe UI, Roboto, Helvetica Neue, Arial',
            fontSize: '12px',

            textColor: '#e6e7ea',
            lineColor: '#94a3b8',

            primaryColor: '#7c4dff',
            primaryTextColor: '#e6e7ea',
            primaryBorderColor: '#a78bfa',

            secondaryColor: '#1f2937',
            tertiaryColor: '#0b1220',

            mainBkg: '#0b1220',
            nodeTextColor: '#e6e7ea',
            nodeBorder: '#475569',

            clusterBkg: '#111827',
            clusterBorder: '#374151',

            edgeLabelBackground: '#0b1220'
        }
    },
    head:
        [
            [
                'link',
                {
                    rel: 'icon',
                    href: 'https://softoft.sirv.com/Images/atc-logo-2024-blue.png?w=84&q=90&lightness=100&colorlevel.white=100'
                }
            ],
            ['script', {async: true, src: 'https://www.googletagmanager.com/gtag/js?id=AW-474755810'}],
            ['script', {}, `
            window.dataLayer = window.dataLayer || [];
            function gtag(){dataLayer.push(arguments);}
            gtag('js', new Date());
            gtag('config', 'AW-474755810');
        `],
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
    description:
        'Open Ticket AI is an open-source, on-premise solution that auto-classifies support tickets by queue and priority—integrates with OTOBO, Znuny, and OTRS.',
    lastUpdated:
        true,
    cleanUrls:
        true,
    sitemap:
        {
            hostname: 'https://open-ticket-ai.com',
        }
    ,
    locales: {
        root: {
            label: 'English',
            lang:
                'en',
            link:
                '/en/',
            themeConfig:
                {
                    nav: [
                        ...navGenerator.generateNavbar('en'),
                    ],
                    sidebar:
                        navGenerator.generateSidebar("en")
                }
        }

    }
    ,
    themeConfig: {
        footer: {
            message: '<strong>OTAI</strong> - Open Ticket AI',
            copyright:
                "by <a href='https://www.softoft.de' target='_blank'>Softoft, Tobias Bück Einzelunternehmen</a>"
        }
    }
    ,
    vite: {
        build: {
            cssCodeSplit: true,
        }
        ,
        plugins: [
            viteCompression({algorithm: 'brotliCompress'}),
            viteCompression({algorithm: 'gzip'})
        ],
        define:
            {
                __VUE_PROD_DEVTOOLS__: 'false',
            }
        ,
        ssr: {
            noExternal: [
                'vue-i18n',
                '@intlify/message-compiler',
                '@intlify/shared'
            ]
        }
        ,
    }
    ,
})
