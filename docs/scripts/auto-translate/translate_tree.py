#!/usr/bin/env python3
"""Auto-translate Astro docs tree using OpenAI Chat Completions API."""

import argparse
import asyncio
import os
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

import yaml
from jinja2 import Environment, FileSystemLoader
from openai import AsyncOpenAI
from tenacity import retry, stop_after_attempt, wait_exponential


@dataclass
class Config:
    """Configuration for tree translation."""

    mappings: list[dict[str, str]]
    include_ext: set[str] = field(default_factory=set)
    exclude_dir_names: set[str] = field(default_factory=set)
    prompt_template_path: Path = Path("prompt.j2")
    base_language: str = "English"
    target_language: str = "German"
    model: str = "gpt-4"
    temperature: float = 0.3
    max_concurrency: int = 5
    force: bool = False

    @classmethod
    def from_yaml(cls, path: Path, force: bool = False) -> "Config":
        """Load configuration from YAML file."""
        with path.open() as f:
            data = yaml.safe_load(f)

        include_ext = set(data.get("include_ext", [".astro", ".yml", ".yaml", ".md", ".mdx"]))
        exclude_dir_names = set(data.get("exclude_dir_names", ["node_modules", ".git", "dist"]))

        prompt_template_path = Path(data.get("prompt_template_path", "prompt.j2"))
        if not prompt_template_path.is_absolute():
            prompt_template_path = path.parent / prompt_template_path

        return cls(
            mappings=data["mappings"],
            include_ext=include_ext,
            exclude_dir_names=exclude_dir_names,
            prompt_template_path=prompt_template_path,
            base_language=data.get("base_language", "English"),
            target_language=data.get("target_language", "German"),
            model=data.get("model", "gpt-4"),
            temperature=data.get("temperature", 0.3),
            max_concurrency=data.get("max_concurrency", 5),
            force=force,
        )


class TreeTranslator:
    """Translates a directory tree of documentation files."""

    def __init__(self, config: Config, client: AsyncOpenAI | None = None) -> None:
        """Initialize the translator.

        Args:
            config: Configuration object
            client: Optional AsyncOpenAI client (for testing/DI)
        """
        self.config = config
        self.client = client
        self.semaphore = asyncio.Semaphore(config.max_concurrency)

        template_dir = config.prompt_template_path.parent
        template_name = config.prompt_template_path.name
        self.jinja_env = Environment(
            loader=FileSystemLoader(template_dir), autoescape=False  # noqa: S701
        )
        self.prompt_template = self.jinja_env.get_template(template_name)

    def _detect_file_type(self, path: Path) -> str:
        """Detect file type from extension."""
        ext = path.suffix.lower()
        if ext == ".astro":
            return "astro"
        elif ext in {".yml", ".yaml"}:
            return "yaml"
        elif ext == ".md":
            return "markdown"
        elif ext == ".mdx":
            return "mdx"
        return "unknown"

    def _render_system_prompt(self, file_type: str) -> str:
        """Render the system prompt for a given file type."""
        return self.prompt_template.render(
            file_type=file_type,
            base_language=self.config.base_language,
            target_language=self.config.target_language,
        )

    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=2, max=10),
    )
    async def _translate_content(self, content: str, file_type: str) -> str:
        """Translate file content using OpenAI API with retry logic."""
        if self.client is None:
            msg = "AsyncOpenAI client not initialized"
            raise RuntimeError(msg)

        system_prompt = self._render_system_prompt(file_type)

        response = await self.client.chat.completions.create(
            model=self.config.model,
            temperature=self.config.temperature,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": content},
            ],
        )

        return response.choices[0].message.content or ""

    async def _translate_file(self, source: Path, target: Path) -> None:
        """Translate a single file."""
        async with self.semaphore:
            if target.exists() and not self.config.force:
                return

            file_type = self._detect_file_type(source)
            content = source.read_text(encoding="utf-8")

            translated = await self._translate_content(content, file_type)

            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_text(translated, encoding="utf-8")
            print(target)

    def _should_process(self, path: Path) -> bool:
        """Check if file should be processed based on extension."""
        return path.suffix.lower() in self.config.include_ext

    def _should_skip_dir(self, dir_name: str) -> bool:
        """Check if directory should be skipped."""
        return dir_name in self.config.exclude_dir_names

    def _collect_files(self, from_dir: Path, to_dir: Path) -> list[tuple[Path, Path]]:
        """Collect all files to translate from source directory."""
        files_to_translate = []

        for item in from_dir.rglob("*"):
            if item.is_file():
                parts = item.relative_to(from_dir).parts
                if any(self._should_skip_dir(part) for part in parts):
                    continue

                if not self._should_process(item):
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


async def main_async(args: argparse.Namespace) -> None:
    """Main async entry point."""
    config_path = Path(args.config)
    config = Config.from_yaml(config_path, force=args.force)

    api_key = args.api_key or os.getenv("OPENAI_API_KEY")
    base_url = args.base_url or os.getenv("OPENAI_BASE_URL")

    client_kwargs: dict[str, Any] = {}
    if api_key:
        client_kwargs["api_key"] = api_key
    if base_url:
        client_kwargs["base_url"] = base_url

    client = AsyncOpenAI(**client_kwargs)

    translator = TreeTranslator(config, client=client)
    await translator.translate_all()


def main() -> None:
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(description="Auto-translate Astro docs tree")
    parser.add_argument("--config", required=True, help="Path to configuration YAML file")
    parser.add_argument("--api-key", help="OpenAI API key (or use OPENAI_API_KEY env var)")
    parser.add_argument("--base-url", help="OpenAI base URL (or use OPENAI_BASE_URL env var)")
    parser.add_argument("--force", action="store_true", help="Overwrite existing files")

    args = parser.parse_args()

    asyncio.run(main_async(args))


if __name__ == "__main__":
    main()
