
#!/usr/bin/env python3
"""
Cognetix GenAI Internship Project Generator

Creates a standard project directory with:
- src/, data/, eval/, docs/
- app.py
- requirements.txt
- .env.example
- .gitignore
- README.md

Existing files are preserved by default.
"""

import argparse
import re
import sys
from pathlib import Path


DEFAULT_PROJECT_NAME = "Cognetix_ProjectName"

DIRECTORIES = [
    "src",
    "data",
    "eval",
    "docs",
]

FILES = {
    "app.py": '''"""
Main application entry point for the Cognetix GenAI project.
"""

import streamlit as st


def main():
    """Render the starter Streamlit application."""
    st.set_page_config(
        page_title="Cognetix GenAI Project",
        page_icon="🤖",
        layout="wide",
    )

    st.title("Cognetix GenAI Project")
    st.write("Welcome! Replace this placeholder with your application.")

    st.info(
        "Next steps: configure your LLM client, add prompts in src/, "
        "and create evaluations in eval/."
    )


if __name__ == "__main__":
    main()
''',

    "requirements.txt": """python-dotenv
openai
streamlit
""",

    ".env.example": """# Copy this file to .env and fill in your actual configuration.
# Never commit your real .env file or API keys.

LLM_API_KEY=your_api_key_here
LLM_BASE_URL=https://api.openai.com/v1
MODEL_NAME=your_model_name
MAX_TOKENS=600
""",

    ".gitignore": """# Environment variables and secrets
.env
.env.*
!.env.example
*.key

# Python virtual environments
.venv/
venv/
env/

# Python cache
__pycache__/
*.py[cod]

# Local data and generated files
chroma_db/
uploads/
*.log

# Editor and operating-system files
.vscode/
.idea/
.DS_Store
Thumbs.db
""",

    "README.md": """# Cognetix GenAI Developer Internship Project

## Objective

Describe the problem your GenAI application solves, its target users,
and the expected outcome.

## Live Links

- **Live Application:** Add deployment URL here.
- **GitHub Repository:** Add repository URL here.
- **Demo Video:** Add 60–90 second demo URL here.

## Architecture

Describe the main components and how data flows through the application.

Suggested structure:

- `app.py` — application entry point
- `src/` — prompts, helper functions, and LLM clients
- `data/` — sample datasets and mock files
- `eval/` — test questions, evaluation results, and reports
- `docs/` — diagrams, screenshots, and supporting documentation

Add architecture diagrams to `docs/`.

## Setup

### Prerequisites

- Python 3.10 or newer
- pip
- Git

### Installation

1. Clone your repository or open the project directory.
2. Create a virtual environment:

   ```bash
   python -m venv .venv
   ```

3. Activate it.

   **Windows PowerShell:**

   ```powershell
   .\\.venv\\Scripts\\Activate.ps1
   ```

   **macOS/Linux:**

   ```bash
   source .venv/bin/activate
   ```

4. Install dependencies:

   ```bash
   python -m pip install -r requirements.txt
   ```

5. Copy `.env.example` to `.env` and configure your settings.

   **Windows PowerShell:**

   ```powershell
   Copy-Item .env.example .env
   ```

   **macOS/Linux:**

   ```bash
   cp .env.example .env
   ```

6. Run the application:

   ```bash
   streamlit run app.py
   ```

Never commit `.env` or expose API keys in source code, screenshots,
logs, or public repositories.

## How It Works

Explain the workflow from user input to prompt construction, LLM
invocation, response processing, and final output.

## Evaluation Results

Document your test questions, evaluation methodology, metrics,
observed results, and any relevant screenshots or reports from `eval/`.

Do not report placeholder or unmeasured results as actual findings.

## Limitations

List known limitations, assumptions, failure cases, and possible
future improvements.

## Author

- **Name:** Add your name here.
- **Program:** Cognetix GenAI Developer Internship
- **Contact:** Add your professional contact or portfolio link.
"""
}


def validate_project_name(name: str) -> str:
    """Validate a single directory name to prevent unsafe paths."""
    name = name.strip()

    if not name:
        raise ValueError("Project name cannot be empty.")

    # Allow common directory-name characters; reject path separators
    # and special path components to prevent path traversal.
    if name in {".", ".."} or not re.fullmatch(
        r"[A-Za-z0-9][A-Za-z0-9._ -]*", name
    ):
        raise ValueError(
            "Use a simple project name containing letters, numbers, "
            "spaces, hyphens, underscores, or periods. "
            "Do not provide a path."
        )

    return name


def create_project(project_name: str, base_dir: Path) -> None:
    """Create the project tree and template files without overwriting."""
    project_dir = base_dir / project_name

    # Create the root directory and requested subdirectories.
    project_dir.mkdir(parents=True, exist_ok=True)
    print(f"[OK] Project directory: {project_dir.resolve()}")

    for directory in DIRECTORIES:
        path = project_dir / directory
        path.mkdir(parents=True, exist_ok=True)
        print(f"[OK] Directory ready: {path.relative_to(base_dir)}")

    # Create boilerplate files only when they do not already exist.
    for filename, content in FILES.items():
        file_path = project_dir / filename

        if file_path.exists():
            print(f"[SKIP] File already exists; preserved: {file_path}")
            continue

        try:
            file_path.write_text(content, encoding="utf-8")
            print(f"[OK] File created: {file_path.relative_to(base_dir)}")
        except OSError as exc:
            print(f"[ERROR] Could not create {file_path}: {exc}")
            raise

    print("\nProject setup finished.")
    print(f"Project location: {project_dir.resolve()}")
    print("Next: install dependencies and configure your local .env file.")


def main() -> int:
    """Parse command-line arguments and run the generator."""
    parser = argparse.ArgumentParser(
        description="Create a Cognetix GenAI internship project template."
    )
    parser.add_argument(
        "project_name",
        nargs="?",
        default=None,
        help=f"Project folder name (default: {DEFAULT_PROJECT_NAME})",
    )
    parser.add_argument(
        "--base-dir",
        type=Path,
        default=Path.cwd(),
        help="Parent directory for the project (default: current directory)",
    )
    args = parser.parse_args()

    project_name = args.project_name

    # Prompt interactively when no name was supplied in the CLI.
    if project_name is None and sys.stdin.isatty():
        entered_name = input(
            f"Project name [{DEFAULT_PROJECT_NAME}]: "
        ).strip()
        project_name = entered_name or DEFAULT_PROJECT_NAME
    elif project_name is None:
        project_name = DEFAULT_PROJECT_NAME

    try:
        project_name = validate_project_name(project_name)
        base_dir = args.base_dir.expanduser().resolve()

        if not base_dir.exists():
            base_dir.mkdir(parents=True, exist_ok=True)

        if not base_dir.is_dir():
            raise NotADirectoryError(
                f"Base path is not a directory: {base_dir}"
            )

        create_project(project_name, base_dir)
        return 0

    except (ValueError, OSError) as exc:
        print(f"[ERROR] {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
