"""Tests for auto-translate tool."""

import asyncio
from pathlib import Path
from typing import Any
from unittest.mock import AsyncMock, MagicMock

import pytest
from translate_tree import Config, TreeTranslator


class FakeChoice:
    """Fake choice object for OpenAI response."""

    def __init__(self, content: str) -> None:
        self.message = MagicMock()
        self.message.content = content


class FakeCompletion:
    """Fake completion object for OpenAI response."""

    def __init__(self, content: str) -> None:
        self.choices = [FakeChoice(content)]


class FakeAsyncOpenAI:
    """Fake AsyncOpenAI client for testing."""

    def __init__(self, translation_fn=None) -> None:
        self.chat = MagicMock()
        self.chat.completions = MagicMock()
        self.translation_fn = translation_fn or (lambda text: f"TRANSLATED: {text}")
        self.call_history: list[dict[str, Any]] = []

        async def create_completion(**kwargs: Any) -> FakeCompletion:
            self.call_history.append(kwargs)
            user_content = kwargs["messages"][1]["content"]
            translated = self.translation_fn(user_content)
            if asyncio.iscoroutine(translated):
                translated = await translated
            return FakeCompletion(translated)

        self.chat.completions.create = AsyncMock(side_effect=create_completion)


@pytest.fixture
def temp_config(tmp_path: Path) -> tuple[Path, Path]:
    """Create a temporary config file and prompt template."""
    config_path = tmp_path / "config.yml"
    prompt_path = tmp_path / "prompt.j2"

    prompt_path.write_text(
        "{% if file_type == 'astro' %}Translate Astro{% elif file_type == 'yaml' %}Translate YAML{% endif %}"
    )

    config_content = f"""
mappings:
  - from_dir: {tmp_path / 'source'}
    to_dir: {tmp_path / 'target'}

include_ext:
  - .astro
  - .md
  - .yml

exclude_dir_names:
  - node_modules
  - .git

prompt_template_path: {prompt_path}
base_language: English
target_language: German
model: gpt-4
temperature: 0.3
max_concurrency: 5
"""
    config_path.write_text(config_content)

    return config_path, tmp_path


@pytest.mark.asyncio
async def test_writes_same_relative_path(temp_config: tuple[Path, Path]) -> None:
    """Test that translator preserves relative path structure."""
    config_path, tmp_path = temp_config
    source_dir = tmp_path / "source"
    target_dir = tmp_path / "target"

    (source_dir / "nested" / "deep").mkdir(parents=True)
    (source_dir / "nested" / "deep" / "file.astro").write_text("Hello")
    (source_dir / "root.md").write_text("World")

    config = Config.from_yaml(config_path)
    fake_client = FakeAsyncOpenAI()
    translator = TreeTranslator(config, client=fake_client)

    await translator.translate_all()

    assert (target_dir / "nested" / "deep" / "file.astro").exists()
    assert (target_dir / "root.md").exists()
    assert (target_dir / "nested" / "deep" / "file.astro").read_text() == "TRANSLATED: Hello"
    assert (target_dir / "root.md").read_text() == "TRANSLATED: World"


@pytest.mark.asyncio
async def test_skips_existing_unless_force(temp_config: tuple[Path, Path]) -> None:
    """Test that existing files are skipped unless force flag is set."""
    config_path, tmp_path = temp_config
    source_dir = tmp_path / "source"
    target_dir = tmp_path / "target"

    source_dir.mkdir()
    target_dir.mkdir()
    source_file = source_dir / "test.md"
    target_file = target_dir / "test.md"

    source_file.write_text("New content")
    target_file.write_text("Old content")

    config = Config.from_yaml(config_path, force=False)
    fake_client = FakeAsyncOpenAI()
    translator = TreeTranslator(config, client=fake_client)

    await translator.translate_all()

    assert target_file.read_text() == "Old content"

    config = Config.from_yaml(config_path, force=True)
    translator = TreeTranslator(config, client=fake_client)

    await translator.translate_all()

    assert target_file.read_text() == "TRANSLATED: New content"


