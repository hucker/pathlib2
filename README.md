
![Python](https://img.shields.io/badge/python-3.8--3.13-blue?logo=python&logoColor=white&style=flat)
![Coverage](https://img.shields.io/badge/coverage-95%25-brightgreen?style=flat)
![Ruff](https://img.shields.io/badge/linting-ruff-blue?logo=ruff&logoColor=white&style=flat)


# pathlib2: Seamless Multi-Extension Globbing for pathlib

> **Note:** `Path2` is a drop-in subclass of `pathlib.Path` with enhanced, declarative multi-extension globbing. Use `Path2` in place of `Path` for all new features below.

Seamlessly filter files by multiple extensions using a single, declarative glob pattern—no manual filtering, no boilerplate. 100% backward compatible with pathlib globbing: standard patterns behave exactly as before; only curly-brace patterns or explicit flags change the default behavior. Declarative usage makes your code more readable and intent-driven.

## Quick Usage


**Before (manual, with pathlib):**

```python
from pathlib import Path
count = 0
for f in Path('.').glob('*'):
    if f.is_file() and f.suffix in {'.csv', '.xls', '.xlsx'}:
        count += 1
print(f"Found {count} matching files.")
```


**After (declarative, with pathlib2):**

```python
from pathlib2.pathlib2 import Path2
num_files = sum(1 for f in Path2('.').glob('*.{csv,xls,xlsx}'))
print(f"Found {num_files} matching files.")
```


**Before (manual, with pathlib, finding largest size):**

```python
from pathlib import Path
largest_size = max((f.stat().st_size for f in Path('.').glob('*') if f.suffix in {'.csv', '.xlsx'} and f.is_file()), default=0)
print(f"Largest file size: {largest_size}")
```


**After (declarative, with pathlib2, finding largest size):**

```python
from pathlib2.pathlib2 import Path2
largest_size = max((f.stat().st_size for f in Path2('.').glob('*.{csv,xlsx}')), default=0)
print(f"Largest file size: {largest_size}")
```


## Highlights

- Patterns like `*.{csv,xls}` match all files with any of the listed extensions (not directories).
- By default, `*.{ext}` patterns match only files, making common use cases declarative and concise.
- Opt-in to include directories or files using `include_files` and `include_dirs` flags.
- Standard patterns (e.g., `*.txt`) match both files and directories, preserving 100% backward compatibility.

See `test/test_legacy_compat.py` for tests demonstrating legacy compatibility and new behaviors.


# PEP Proposal: Seamless Multi-Extension Globbing for pathlib
## Abstract

This proposal aims to make multi-extension file filtering a declarative, drop-in enhancement for Python's `pathlib` glob methods. By supporting patterns
like `*.{csv,xls,xlsx}` directly in `Path.glob` and `Path.rglob`, users can filter by multiple extensions with a single, expressive pattern—no extra loops, no manual filtering, and no boilerplate.

**Note:** The sample code uses a subclass (`Path2`) for demonstration purposes only. The intent of this proposal is for this feature to be 
integrated directly into the standard `pathlib.Path` class.

## Motivation


Filtering files by multiple extensions is a common, real-world need in data science, automation, and scripting. Having a compact, declarative option for globbing is especially conducive to using comprehensions and generators, making code readable and concise. Users likely expect to write:


```python
# Example: find the largest matching file using a generator expression
largest = max((f for f in Path('.').glob('*.{csv,xls,xlsx}')), key=lambda f: f.stat().st_size)
print(f"Largest file: {largest} ({largest.stat().st_size} bytes)")
```

and have it "just work" matching all relevant files, regardless of extension or platform. Pathlib globbing requires more verbose code than to filter files and verify extensions for everyday use cases.

## Design Philosophy

- **Drop-in usability:** The enhanced is 100% backwards compatible with `pathlib` methods.
- **Expressiveness and declarative style:** Users can specify multiple extensions in a single, declarative pattern, just as they would in Unix shells.
- **Efficiency:** The implementation avoids possible repeated directory scans and removes boiler plate checking.
- **Cross-platform:** The feature behaves consistently on all platforms.
- **Comprehensions:** Because of the declarative notation, generators and comprehensions are easier to reason about.

## Specification (Prototype)

### API Signature

```python
Path.glob(
    self,
    pattern: str,
    include_files: bool | None = None,
    include_dirs: bool | None = None,
    **kwargs
) -> Iterator[Path]
```

### Arguments

- `pattern` (str): Glob pattern. Supports brace-enclosed, comma-separated extensions (e.g., `'*.{csv,xls,xlsx}'`).
- `include_files` (bool | None): If True, include files. If False, exclude files. If None, defaults to True for standard patterns, True for files and False for directories for curly-brace patterns.
- `include_dirs` (bool | None): If True, include directories. If False, exclude directories. If None, defaults to True for standard patterns, False for curly-brace patterns.
- `**kwargs`: Passed to the underlying glob implementation for compatibility.

### Semantics

- Curly-brace patterns (e.g., `'*.{csv,xls,xlsx}'`) match any file (or directory, if enabled) with an extension in the set.
- Standard patterns (e.g., `'*.txt'`) behave exactly as in current pathlib.
- By default, curly-brace patterns match only files, not directories, for safety and convenience.

- The method yields `Path` objects matching the pattern and type criteria.

### Example

```python
from pathlib2.pathlib2 import Path2
files = [f for f in Path2('.').glob('*.{csv,xls,xlsx}')]
print(files)
```

## Alternatives Considered

### 1. Implement in `fnmatch`

Adding this brace expansion to `fnmatch` would allow pattern matching extend these capabilities to more use cases but the backwards compatibility 
footprint was a bit intimidating. In my view this could be the be a good answer but I don't know the use cases for `fnmatch`.

Adding a method like `glob_exts(['csv', 'xls', 'xlsx'])` is explicit but requires a "new" API to learn that is the same but different.

Adding this capability as a standalone package is possible, but given the ubiquitous nature of these operations it makes more sense in pathlib.


## Implementation Notes

- The current prototype subclasses `pathlib.Path` and overrides `glob` and `rglob` to support brace-enclosed, comma-separated extensions. In a real implementation, this logic would be integrated into the standard library's `pathlib.Path`.
- The implementation scans the directory once and filters files by extension, yielding results as `Path2` objects (or `Path` in the standard library).
- There is some ad-hackery going on to make this work with different version of python (that AI found for me)



## Limitations

- Prototype is for discussion and feedback; not production-ready.
- Edge cases (e.g., extensions with braces) are not handled.
- This code was nearly 100% written by AI, I guided it (ALOT), but it was an experiment on my part to see what happens if I commit to being a code boss rather than (trying to be) a boss coder.

## Potential Objections and Discussion

**Consistency with Python's glob module:**
One of the biggest risks with this proposal is that it introduces new pattern syntax and behavior (such as curly-brace expansion and file/dir filtering) to `pathlib` globbing, which differs from Python's standard `glob` module and other places where globbing is used. If users expect globbing to behave identically everywhere in Python, this could lead to confusion—especially for those who move between `glob.glob`, `Path.glob`, and other tools. The more places Python exposes globbing, the more important it is to keep the behavior consistent across the standard library. Careful documentation and clear separation of features are essential to mitigate this risk.

---
Prototype and rationale by Chuck, October 2025.

---

## Coverage

To check coverage locally:

```sh
pytest --cov=src/pathlib2 --cov-report=term-missing
```

- Coverage is measured only for the `src/pathlib2` directory.
- Compatibility code for Python < 3.13 is excluded from coverage.
- All configuration is in `pyproject.toml`.



