// .vitepress/navgen.ts
import fs from 'fs'
import path from 'path'

type LinkNode = { text: string; link: string }
type GroupNode<T = {}> = { text: string; items: TreeNode<T>[] } & T
type TreeNode<T = {}> = LinkNode | GroupNode<T>
type SidebarNode = TreeNode<{ collapsible?: boolean; collapsed?: boolean }>
type SidebarMap = Record<string, SidebarNode[]>
type DirectoryNode = { type: 'dir'; name: string; absolutePath: string; children: FileSystemNode[] }
type FileNode = { type: 'file'; name: string; absolutePath: string }
type FileSystemNode = DirectoryNode | FileNode

export type NavGeneratorOptions = {
    rootPath: string
    allowedExtensions?: string[]
    excludePatterns?: RegExp[]
    hideHiddenEntries?: boolean
    includeIndexAsFolderLink?: boolean
    includeEmptyDirectories?: boolean
    stripExtensionsInLinks?: boolean
    sidebarCollapsible?: boolean
    sidebarCollapsed?: boolean
    titleTransform?: (name: string) => string
    sortComparator?: (a: string, b: string) => number
}

const defaultTitleTransform = (name: string) =>
  name.replace(/\.[^.]+$/, '').replace(/[-_]/g, ' ').replace(/\b\w/g, c => c.toUpperCase())
export class NavGenerator {
    private rootPath: string
    private allowedExtensions: string[]
    private excludePatterns: RegExp[]
    private hideHiddenEntries: boolean
    private includeIndexAsFolderLink: boolean
    private includeEmptyDirectories: boolean
    private stripExtensionsInLinks: boolean
    private sidebarCollapsible: boolean
    private sidebarCollapsed: boolean
    private titleTransform: (name: string) => string
    private sortComparator: (a: string, b: string) => number

    constructor(options: NavGeneratorOptions) {
        this.rootPath = path.resolve(options.rootPath)
        this.allowedExtensions = options.allowedExtensions ?? ['.md']
        this.excludePatterns = options.excludePatterns ?? []
        this.hideHiddenEntries = options.hideHiddenEntries ?? true
        this.includeIndexAsFolderLink = options.includeIndexAsFolderLink ?? false
        this.includeEmptyDirectories = options.includeEmptyDirectories ?? false
        this.stripExtensionsInLinks = options.stripExtensionsInLinks ?? true
        this.sidebarCollapsible = options.sidebarCollapsible ?? true
        this.sidebarCollapsed = options.sidebarCollapsed ?? true
        this.titleTransform = options.titleTransform ?? defaultTitleTransform
        this.sortComparator = options.sortComparator ?? ((a, b) => a.localeCompare(b, undefined, {
            numeric: true,
            sensitivity: 'base'
        }))
    }

    generateNavbar(basePath: string): TreeNode[] {
        const baseDirPath = path.join(this.rootPath, basePath)
        const nodes = this.scanDirectory(baseDirPath)
        return this.toNavbar(nodes)
    }

    generateSidebar(basePath: string): SidebarMap {
        const baseDirPath = path.join(this.rootPath, basePath)
        const topLevel = this.scanDirectory(baseDirPath).filter(n => n.type === 'dir') as DirectoryNode[]
        const sidebar: SidebarMap = {}
        for (const section of topLevel) {
            const group = this.toSidebarGroup(section)
            if (group) sidebar[`/${basePath}/${section.name}/`] = [group]
        }
        return sidebar
    }

    private scanDirectory(directoryPath: string): FileSystemNode[] {
        const dirents = fs.readdirSync(directoryPath, {withFileTypes: true})
            .filter(d => this.shouldIncludeDirent(d))
            .sort((a, b) => this.sortComparator(a.name, b.name))

        const nodes: FileSystemNode[] = []
        for (const dirent of dirents) {
            const absolutePath = path.join(directoryPath, dirent.name)
            if (dirent.isDirectory()) {
                const children = this.scanDirectory(absolutePath)
                if (children.length > 0 || this.includeEmptyDirectories) {
                    nodes.push({type: 'dir', name: dirent.name, absolutePath, children})
                }
            } else {
                if (this.isIndexFile(dirent.name) && !this.includeIndexAsFolderLink) continue
                nodes.push({type: 'file', name: dirent.name, absolutePath})
            }
        }
        return nodes
    }

    private toNavbar(nodes: FileSystemNode[]): TreeNode[] {
        const nav: TreeNode[] = []
        for (const node of nodes) {
            if (node.type === 'dir') {
                const items = this.toNavbar(node.children)
                if (items.length > 0 || this.includeEmptyDirectories) {
                    nav.push({text: this.titleTransform(node.name), items})
                }
            } else {
                const link = this.linkFromAbsolutePath(node.absolutePath)
                nav.push({text: this.titleTransform(node.name), link})
            }
        }
        return nav
    }

    private toSidebarGroup(directoryNode: DirectoryNode): SidebarNode | null {
        const items: SidebarNode[] = []
        for (const child of directoryNode.children) {
            if (child.type === 'dir') {
                const group = this.toSidebarGroup(child)
                if (group) items.push(group)
            } else {
                items.push({text: this.titleTransform(child.name), link: this.linkFromAbsolutePath(child.absolutePath)})
            }
        }
        if (!items.length && !this.includeEmptyDirectories) return null
        return {
            text: this.titleTransform(directoryNode.name),
            items,
            collapsible: this.sidebarCollapsible,
            collapsed: this.sidebarCollapsed
        }
    }

    private shouldIncludeDirent(dirent: fs.Dirent): boolean {
        if (this.hideHiddenEntries && (dirent.name.startsWith('.') || dirent.name.startsWith('_'))) return false
        if (this.excludePatterns.some(rx => rx.test(dirent.name))) return false
        if (dirent.isDirectory()) return true
        return this.isAllowedFile(dirent.name)
    }

    private isAllowedFile(name: string): boolean {
        const ext = '.' + name.split('.').pop()?.toLowerCase()
        return this.allowedExtensions.map(e => e.toLowerCase()).includes(ext)
    }

    private isIndexFile(name: string): boolean {
        const lower = name.toLowerCase()
        return lower === 'index.md' || lower === 'readme.md'
    }

    private linkFromAbsolutePath(absolutePath: string): string {
        const rel = '/' + path.relative(this.rootPath, absolutePath).replace(/\\/g, '/')
        if (this.isIndexFile(path.basename(absolutePath))) {
            const dir = rel.replace(/\/[^/]+$/, '/')
            return dir
        }
        if (!this.stripExtensionsInLinks) return rel
        return rel.replace(/\.[^.]+$/, '')
    }
}
