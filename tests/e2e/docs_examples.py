from pathlib import Path
import json

from pydantic import BaseModel
import yaml


def save_example(config: BaseModel, slug: str, name: str, tags: list[str], description: str,
    out_dir: str = "docs/examples") -> Path:
    base = Path(out_dir) / slug
    base.mkdir(parents=True, exist_ok=True)
    (base / "config.yml").write_text(
        yaml.safe_dump(config.model_dump(mode="json", exclude_none=True), sort_keys=False, allow_unicode=True))
    meta = {"slug": slug, "name": name, "tags": tags, "description": description,
        "path": f"/examples/{slug}/config.yml"}
    (base / "meta.json").write_text(json.dumps(meta, ensure_ascii=False, indent=2))
    _update_registry(Path(out_dir), meta)
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
