# Code Quality Guidelines

This project uses **Ruff** for extremely fast Python linting and formatting.
Automated checks run on `git commit` via pre-commit hooks to ensure consistency.

## Environment Setup
To ensure hooks run automatically:
1. Install development dependencies: `pip install -e ".[dev]"`
2. Install git hooks:
   ```bash
   pre-commit install
   ```

## Manual Execution Commands

**Run checks on ALL files repository-wide:**
```bash
pre-commit run --all-files
```

**Run checks on strictly staged files:**
```bash
pre-commit run
```

## Isolated Tool Commands

If you prefer to run Ruff manually without the pre-commit wrapper:

**Format Code (Auto-fix):**
```bash
ruff format .
```

**Lint Code (Check for issues):**
```bash
ruff check .
```

**Lint Code (Auto-fix safe issues):**
```bash
ruff check . --fix
```

## Emergency Bypassing
If you urgently need to bypass hooks (e.g., for an emergency hotfix), append `--no-verify` to your commit command:
```bash
git commit -m "fix(urgent): patch memory leak" --no-verify
```
*Note: Use bypasses sparingly. CI pipelines will still enforce these checks.*
