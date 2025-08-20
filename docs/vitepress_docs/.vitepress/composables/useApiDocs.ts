import {readonly} from 'vue';
// Make sure the path to your JSON file is correct relative to the .vitepress directory


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

// CORRECTED: This is the structure of each element in the root JSON array
export interface ModuleEntry {
    module_path: string;
    module_docstring: DocstringData;
    classes: ClassData[];
    functions: FunctionData[];
}

// This will be the type stored in the Map, with module_path added for context
export interface ClassDataWithContext extends ClassData {
    module_path: string;
}

// --- DATA STORE ---

// Type the raw JSON data import


// This will hold our processed, easily searchable data with strong types
const processedData = {
  packages: new Map<string, ModuleEntry>(),
  classes: new Map<string, ClassDataWithContext>(),
};

/**
 * Processes the raw API data from JSON into structured Maps for efficient lookups.
 * This function runs only once.
 */
async function processApiData() {
  // Guard to prevent processing more than once
  if (processedData.packages.size > 0) return;
  const response = await fetch('/assets/api_reference.json'); // Adjust the path as needed
    if (!response.ok) {
        throw new Error(`Failed to fetch API documentation: ${response.statusText}`);
    }
  const apiData: ModuleEntry[] = await response.json();
  for (const module of apiData) {
    const modulePath = module.module_path;

    // 1. Store the entire module data by its path
    processedData.packages.set(modulePath, module);

    // 2. Store each class with a unique, searchable ID (e.g., 'path.to.file.ClassName')
    if (module.classes) {
      for (const cls of module.classes) {
        // Use dot notation for IDs to match the python package structure
        const classId = `${modulePath.replace(/\//g, '.')}.${cls.name}`;
        // Store class data along with its module path for context
        processedData.classes.set(classId, { ...cls, module_path: modulePath });
      }
    }
  }
}

// Run the processing logic as soon as this module is imported
processApiData();

/**
 * A Vue composable that provides reactive, read-only access to the processed API documentation.
 */
export function useApiDocs() {
  return {
    packages: readonly(processedData.packages),
    classes: readonly(processedData.classes),
  };
}
