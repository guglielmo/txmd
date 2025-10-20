# GitHub Actions Workflows

This directory contains the CI/CD automation workflows for txmd.

## Workflows

### CI Workflow (`ci.yml`)

Runs on every push and pull request to `main` and `develop` branches.

**Jobs:**

1. **test** - Multi-platform, multi-version testing
   - Tests on Linux, macOS, and Windows
   - Tests Python versions: 3.9, 3.10, 3.11, 3.12
   - Runs pytest with coverage reporting
   - Uploads coverage to Codecov (Ubuntu + Python 3.11 only)
   - Uses caching for Poetry dependencies to speed up runs

2. **quality** - Code quality checks
   - Runs black (code formatting)
   - Runs isort (import sorting)
   - Runs flake8 (linting)
   - Optional mypy type checking

3. **build** - Package build verification
   - Builds the package with Poetry
   - Uploads build artifacts for inspection
   - Only runs if tests and quality checks pass

### Publish Workflow (`publish.yml`)

Publishes the package to PyPI when a new release is created.

**Triggers:**
- Automatically on GitHub release creation
- Manually via workflow dispatch (with option for Test PyPI)

**Features:**
- Verifies tag version matches `pyproject.toml` version
- Uses PyPI trusted publishing (no API tokens needed)
- Builds and publishes to PyPI or Test PyPI

## Setup Requirements

### For CI to work properly:

1. **Codecov** (optional but recommended):
   - Sign up at https://codecov.io
   - Add your repository
   - Add `CODECOV_TOKEN` to GitHub Secrets

### For Publishing to PyPI:

1. **Configure Trusted Publishing on PyPI**:
   - Go to https://pypi.org/manage/account/publishing/
   - Add a new pending publisher:
     - PyPI Project Name: `txmd`
     - Owner: `guglielmo`
     - Repository: `txmd`
     - Workflow: `publish.yml`
     - Environment: `pypi`

2. **Create PyPI environment in GitHub**:
   - Go to repository Settings > Environments
   - Create environment named `pypi`
   - Add protection rules if desired (e.g., require reviewers)

### Creating a Release

To publish a new version to PyPI:

1. Update version in `pyproject.toml`
2. Commit and push changes
3. Create a git tag: `git tag v0.1.4`
4. Push the tag: `git push origin v0.1.4`
5. Create a GitHub release from the tag
6. The publish workflow will automatically run and deploy to PyPI

Alternatively, create the release directly on GitHub:
- Go to Releases > Draft a new release
- Create a new tag (e.g., `v0.1.4`)
- Add release notes
- Publish release

## Manual Testing

To test the publish workflow without releasing to PyPI:
1. Go to Actions > Publish to PyPI
2. Click "Run workflow"
3. Check "Publish to Test PyPI instead"
4. Click "Run workflow"

## Monitoring

- **CI Status**: Check the Actions tab for build status
- **Coverage**: View coverage reports at https://codecov.io (if configured)
- **PyPI Releases**: https://pypi.org/project/txmd/
