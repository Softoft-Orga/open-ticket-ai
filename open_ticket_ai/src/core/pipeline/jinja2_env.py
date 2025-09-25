from typing import Any

from jinja2.sandbox import SandboxedEnvironment

from open_ticket_ai.src.core.pipeline.context import PipelineContext

_env = SandboxedEnvironment(autoescape=False, trim_blocks=True, lstrip_blocks=True)


def render_text(val, scope: dict):
    return _env.from_string(val).render(scope) if isinstance(val, str) else val

def render_any(obj: Any, scope: PipelineContext) -> Any:
    scope_dict = scope.model_dump()
    if isinstance(obj, str):
        return render_text(obj, scope_dict)
    if isinstance(obj, list):
        return [render_any(v, scope) for v in obj]
    if isinstance(obj, dict):
        return {k: render_any(v, scope) for k, v in obj.items()}
    return obj
