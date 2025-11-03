import json
import re
from pathlib import Path
from typing import Literal

import yaml
from pydantic import BaseModel, Field, model_validator


# IDEA: Also report the version the config was tested with

DOCS_DIR = "docs/docs_src/public/configExamples"
SRC_TEMPLATES = "src/data/configExamples"

def _slugify(s: str) -> str:
    s = s.strip().lower()
    s = re.sub(r"[^a-z0-9]+", "-", s)
    s = re.sub(r"-{2,}", "-", s)
    return s.strip("-")


type Tag = Literal["basic", "simple-ticket-system", "simple-ai", "complex-workflow"]


class OTAIConfigExampleMetaInfo(BaseModel):
    name: str = Field(min_length=5, max_length=40, pattern=r'^(\w+\s\w+)*\s?$')
    md_description: str = Field(min_length=20, max_length=200)
    md_details: str | None = Field(None, min_length=20, max_length=5000)
    tags: list[Tag]

    @model_validator(mode='after')
    def set_md_details_default(self):
        if self.md_details is None:
            self.md_details = self.md_description
        return self


def save_example(config: BaseModel, meta: OTAIConfigExampleMetaInfo,
    out_dir: str = "docs/docs_src/public/configExamples") -> Path:
    slug = _slugify(meta.name)
    base = Path(out_dir) / slug
    base.mkdir(parents=True, exist_ok=True)
    (base / "config.yml").write_text(
        yaml.safe_dump(config.model_dump(mode="json", exclude_none=True), sort_keys=False, allow_unicode=True),
    )
    meta_dict = meta.model_dump()
    meta_dict["slug"] = slug
    meta_dict["path"] = f"/configExamples/{slug}/config.yml"
    (base / "meta.json").write_text(json.dumps(meta_dict, ensure_ascii=False, indent=2))
    _update_registry(Path(out_dir), meta_dict)
    return base / "config.yml"


def _update_registry(out_dir: Path, entry: dict):
    reg_json = out_dir / "registry.json"
    reg = []
    if reg_json.exists():
        reg = json.loads(reg_json.read_text())
    by_slug = {e["slug"]: e for e in reg}
    by_slug[entry["slug"]] = entry
    reg = list(by_slug.values())
    reg_json.write_text(json.dumps(reg, ensure_ascii=False, indent=2))
    (out_dir / "registry.yml").write_text(yaml.safe_dump(reg, sort_keys=False, allow_unicode=True))
