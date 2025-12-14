# Releasing a New Version

This project uses GitHub Actions with PyPI Trusted Publishing for releases.

## Steps to Release

### 1. Update Version Numbers

Update the version in **both** files:

- `pyproject.toml`:
  ```toml
  version = "X.Y.Z"
  ```

- `numbasom/__init__.py`:
  ```python
  __version__ = "X.Y.Z"
  ```

### 2. Commit and Push

```bash
git add pyproject.toml numbasom/__init__.py
git commit -m "Bump version to X.Y.Z"
git push
```

### 3. Create a GitHub Release

1. Go to the repository on GitHub
2. Click **Releases** → **Create a new release**
3. Click **Choose a tag** → type `vX.Y.Z` (e.g., `v0.1.0`) → **Create new tag**
4. Set **Release title** to `vX.Y.Z`
5. Add release notes describing what changed
6. Click **Publish release**

### 4. Automatic Publishing

The `publish.yml` workflow will automatically:
- Build the package
- Publish to PyPI using trusted publishing (no API token needed)

You can monitor the progress in the **Actions** tab.

## Version Numbering

This project follows [Semantic Versioning](https://semver.org/):

- **MAJOR** (X): Breaking changes to the public API
- **MINOR** (Y): New features, backwards compatible
- **PATCH** (Z): Bug fixes, backwards compatible

## Verifying the Release

After the workflow completes:

1. Check [PyPI](https://pypi.org/project/numbasom/) for the new version
2. Test installation: `pip install numbasom==X.Y.Z`
