import json
from typing import Any


def prettify(obj: Any) -> str:
    return str(json.dumps(obj, indent=2, ensure_ascii=False, default=str))
