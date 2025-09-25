# FILE_PATH: open_ticket_ai\scripts\doc_generation\add_docstrings.py
"""Automatically adds long Google style docstrings to Python files using AI."""

import asyncio
from pathlib import Path
import re

from openai import AsyncOpenAI

"""Automatically adds long Google style docstrings to Python files using AI."""


class DocstringGenerator:
    """Generate docstrings for Python files using an injected AsyncOpenAI client.

    This class provides functionality to:
    - Discover Python files in a directory while respecting exclusion rules
    - Send file content to an AI model for docstring generation
    - Clean and process AI responses
    - Update files with generated docstrings

    Attributes:
        client (AsyncOpenAI): Asynchronous OpenAI client for API interactions.
        base_path (Path): Root directory to search for Python files.
        exclude_dirs (set[str]): Directory names to exclude from processing.
        exclude_files (set[str]): Specific filenames to exclude from processing.
        model (str): AI model identifier for docstring generation.
    """

    def __init__(
        self,
        client: AsyncOpenAI,
        base_path: Path,
        exclude_dirs: set[str],
        exclude_files: set[str],
        model: str = "deepseek/deepseek-r1-0528",
    ) -> None:
        """Initialize the DocstringGenerator instance.

        Args:
            client (AsyncOpenAI): An asynchronous OpenAI client for API interactions.
            base_path (Path): Root directory to search for Python files.
            exclude_dirs (set[str]): Directory names to exclude from processing.
            exclude_files (set[str]): Specific filenames to exclude from processing.
            model (str, optional): AI model identifier for docstring generation.
                Defaults to "deepseek/deepseek-r1-0528".
        """
        self.client = client
        self.base_path = base_path
        self.exclude_dirs = exclude_dirs
        self.exclude_files = exclude_files
        self.model = model

    def find_python_files(self) -> list[Path]:
        """Return all Python files in ``base_path`` respecting exclusion rules.

        Walks through the directory tree starting at ``base_path`` and collects
        all Python files (.py) that are not in excluded directories or named in
        the excluded files list.

        Returns:
            list[Path]: List of Path objects representing Python files to process.
        """
        py_files = []
        for item in self.base_path.rglob("*.py"):
            if (
                not any(part in self.exclude_dirs for part in item.parts)
                and item.name not in self.exclude_files
            ):
                py_files.append(item)
        print(f"Found {len(py_files)} Python files to process.")
        return py_files

    @staticmethod
    def clean_ai_response(response_text: str) -> str:
        """Extract Python code from a response that may contain Markdown fences.

        Args:
            response_text (str): Raw response text from the AI model.

        Returns:
            str: Cleaned Python code with Markdown fences removed.

        Note:
            If no code block is found, returns the original text stripped of
            leading/trailing whitespace.
        """
        code_block_pattern = re.compile(r"```python\n(.*?)\n```", re.DOTALL)
        match = code_block_pattern.search(response_text)
        if match:
            return match.group(1).strip()
        return response_text.strip()

    async def add_docstrings_to_file_content(self, file_content: str) -> str | None:
        """Send file content to the AI model and return the updated version.

        Args:
            file_content (str): Original Python file content to process.

        Returns:
            str | None: Updated file content with docstrings added, or None on error.

        Note:
            Uses a predefined prompt that instructs the AI model to add Google-style
            docstrings to all public classes, methods, and functions missing them.
        """
        prompt = f"""
        You are an expert Python developer specializing in writing high-quality,
         human-readable documentation.
        Your task is to analyze the following Python file and add comprehensive docstrings to all
         public classes, methods, and functions that are missing them.

        **Docstring Requirements:**
        1.  **Style:** All docstrings MUST strictly follow the **Google Python Style Guide**.
        2.  **Formatting:** Use **Markdown** for rich text formatting within the docstrings
        (e.g., for `Args`, `Returns`, `Raises` sections). Do **not** use HTML tags.
        Wrap Code blocks in triple backticks with the language specified as `python`.
        Do not write >>>
        3.  **Detail Level:** The length and detail of your descriptions should be proportional to
        the complexity of the code.
            -   A simple, self-explanatory attribute may only need a brief phrase.
            -   A complex class or function with intricate logic requires a thorough explanation of
             its purpose, behavior, arguments, and return values.

        **CRITICAL Output Rules:**
        -   **Return the ENTIRE file content.** Your output must be the complete Python script,
         including all original code and your new docstrings.
        -   **DO NOT change any existing code.** You must not refactor, alter,
         or remove any part of the Python logic. Your only job is to add documentation.
        -   **RAW PYTHON CODE ONLY.** Your response MUST be only the raw Python code.
         Do not include any surrounding text, explanations, notes, or commentary. Most importantly,
          **DO NOT wrap the full file code in Markdown code fences** (i.e., no ```python or ```).
           The output must be immediately ready to be saved as a `.py` file.

        Here is the file content:
        {file_content}
        """
        try:
            response = await self.client.chat.completions.create(
                model="deepseek/deepseek-r1-0528",
                messages=[
                    {
                        "role": "system",
                        "content": (
                            "You are a helpful Python assistant that adds docstrings to code."
                        ),
                    },
                    {"role": "user", "content": prompt},
                ],
                temperature=0.1,
            )
            new_content = response.choices[0].message.content
            return self.clean_ai_response(new_content)
        except Exception as exc:  # pragma: no cover - guard for unexpected failures
            print(f"Error calling AI model: {exc}")
            return None

    async def process_file(self, file_path: Path) -> None:
        """Process a single Python file by adding docstrings and saving changes.

        Args:
            file_path (Path): Path to the Python file to process.

        Steps:
            1. Reads original file content
            2. Skips empty files
            3. Sends content to AI for docstring generation
            4. Writes updated content back if changes exist

        Note:
            Prints status messages throughout the process and handles exceptions
            during file operations.
        """
        print(f"-> Processing: {file_path}")
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                original_content = f.read()

            if not original_content.strip():
                print(f"   - Skipping empty file: {file_path}")
                return

            print("   - Sending to AI for docstring generation...")
            new_content = await self.add_docstrings_to_file_content(original_content)

            if new_content and new_content != original_content:
                print("   - AI returned updated content. Writing to file.")
                with open(file_path, "w", encoding="utf-8") as f:
                    f.write(new_content)
                print(f"   - Successfully updated: {file_path}")
            elif not new_content:
                print(f"   - Failed to get a valid response from AI for {file_path}.")
            else:
                print(f"   - No changes were made by the AI for {file_path}.")
        except Exception as exc:  # pragma: no cover - safeguard around file ops
            print(f"   - Could not process file {file_path}: {exc}")

    async def run(self) -> None:
        """Run the docstring generation over all discovered Python files.

        Steps:
            1. Discovers Python files respecting exclusion rules
            2. Processes files concurrently using asyncio
            3. Prints summary upon completion

        Note:
            Skips processing if no Python files are found.
        """
        print("Starting docstring generation using whole-file processing...")
        py_files = self.find_python_files()

        if not py_files:
            print("No Python files found to process. Exiting.")
            return

        tasks = [self.process_file(file) for file in py_files]
        await asyncio.gather(*tasks)
        print("\nAll files processed. Docstring generation complete.")


