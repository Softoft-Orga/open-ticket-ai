#!/usr/bin/env python3
"""Auto-translate Astro docs tree using OpenAI Chat Completions API."""

import asyncio
import os
from pathlib import Path
from typing import Any, Self

import yaml
from jinja2 import Environment, FileSystemLoader
from openai import AsyncOpenAI
from openai.types.chat import ChatCompletionMessageParam
from pydantic import BaseModel, Field
from tenacity import retry, stop_after_attempt, wait_exponential


class Config(BaseModel):
    """Configuration for tree translation."""

    mappings: list[dict[str, str]]
    include_ext: set[str] = Field(
        default_factory=lambda: {".astro", ".yml", ".yaml", ".md", ".mdx"},
    )
    exclude_dir_names: set[str] = Field(
        default_factory=lambda: {"node_modules", ".git", "dist"},
    )
    prompt_template_path: Path = Path("prompt.j2")
    base_language: str = "English"
    target_language: str = "German"
    model: str = "gpt-4"
    temperature: float = 0.3
    max_concurrency: int = 5
    force: bool = False

    @classmethod
    def from_yaml(cls, path: Path, **kwargs: Any) -> Self:
        """Load configuration from YAML file."""
        with path.open() as f:
            data = yaml.safe_load(f) or {}

        data.update(kwargs)

        if "prompt_template_path" in data:
            p = Path(data["prompt_template_path"])
            if not p.is_absolute():
                data["prompt_template_path"] = path.parent / p

        return cls.model_validate(data)


class TreeTranslator:

    def __init__(self, config: Config, client: AsyncOpenAI | None = None) -> None:
        self.config = config
        self.client = client
        self.semaphore = asyncio.Semaphore(config.max_concurrency)

        template_dir = config.prompt_template_path.parent
        template_name = config.prompt_template_path.name
        self.jinja_env = Environment(loader=FileSystemLoader(template_dir))
        self.prompt_template = self.jinja_env.get_template(template_name)

    def _render_system_prompt(self, file_ext: str) -> str:
        return self.prompt_template.render(
            file_ext=file_ext,
            base_language=self.config.base_language,
            target_language=self.config.target_language,
        )

    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=2, max=10),
    )
    async def _translate_content(self, content: str, file_ext: str) -> str:
        """Translate file content using OpenAI API with retry logic."""
        if self.client is None:
            raise RuntimeError("AsyncOpenAI client not initialized")

        system_prompt = self._render_system_prompt(file_ext)

        messages: list[ChatCompletionMessageParam] = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": content},
        ]

        response = await self.client.chat.completions.create(
            model=self.config.model,
            temperature=self.config.temperature,
            messages=messages,
        )

        return response.choices[0].message.content or ""

    async def _translate_file(self, source: Path, target: Path) -> None:
        """Translate a single file."""
        async with self.semaphore:
            if target.exists() and not self.config.force:
                return

            file_ext = source.suffix.lower()
            content = source.read_text(encoding="utf-8")

            translated = await self._translate_content(content, file_ext)

            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_text(translated, encoding="utf-8")
            print(target)

    def _should_process(self, path: Path) -> bool:
        return path.suffix.lower() in self.config.include_ext

    def _should_skip_dir(self, dir_name: str) -> bool:
        return dir_name in self.config.exclude_dir_names

    def _collect_files(self, from_dir: Path, to_dir: Path) -> list[tuple[Path, Path]]:
        files_to_translate = []

        for item in from_dir.rglob("*"):
            if item.is_file():
                parts = item.relative_to(from_dir).parts
                if (any(self._should_skip_dir(part) for part in parts) or
                    not self._should_process(item)):
                    continue

                relative_path = item.relative_to(from_dir)
                target_path = to_dir / relative_path
                files_to_translate.append((item, target_path))

        return files_to_translate

    async def translate_all(self) -> None:
        """Translate all files according to configuration mappings."""
        all_tasks = []

        for mapping in self.config.mappings:
            from_dir = Path(mapping["from_dir"])
            to_dir = Path(mapping["to_dir"])

            if not from_dir.exists():
                print(f"Warning: Source directory does not exist: {from_dir}")
                continue

            files_to_translate = self._collect_files(from_dir, to_dir)

            for source, target in files_to_translate:
                task = self._translate_file(source, target)
                all_tasks.append(task)

        if all_tasks:
            await asyncio.gather(*all_tasks)


if __name__ == "__main__":
    config_path = Path("./translate.config.yml")
    config = Config.from_yaml(config_path)

    api_key = os.getenv("OPEN_ROUTER_API_KEY")
    base_url = "https://openrouter.ai/api/v1"

    client_kwargs: dict[str, Any] = {
        "api_key": api_key,
        "base_url": base_url,
    }

    client = AsyncOpenAI(**client_kwargs)

    translator = TreeTranslator(config, client=client)
    asyncio.run(translator.translate_all())
