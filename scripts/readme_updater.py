from __future__ import annotations

from open_ticket_ai.scripts.util.display_file_structure import display_dir_tree
from open_ticket_ai.src.core.util.path_util import find_python_code_root_path

"""Module for updating project README files using AI-generated content.

This module contains the `ReadmeUpdater` class which automates the process of:
1. Collecting project documentation from Markdown files
2. Generating an updated README using OpenAI's language models
3. Writing the new content to the project's AI_README file
"""

from pathlib import Path

from openai import AsyncOpenAI


class ReadmeUpdater:
    """Update the AI_README file based on project documentation."""

    def __init__(self, client: AsyncOpenAI, docs_dir: Path, readme_path: Path, model: str) -> None:
        """Store dependencies for later use.

        Args:
            client: Asynchronous OpenAI client.
            docs_dir: Path to the directory containing Markdown documentation.
            readme_path: Path to the AI_README file to update.
            model: Name of the model used for text generation.
        """
        self.client = client
        self.docs_dir = docs_dir
        self.readme_path = readme_path
        self.model = model

    def _get_file_structure(self) -> str:
        """Generate a directory tree representation of the project.

        Returns:
            String representation of the directory structure.
        """
        return display_dir_tree(find_python_code_root_path().parent)

    def _get_important_files(self) -> list[Path]:
        """Identify important non-Markdown files to include in documentation.

        Returns:
            List of Path objects pointing to important project files.
        """
        root_path = find_python_code_root_path().parent
        return [
            root_path / "pyproject.toml",
            root_path / "docs" / "vitepress_docs" / "package.json",
        ]

    async def update_ai_prompt(self) -> None:
        """Generate a new README from documentation and save it.

        This method performs the following steps:
        1. Collects all Markdown files (recursively) from the stored documentation directory
           and includes predefined important non-Markdown files.
        2. Constructs a prompt by concatenating file contents with headers indicating their relative paths.
        3. Uses the OpenAI API to generate an updated README based on the documentation.
        4. Appends the project's directory structure to the generated content.
        5. Writes the final content to the stored readme path.

        The system message for the OpenAI API instructs the model to:
        - Update the project summary (AI_README.md)
        - Pay special attention to files in the '/api' directory
        - Return only the updated README in Markdown format

        The generation temperature is set to 0.2 for more deterministic outputs.

        Raises:
            FileNotFoundError: If the documentation directory or a Markdown file is not found.
            OSError: If an I/O error occurs during file operations.
            openai.OpenAIError: If the OpenAI API request fails.
        """
        root_path = find_python_code_root_path().parent
        docs_text: list[str] = []
        all_files = self._get_important_files() + list(sorted(self.docs_dir.rglob("*.md")))
        for file in all_files:
            relative = file.relative_to(root_path)
            content = file.read_text(encoding="utf-8")
            docs_text.append(f"# FILE: {relative}\n{content}")
        prompt = "\n\n".join(docs_text)
        system_msg = """
            You will write a project summary for the AI_README.md file; The target audience is an LLM;
            So give the LLM instructions on how to help the Projects Developers, Project Managers and documentation writers;
            Update it using the following documentation, paying special attention to files in the /api directory.
            Since they are always up to date.
            While the rest of the documentation can be outdated.
            Return only the README in Markdown.
            Write 2000 - 5000 words
        """
        response = await self.client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": system_msg},
                {"role": "user", "content": prompt},
            ],
            temperature=0.2,
        )
        ai_generated_content = response.choices[0].message.content

        ai_generated_content = ai_generated_content.strip() + "\nDIRECTORY STRUCTURE:\n" + self._get_file_structure()

        self.readme_path.write_text(ai_generated_content.strip(), encoding="utf-8")