async def main() -> None:
    """Parse command-line arguments and run the docstring generation process.

    This function:
      - Sets up an argument parser to read command-line options
      - Validates the provided base directory exists
      - Initializes the OpenAI client using the OPENAI_API_KEY environment variable
      - Creates and runs the DocstringGenerator

    Command-line arguments:
      --base_path: Base directory to search for Python files (default: current directory)
      --exclude_dirs: Comma-separated list of directories to exclude (default: 'venv,.git')
      --exclude_files: Comma-separated list of files to exclude (default: '__init__.py')
      --model: AI model to use for docstring generation (default: 'deepseek/deepseek-r1-0528')

    Raises:
        SystemExit: If base_path doesn't exist or OPENAI_API_KEY is missing.
    """
    parser = argparse.ArgumentParser(
        description="Automatically add Google-style docstrings to Python files using AI.",
    )
    parser.add_argument(
        "--base_path",
        type=Path,
        default=Path.cwd(),
        help="Base directory to search for Python files (default: current directory).",
    )
    parser.add_argument(
        "--exclude_dirs",
        type=str,
        default="venv,.git",
        help="Comma-separated list of directories to exclude (default: 'venv,.git').",
    )
    parser.add_argument(
        "--exclude_files",
        type=str,
        default="__init__.py",
        help="Comma-separated list of files to exclude (default: '__init__.py').",
    )
    parser.add_argument(
        "--model",
        type=str,
        default="deepseek/deepseek-r1-0528",
        help="AI model to use for docstring generation (default: deepseek-r1-0528).",
    )
    args = parser.parse_args()

    base_path = args.base_path
    if not base_path.exists():
        print(f"Error: The base path '{base_path}' does not exist.")
        raise SystemExit(1)

    exclude_dirs = set(args.exclude_dirs.split(",")) if args.exclude_dirs else set()
    exclude_files = set(args.exclude_files.split(",")) if args.exclude_files else set()

    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        print("Error: OPENAI_API_KEY environment variable not set.")
        raise SystemExit(1)

    client = AsyncOpenAI(api_key=api_key)
    generator = DocstringGenerator(
        client=client,
        base_path=base_path,
        exclude_dirs=exclude_dirs,
        exclude_files=exclude_files,
        model=args.model,
    )
    await generator.run()


if __name__ == "__main__":
    asyncio.run(main())
