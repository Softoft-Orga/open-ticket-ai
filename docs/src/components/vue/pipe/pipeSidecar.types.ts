export interface PipeSidecarInput {
    placement: string
    alongside?: string[]
    params?: Record<string, string>
}

export interface PipeSidecarOutputExample {
    state: string
    payload?: any
    error?: string
}

export interface PipeSidecarOutput {
    state_enum: string[]
    description: string
    payload_schema_ref?: string
    examples?: Record<string, PipeSidecarOutputExample>
}

export interface PipeSidecarError {
    code: string
    when: string
}

export interface PipeSidecarErrors {
    fail?: PipeSidecarError[]
    break?: PipeSidecarError[]
    continue?: PipeSidecarError[]
}

export interface PipeSidecarEngineSupport {
    on_failure: boolean
    on_success: boolean
}

export interface PipeSidecar {
    _version: string
    _class: string
    _extends: string
    _title: string
    _summary: string
    _category: string
    _inputs: PipeSidecarInput
    _defaults?: Record<string, any>
    _output: PipeSidecarOutput
    _errors: PipeSidecarErrors
    _engine_support: PipeSidecarEngineSupport
    _examples: Record<string, string>
}
