## Package Checklist

- [X] src/ layout
- [ ] ruff + mypy config
- [ ] pyproject.toml metadata
- [ ] requires-python
- [ ] dev optional deps
- [ ] pytest working
- [ ] CI matrix
- [ ] coverage reporting
- [ ] LICENSE file
- [ ] README badges
- [ ] GitHub Pages
- [ ] release.yml (tag → release)
- [ ] importlib.metadata version

---

*Phase 1 - Packaging Foundation*
- pyproject.toml
- metadata
- requires-python
- dev optional deps
- editable install working
- version via importlib.metadata

*Phase 2 – Tooling & Quality*
- ruff config
- mypy config
- pytest wired up
- coverage

*Phase 3 – CI & Automation*
- GitHub Actions matrix
- coverage reporting badge
- README badges
- release.yml (tag → GitHub release)
- optional PyPI publish
- optional Pages

---

## Notes on pyproject.toml

The project uses pyproject.toml as the single source of truth for packaging
configuration following PEP 621.  The project uses setuptools as the build
backend.  So this will work with `pip install -e .[dev]` and `python -m build`.

--- 

### The Build System Section

- `setuptools` is the backend
- `wheel` is required for building distribution artifacts
- Using `setuptools.build_meta` is the standard PEP 517 backend

```
[build-system]
requires = ["setuptools>=68", "wheel"]
build-backend = "setuptools.build_meta"
```

---

### Project Metadata Section

- Version is defined here
- Supported Python version is defined (>=3.14)
- MIT license is specified

```
[project]
name = "rpgcharacters"
version = "0.1.0"
description = "Character generation and utilities for Basic Fantasy RPG."
readme = "README.md"
requires-python = ">=3.14"
license = { file = "LICENSE" }
authors = [
    { name = "Jason Tennant" }
]
```

Note: The version of the package defined in pyproject.toml can be accessed with
`importlib.metadata.version()` in the code.  Example below:

```python
from importlib.metadata import PackageNotFoundError, version

def _project_version() -> str:
    try:
        return version("rpgcharacters")  # must match [project].name in pyproject.toml
    except PackageNotFoundError:
        return "unknown"
```

---

### Optional Dependencies Section (dev)

- Enables `pip install -e .[dev]`
- Clean separation between runtime and development tooling
- Helps make CI setup simpler

```
[project.optional-dependencies]
dev = [
    "pytest",
    "pytest-cov",
    "ruff",
    "mypy",
    "build",
]
```

---

### src Layout Configuration

- The src/ layout is intentionally chosen
- Forces packagin correctness

```
[tool.setuptools]
package-dir = {"" = "src"}

[tool.setuptools.packages.find]
where = ["src"]
```

---

#### src Layout Configuration (types)

- Added a py.typed file in the src/rpgcharacters directory
- Allows for mypy to discover types for this package when it is a dependency for
  other projects.

```
[tool.setuptools.package-data]
"rpgcharacters" = ["py.typed"]
```

---

### Ruff Configuration Section

- Defines a baseline for Ruff
- Running `ruff check . --fix` allows Ruff to auto-fix what it can

```
# ---------------------------------------------
[tool.ruff]
line-length = 100
target-version = "py314"

[tool.ruff.lint]
select = [
  "E",  # pycodestyle errors
  "F",  # pyflakes
  "I",  # import sorting
  "UP", # pyupgrade
]
ignore = []

[tool.ruff.format]
quote-style = "double"
indent-style = "space"
```

---

### Mypy Configuration Section

- TIP: Don't start with strict initially, tighten it later

```
[tool.mypy]
python_version = "3.14"
warn_unused_configs = true
warn_return_any = true
warn_unused_ignores = true
disallow_any_generics = true
```

---

### Pytest Configuration Section

- Lock test discovery
- Cleaner output

```
[tool.pytest.ini_options]
testpaths = ["tests"]
addopts = "-ra"
```

Configuration for code coverage.

- `source = ["rpgcharacters"]` limits coverage to my package
- `branch = true` catches logic gaps, not just line execution
- `omit` will exclude what I don't want to test

```
[tool.coverage.run]
branch = true
source = ["rpgcharacters"]
omit = [
    "src/rpgcharacters/cli.py",
]

[tool.coverage.report]
show_missing = true
skip_covered = true
```

Note for coverage testing.  Run:
`pytest --cov=src --cov-report=term-missing`

---

## Local Development Tooling (DRAFT)

The following will be ran to install the project locally for development:

```
pip install -e .[dev]
```

The following tools will be ran to verify the project is looking good:

```
pytest
pytest --cov=src --cov-report=term-missing
ruff check .
mypy src
python -m build
```

---


