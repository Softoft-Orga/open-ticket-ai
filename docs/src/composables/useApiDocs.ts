import {reactive, readonly, toRefs} from 'vue';

// --- (All your interface definitions like ParameterData, ClassData, etc., remain here) ---
export interface ParameterData {
    name?: string | null;
    type?: string | null;
    default?: string | null;
    is_optional?: boolean | null;
    description?: string | null;
}

export interface ReturnsData {
    type?: string | null;
    description?: string | null;
    name?: string | null;
}

export interface DocstringData {
    short_description?: string | null;
    long_description?: string | null;
    params: ParameterData[];
    raises: ParameterData[];
    returns?: ReturnsData | null;
}

export interface FunctionData {
    name: string;
    signature: string;
    is_async: boolean;
    docstring: DocstringData;
}

export interface ClassData {
    name: string;
    docstring: DocstringData;
    methods: FunctionData[];
}

export interface ModuleEntry {
    module_path: string;
    module_docstring: DocstringData;
    classes: ClassData[];
    functions: FunctionData[];
}

export interface ClassDataWithContext extends ClassData {
    module_path: string;
}


// --- REACTIVE DATA STORE ---
// This state is defined once and shared across all components that use the composable.
const state = reactive({
    packages: new Map<string, ModuleEntry>(),
    classes: new Map<string, ClassDataWithContext>(),
    isLoading: false,
    error: null as Error | null,
});

// A flag to ensure the fetch operation only ever runs once.
let hasFetched = false;

/**
 * Fetches and processes the API data, populating the shared reactive state.
 */
async function fetchAndProcessApiData() {
    // This function will now only execute its logic one time.
    if (hasFetched) {
        return;
    }
    hasFetched = true; // Set flag immediately to prevent race conditions

    state.isLoading = true;
    try {
        const response = await fetch('/assets/api_reference.json');
        if (!response.ok) {
            throw new Error(`Failed to fetch API documentation: ${response.statusText}`);
        }
        const apiData: ModuleEntry[] = await response.json();

        // Build maps in temporary variables to avoid triggering reactivity on every item added.
        const tempPackages = new Map<string, ModuleEntry>();
        const tempClasses = new Map<string, ClassDataWithContext>();

        for (const module of apiData) {
            tempPackages.set(module.module_path, module);
            if (module.classes) {
                for (const cls of module.classes) {
                    const classId = `${module.module_path.replace(/\//g, '.')}.${cls.name}`;
                    tempClasses.set(classId, {...cls, module_path: module.module_path});
                }
            }
        }

        // Update the reactive state once with the final maps.
        state.packages = tempPackages;
        state.classes = tempClasses;

    } catch (e) {
        state.error = e as Error;
        console.error("Failed to load API docs:", e);
    } finally {
        state.isLoading = false;
    }
}

/**
 * A Vue composable that provides reactive, read-only access to the API documentation.
 * It triggers the data fetching process only once when it's first used.
 */
export function useApiDocs() {
    // Kick off the data fetching process if it hasn't started yet.
    fetchAndProcessApiData();

    // Return the reactive state properties as readonly refs.
    // This allows for easy destructuring in components while preventing modification.
    return {
        ...toRefs(readonly(state)),
    };
}
