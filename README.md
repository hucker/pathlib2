## Case Sensitivity Options

The glob and rglob methods now support a `match_case` parameter to control case sensitivity:

- `MatchCase.SENSITIVE` (default): Case-sensitive matching for the entire filename and extension.
- `MatchCase.IGNORE`: Case-insensitive matching for the entire filename and extension.
- `MatchCase.IGNORE_EXTENSION`: Case-sensitive for the filename, case-insensitive for the extension only.

**Examples:**

```python
from pathlib2.pathlib2 import Path2, MatchCase

# Case-sensitive (default)
for f in Path2('.').glob('*.{csv,xls}', match_case=MatchCase.SENSITIVE):
    print(f)

# Case-insensitive (entire filename)
for f in Path2('.').glob('*.{csv,xls}', match_case=MatchCase.IGNORE):
    print(f)

# Case-insensitive (extension only)
for f in Path2('.').glob('*.{csv,xls}', match_case=MatchCase.IGNORE_EXTENSION):
    print(f)
```

See `test/test_case_sensitivity.py` for parameterized test cases covering all modes.
p = Path2('.')



# PEP Proposal: Seamless Multi-Extension Globbing for pathlib

## Abstract

This proposal aims to make multi-extension file filtering a seamless, drop-in enhancement for Python's `pathlib` glob methods. By supporting patterns like `*.{csv,xls,xlsx}` directly in `Path.glob` and `Path.rglob`, users can filter by multiple extensions with a single, expressive pattern—no extra loops, no manual filtering, and no boilerplate.

**Note:** The sample code below uses a subclass (`Path2`) for demonstration purposes only. The intent of this proposal is for this feature to be integrated directly into the standard `pathlib.Path` class.

## Motivation


Filtering files by multiple extensions is a common, real-world need in data science, automation, and scripting. Users expect to write:

```python
for f in Path('.').glob('*.{csv,xls,xlsx}'):
    ...
```

and have it "just work"—matching all relevant files, regardless of extension case or platform. Today, this requires verbose code, repeated directory scans, or custom utilities.

## Design Philosophy

- **Drop-in usability:** The enhanced globbing should work exactly like existing `pathlib` methods, with no new APIs to learn.
- **Expressiveness:** Users can specify multiple extensions in a single pattern, just as they would in Unix shells.
- **Efficiency:** The implementation avoids repeated directory scans and integrates with the standard globbing workflow.
- **Cross-platform:** The feature should behave consistently on all platforms, with a clear path to case-insensitive matching if desired.

## Specification (Prototype)

The prototype in `pathlib2.Path2` demonstrates this seamless experience:

```python
from pathlib2.pathlib2 import Path2

# Demonstration subclass: in a real implementation, this would be pathlib.Path
for f in Path2('.').glob('*.{csv,xls,xlsx}'):
    print(f)
```

No extra loops, no manual filtering—just a single, expressive pattern.

**In the proposed PEP, this would be:**

```python
from pathlib import Path
for f in Path('.').glob('*.{csv,xls,xlsx}'):
    print(f)
```

## Alternatives Considered

### 1. Implement in `fnmatch`

Adding brace expansion to `fnmatch` would allow pattern matching, but would not address efficient directory traversal or integrate with `pathlib`'s object-oriented API.

### 2. New `pathlib` method

Adding a method like `glob_exts(['csv', 'xls', 'xlsx'])` is explicit, but less discoverable and less consistent with shell-style globbing.

## Implementation Notes

- The current prototype subclasses `pathlib.Path` and overrides `glob` and `rglob` to support brace-enclosed, comma-separated extensions. In a real implementation, this logic would be integrated into the standard library's `pathlib.Path`.
- The implementation scans the directory once and filters files by extension, yielding results as `Path2` objects (or `Path` in the standard library).
- Case-insensitive matching is not yet implemented, but is a logical extension for cross-platform robustness.

## Limitations

- Prototype is for discussion and feedback; not production-ready.
- Edge cases (e.g., extensions with braces) are not handled.
- Case-insensitive matching is a future enhancement.

---
Prototype and rationale by Chuck, October 2025.


