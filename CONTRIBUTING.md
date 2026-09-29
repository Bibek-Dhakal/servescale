# Contributing to ServeScale

Thank you for your interest in contributing! To maintain consistency and automate our release pipelines, we enforce specific guidelines.

## Code Quality
Ensure all code passes formatting, linting, and testing before submitting a Pull Request.
We use `ruff` for linting and formatting. Git pre-commit hooks are configured to automate this.
See [CODE_QUALITY.md](CODE_QUALITY.md) for setup details.

## Conventional Commits (Strictly Enforced)
We use `release-please` to automate versioning and `CHANGELOG.md` generation based directly on commit history.
**All commit messages and PR titles MUST follow the Conventional Commits specification.**

### Format
```text
<type>(<optional scope>): <description>

[optional body]

[optional footer(s)]
```

### Allowed Types
* `feat`: A new feature (correlates with a MINOR semantic version bump).
* `fix`: A bug fix (correlates with a PATCH semantic version bump).
* `feat!:` or `fix!:`: A breaking change (correlates with a MAJOR semantic version bump).
* `docs`: Documentation changes.
* `chore`: Routine tasks, maintenance, dependency updates.
* `refactor`: Code refactoring without adding features or fixing bugs.
* `test`: Adding or updating tests.

### Examples
* `feat(api): add batch inference endpoint`
* `fix(k8s): resolve readiness probe timeout issue`
* `docs: update deployment instructions`
* `feat!(model): change expected input tensor shape`

## Release Process
1. Commits pushed to `main` are aggregated by the `.github/workflows/release-please.yml` action.
2. A Release PR is automatically generated/updated (`chore: release x.y.z`).
3. Merging the Release PR finalizes the release, tags the repository, and updates the `CHANGELOG.md`.
