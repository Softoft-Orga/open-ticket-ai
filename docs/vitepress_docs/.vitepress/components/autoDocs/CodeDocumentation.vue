<template>
    <div class="flex items-center min-h-64 w-full">
        <LoadingComponent v-if="isLoading" class="w-full h-64"/>
        <div v-else>
            <Suspense>
                <template #default>
                    <div>
                        <div v-if="subPackagesToDisplay.length" class="space-y-4">
                            <div class="flex items-center space-x-2">
                                <Badge class="text-3xl" type="success">package</Badge>
                                <h1 class="text-3xl mb-2">{{ parentPackageId }}</h1>
                            </div>
                            <div class="space-y-4">
                                <Card v-for="subPkg in subPackagesToDisplay" :key="subPkg.module_path" class="p-2">
                                    <CodeDocumentation :package-id="subPkg.module_path" show-all-classes
                                                       show-all-functions/>
                                </Card>
                            </div>
                        </div>

                        <Card v-else-if="classData || packageData" class="mb-4 p-1 border-none">
                            <div v-if="classData">
                                <div class="flex items-center space-x-2 mb-2">
                                    <Badge type="warning">class</Badge>
                                    <h3 class="font-mono text-xl">{{ classData.name }}</h3>
                                </div>
                                <p class="text-sm text-vp-text-2 mb-4">From: <code>{{ classData.module_path }}</code>
                                </p>
                                <Docstring :doc="classData.docstring" class="py-3"/>
                                <Accordion v-if="methodsToDisplay.length" :items="methodItems">
                                    <template v-for="(method, i) in methodsToDisplay" :key="i" v-slot:[`item-${i}`]>
                                        <FunctionDoc :func="method" :parent-id="classId"/>
                                    </template>
                                </Accordion>
                            </div>

                            <div v-else>
                                <div class="flex items-center space-x-2 mb-1">
                                    <Badge type="primary">module</Badge>
                                    <h2 class="font-mono text-xl">{{ packageId }}</h2>
                                </div>
                                <Docstring :doc="packageData.module_docstring" class="py-3"/>
                                <div v-if="showAllClasses && packageData.classes.length" class="mt-4 space-y-3">
                                    <h2 class="text-xl font-semibold mb-4">Classes</h2>
                                    <div v-for="cls in packageData.classes" :key="cls.name">
                                        <CodeDocumentation :class-id="`${packageId.replace(/\//g, '.')}.${cls.name}`"
                                                           show-public-methods/>
                                    </div>
                                </div>
                                <div v-if="showAllFunctions && packageData.functions.length" class="mt-4">
                                    <h2 class="text-xl font-semibold mb-4">Functions</h2>
                                    <Accordion :items="functionItems">
                                        <template v-for="(func, i) in packageData.functions" :key="i"
                                                  v-slot:[`item-${i}`]>
                                            <FunctionDoc :func="func" :parent-id="packageId"/>
                                        </template>
                                    </Accordion>
                                </div>
                            </div>
                        </Card>
                    </div>
                </template>

                <template #fallback>
                    <LoadingComponent class="w-full h-64"/>
                </template>
            </Suspense>
        </div>
    </div>
</template>

<script lang="ts" setup>
import {computed, defineAsyncComponent} from 'vue' // Import defineAsyncComponent
import {useApiDocs} from '../../composables/useApiDocs'
import LoadingComponent from "../core/LoadingComponent.vue"; // Keep this one static

// --- Define Components Asynchronously ---
const FunctionDoc = defineAsyncComponent(() => import('./FunctionDoc.vue'));
const Docstring = defineAsyncComponent(() => import('./Docstring.vue'));
const Badge = defineAsyncComponent(() => import('../core/basic/Badge.vue'));
const Card = defineAsyncComponent(() => import('../core/basic/Card.vue'));
const Accordion = defineAsyncComponent(() => import('../core/accordion/Accordion.vue'));
const CodeDocumentation = defineAsyncComponent(() => import('./CodeDocumentation.vue'));

// --- THE REST OF THE SCRIPT IS UNCHANGED ---
interface Props {
    classId?: string
    packageId?: string
    parentPackageId?: string
    showAllMethods?: boolean
    showPublicMethods?: boolean
    showAllClasses?: boolean
    showAllFunctions?: boolean
}

const props = withDefaults(defineProps<Props>(), {
    classId: '',
    packageId: '',
    parentPackageId: '',
    showAllMethods: false,
    showPublicMethods: false,
    showAllClasses: false,
    showAllFunctions: false,
})

const {packages, classes, isLoading} = useApiDocs()

const classData = computed(() =>
    props.classId ? classes.value.get(props.classId) ?? null : null
)
const packageData = computed(() =>
    props.packageId ? packages.value.get(props.packageId) ?? null : null
)

const methodsToDisplay = computed(() => {
    if (!classData.value?.methods) return []
    if (props.showAllMethods) return classData.value.methods
    if (props.showPublicMethods) {
        return classData.value.methods.filter(m => !m.name.startsWith('_'))
    }
    return []
})

const methodItems = computed(() =>
    methodsToDisplay.value.map(m => ({title: m.name}))
)

const functionItems = computed(() =>
    packageData.value?.functions.map(f => ({title: f.name})) || []
)

const subPackagesToDisplay = computed(() => {
    if (!props.parentPackageId) return []
    const parentPath = props.parentPackageId.replace(/\//g, '.')
    return Array.from(packages.value.values()).filter(pkg =>
        pkg.module_path.replace(/\//g, '.').startsWith(parentPath + '.')
    )
})
</script>
