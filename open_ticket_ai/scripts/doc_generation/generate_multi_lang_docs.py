"""Module for translating Markdown documentation files into multiple languages.

This module provides functionality to asynchronously translate Markdown files using
OpenAI's API. It supports translating entire directory structures while preserving
file hierarchy and supports multiple target languages.

The main class `Translator` handles:
- Initialization with translation parameters
- Text translation with automatic retries
- File processing and output writing
- Concurrent directory translation

Example usage:
    client = AsyncOpenAI(api_key="your_api_key")
    translator = Translator(client, base_language="en")
    asyncio.run(translator.translate_directory(
        docs_src=Path("docs"),
        languages=["es", "fr", "de"],
        model="gpt-4",
        out_dir=Path("translated_docs")
    ))

Note:
    The translation instruction prompt is read from 'translation_instruction.txt'
    by default. This file should contain system instructions for the translation model.
"""
from __future__ import annotations

import asyncio
from hashlib import sha256
from pathlib import Path
from typing import List

from openai import AsyncOpenAI
import tenacity
from tenacity import stop_after_attempt, wait_exponential


class Translator:
    """Translates Markdown documentation files into multiple languages.

    This class handles the translation of Markdown files using OpenAI's API. It supports
    translating entire directory structures while preserving the file hierarchy and supports
    multiple target languages.

    Attributes:
        client (AsyncOpenAI): An asynchronous OpenAI client instance for API interactions.
        base_language (str): The source language of the documents (e.g., 'en').
        translation_instruction (str): The system prompt instruction for translation.

    Example:
        client = AsyncOpenAI(api_key="your_api_key")
        translator = Translator(client, base_language="en")
        asyncio.run(translator.translate_directory(
            docs_src=Path("docs"),
            languages=["es", "fr", "de"],
            model="gpt-4",
            out_dir=Path("translated_docs")
        ))
    """

    def __init__(
        self,
        client: AsyncOpenAI,
        base_language: str,
        languages: List[str],
        model: str,
        translation_file_path: Path = None
    ) -> None:
        """Initializes the Translator instance.

        Args:
            client: An asynchronous OpenAI client instance for API interactions.
            base_language: Language code (e.g., 'en') representing the source language of documents.
            translation_file_path: Path to a file containing the translation instruction for the system prompt.
                If not provided, defaults to "translation_instruction.txt" in the same directory as this module.

        Raises:
            FileNotFoundError: If the translation instruction file is not found.
            OSError: If there is an error reading the translation instruction file.
        """
        if translation_file_path is None:
            translation_file_path = Path(__file__).parent / "translation_instruction.txt"
        self.client = client
        self.base_language = base_language
        self.translation_instruction = translation_file_path.read_text(encoding="utf-8").strip()
        self.languages = languages
        self.model = model
        self.used_file_paths = set()

    def initialize_hash_file(self, root: Path) -> None:
        """Initializes the hash file to track changes in Markdown files.

        Creates a `.hashes.json` file in the root directory if it does not exist.
        This file will store the SHA-256 hashes of the Markdown files to detect changes.

        Args:
            root: The root directory where the `.hashes.json` file should be created.

        Raises:
            OSError: If there is an issue creating or writing to the hash file.
        """
        hash_file = root / ".hashes.json"
        if not hash_file.exists():
            hash_file.write_text("{}", encoding="utf-8")

    def create_hash_for_file(self, path: Path) -> str:
        """Creates a SHA-256 hash for the content of a file.

        Args:

            """
        return sha256(path.read_bytes()).hexdigest()

    def update_hash_file(self, root: Path, relative: Path, new_hash: str) -> None:
        """Updates the hash file with a new hash for a specific file.

        Args:
            root: The root directory where the `.hashes.json` file is located.
            relative: The relative path of the file whose hash is being updated.
            new_hash: The new SHA-256 hash to store for the file.

        Raises:
            OSError: If there is an issue writing to the hash file.
        """
        hash_file = root / ".hashes.json"
        import json
        with hash_file.open(encoding="utf-8") as f:
            previous_hashes = json.load(f)
        previous_hashes[str(relative)] = new_hash
        with hash_file.open("w", encoding="utf-8") as f:
            json.dump(previous_hashes, f, indent=2)

    def has_file_changed(
        self, root: Path, relative: Path, new_text_hash: str
    ) -> bool:
        """Checks if a file has changed by comparing its current hash with the stored hash.

        Args:
            root: The root directory where the `.hashes.json` file is located.
            relative: The relative path of the file to check.
            new_text_hash: The new SHA-256 hash of the file content.

        Returns:
            bool: True if the file has changed, False otherwise.
        """
        previous_hash_file = root / ".hashes.json"
        if previous_hash_file.exists():
            import json
            with previous_hash_file.open(encoding="utf-8") as f:
                previous_hashes = json.load(f)
            old_text_hash = previous_hashes.get(str(relative), None)
            return old_text_hash != new_text_hash
        return True

    @tenacity.retry(
        wait=wait_exponential(multiplier=2, min=2, max=60),
        stop=stop_after_attempt(6),
    )
    async def translate_text(self, content: str, target_lang: str) -> str:
        """Translates Markdown content to a target language using OpenAI's API.

        This method uses exponential backoff and retries up to 6 times on failure.

        Args:
            content: The Markdown text to translate.
            target_lang: Target language code (e.g., 'es' for Spanish).
            model: OpenAI model identifier to use for translation.

        Returns:
            The translated Markdown content as a string.

        Raises:
            tenacity.RetryError: If all retry attempts fail.
        """
        response = await self.client.chat.completions.create(
            model=self.model,
            messages=[
                {
                    "role": "system",
                    "content": (
                        self.translation_instruction
                    ),
                },
                {
                    "role": "user",
                    "content": f"Translate the following markdown to {target_lang}:\n\n{content}",
                },
            ],
            temperature=0.2,
        )
        return response.choices[0].message.content

    def set_lang_files_used(self, out_dir: Path, relative: Path) -> None:
        for lang in self.languages:
            out_file = out_dir / lang / relative
            self.used_file_paths.add(str(out_file))

    async def process_file(
        self,
        path: Path,
        root: Path,
        out_dir: Path,
    ) -> None:
        async def write_lang_translated_file(
            lang: str, text: str, relative: Path
        ) -> None:
            if lang == self.base_language:
                translated = text
            else:
                translated = await self.translate_text(text, lang)
            out_file = out_dir / lang / relative
            out_file.parent.mkdir(parents=True, exist_ok=True)
            out_file.write_text(translated, encoding="utf-8")
            print(f"Wrote {out_file}")
        """Processes a single Markdown file for translation into multiple languages.

        For each target language:
        1. Reads the source Markdown file
        2. Translates content (skips translation for base language)
        3. Writes translated content to appropriate output path

        Args:
            path: Absolute path to the source Markdown file.
            root: Root directory of the documentation source tree.
            languages: List of target language codes to translate into.
            model: OpenAI model identifier for translation.
            out_dir: Base output directory for translated files.

        Raises:
            tenacity.RetryError: If translation fails after multiple retries.
            OSError: If there is an issue reading the source file or writing the translated file.
        """
        text = path.read_text(encoding="utf-8")
        relative = path.relative_to(root)
        self.set_lang_files_used(out_dir, relative)
        new_text_hash = self.create_hash_for_file(path)
        if not self.has_file_changed(root, relative, new_text_hash):
            print(f"Skipping {relative} as it has not changed.")
            return
        self.update_hash_file(root, relative, new_text_hash)
        file_tasks = [
            write_lang_translated_file(lang, text, relative)
            for lang in self.languages
        ]
        await asyncio.gather(*file_tasks)

    def clean_up_unused_files(self, out_dir: Path) -> None:
        """Cleans up files in the output directory that were not used during translation.

        This method removes any files in the output directory that were not created
        during the translation process, ensuring that only relevant translated files remain.

        Args:
            out_dir: Base output directory where translated files are stored.

        Raises:
            OSError: If there is an issue removing files or directories.
        """
        for lang in self.languages:
            lang_dir = out_dir / lang
            if lang_dir.exists():
                for file in lang_dir.rglob("*.md"):
                    if str(file) not in self.used_file_paths and file.is_file():
                        print(f"Removing unused file: {file}")
                        file.unlink()
                # Remove empty directories
                for dir in reversed(list(lang_dir.rglob("*"))):
                    if dir.is_dir() and not any(dir.iterdir()):
                        print(f"Removing empty directory: {dir}")
                        dir.rmdir()
    async def translate_directory(
        self,
        docs_src: Path,
        out_dir: Path,
    ) -> None:
        start_time = asyncio.get_event_loop().time()
        """Translates an entire directory of Markdown files concurrently.

        Walks through all `.md` files in `docs_dir`, creates translation tasks
        for each file, and processes them asynchronously.

        Args:
            docs_src: Directory containing source Markdown files.
            languages: List of target language codes for translation.
            model: OpenAI model identifier for translation.
            out_dir: Base output directory for translated files.

        Raises:
            tenacity.RetryError: If translation of any file fails after retries.
            OSError: If any file I/O operation fails during processing.
        """
        self.initialize_hash_file(docs_src)
        tasks = []
        for md_file in docs_src.rglob("*.md"):
            tasks.append(self.process_file(md_file, docs_src, out_dir))
        await asyncio.gather(*tasks)
        self.clean_up_unused_files(out_dir)
        end_time = asyncio.get_event_loop().time()
        print(f"Translation completed in {end_time - start_time:.2f} seconds.")