@pytest.mark.asyncio
async def test_filters_extensions_and_excluded_dirs(temp_config: tuple[Path, Path]) -> None:
    """Test that unsupported extensions and excluded directories are skipped."""
    config_path, tmp_path = temp_config
    source_dir = tmp_path / "source"

    (source_dir / "node_modules").mkdir(parents=True)
    (source_dir / "node_modules" / "package.md").write_text("Should not translate")

    (source_dir / "valid").mkdir()
    (source_dir / "valid" / "doc.md").write_text("Should translate")
    (source_dir / "valid" / "image.png").write_text("Binary file")

    config = Config.from_yaml(config_path)
    fake_client = FakeAsyncOpenAI()
    translator = TreeTranslator(config, client=fake_client)

    await translator.translate_all()

    target_dir = tmp_path / "target"
    assert not (target_dir / "node_modules" / "package.md").exists()
    assert not (target_dir / "valid" / "image.png").exists()
    assert (target_dir / "valid" / "doc.md").exists()


@pytest.mark.asyncio
async def test_renders_prompt_per_file_type(temp_config: tuple[Path, Path]) -> None:
    """Test that prompt template is rendered differently for each file type."""
    config_path, tmp_path = temp_config
    source_dir = tmp_path / "source"

    source_dir.mkdir()
    (source_dir / "component.astro").write_text("Astro content")
    (source_dir / "config.yml").write_text("key: value")

    config = Config.from_yaml(config_path)
    fake_client = FakeAsyncOpenAI()
    translator = TreeTranslator(config, client=fake_client)

    await translator.translate_all()

    assert len(fake_client.call_history) == 2

    astro_call = next(call for call in fake_client.call_history if "Astro content" in call["messages"][1]["content"])
    yaml_call = next(call for call in fake_client.call_history if "key: value" in call["messages"][1]["content"])

    assert "Translate Astro" in astro_call["messages"][0]["content"]
    assert "Translate YAML" in yaml_call["messages"][0]["content"]


@pytest.mark.asyncio
async def test_detect_file_type() -> None:
    """Test file type detection."""
    config = Config(mappings=[])
    translator = TreeTranslator(config, client=FakeAsyncOpenAI())

    assert translator._detect_file_type(Path("test.astro")) == "astro"
    assert translator._detect_file_type(Path("test.yml")) == "yaml"
    assert translator._detect_file_type(Path("test.yaml")) == "yaml"
    assert translator._detect_file_type(Path("test.md")) == "markdown"
    assert translator._detect_file_type(Path("test.mdx")) == "mdx"


@pytest.mark.asyncio
async def test_concurrent_translation(temp_config: tuple[Path, Path]) -> None:
    """Test that multiple files are translated concurrently."""
    config_path, tmp_path = temp_config
    source_dir = tmp_path / "source"

    source_dir.mkdir()
    for i in range(10):
        (source_dir / f"file{i}.md").write_text(f"Content {i}")

    config = Config.from_yaml(config_path)

    call_times = []

    async def slow_translation(text: str) -> str:
        call_times.append(asyncio.get_event_loop().time())
        await asyncio.sleep(0.01)
        return f"TRANSLATED: {text}"

    fake_client = FakeAsyncOpenAI(translation_fn=slow_translation)
    translator = TreeTranslator(config, client=fake_client)

    await translator.translate_all()

    time_span = max(call_times) - min(call_times)
    assert time_span < 0.1


@pytest.mark.asyncio
async def test_creates_parent_directories(temp_config: tuple[Path, Path]) -> None:
    """Test that parent directories are created automatically."""
    config_path, tmp_path = temp_config
    source_dir = tmp_path / "source"
    target_dir = tmp_path / "target"

    (source_dir / "a" / "b" / "c").mkdir(parents=True)
    (source_dir / "a" / "b" / "c" / "deep.md").write_text("Deep content")

    config = Config.from_yaml(config_path)
    fake_client = FakeAsyncOpenAI()
    translator = TreeTranslator(config, client=fake_client)

    await translator.translate_all()

    assert (target_dir / "a" / "b" / "c" / "deep.md").exists()
    assert (target_dir / "a" / "b" / "c" / "deep.md").read_text() == "TRANSLATED: Deep content"
