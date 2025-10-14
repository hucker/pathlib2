# Proposal: Multi-Extension Globbing for pathlib2.Path2

## Abstract
This document describes the `pathlib2` package, which provides a `Path2` class supporting multi-extension glob patterns, such as `*.{csv,xls,xlsx}`. This feature addresses a common need in data science, programming, and system scripting, and provides a more efficient and expressive API for file selection.

## Motivation
Matching files with multiple extensions is a frequent requirement in many domains:
 - Data science: `*.csv`, `*.xls`, `*.xlsx`
 - Programming: `*.c`, `*.cpp`, `*.h`
 - Text processing: `*.txt`, `*.dat`
 - System operations: `*.zip`, `*.tar`, `*.gzip`

Currently, users often implement this by iterating over a list of extensions and calling glob multiple times, or by writing double-nested loops. This is inefficient, as it requires scanning the directory tree multiple times, and leads to verbose, error-prone code.

## Rationale
By encapsulating multi-extension globbing in the `pathlib2.Path2` API, this package provides a single, efficient directory scan and a concise, readable interface. This approach is more natural for users who are already working with modern path objects, and keeps the implementation footprint small and focused. It also aligns with patterns found in Unix shells and other scripting environments.

## Specification (Prototype)
This package provides `pathlib2.Path2` with support for multi-extension patterns:

p = PDirPath('.')

```python
from pathlib2.pathlib2 import Path2

p = Path2('.')
for f in p.glob('*.{csv,xls,xlsx}'):
    print(f)
```

 - This feature is implemented in `pathlib2.Path2`, where most users expect to find advanced path and globbing functionality.
 - While it is possible to extend globbing by modifying the `glob` or `fnmatch` modules, this approach keeps the logic close to the path object and is more discoverable for users.
 - In practice, most users who need this pattern are already using `pathlib`, and this approach keeps the implementation footprint small and focused.
 - If you need to match extensions that contain curly braces (`{}`), an escape mechanism may be required. This is not currently implemented, but could be added for edge cases.

- A case-insensitive flag could be added in the future to support matching extensions regardless of case (e.g., matching both `.JPG` and `.jpg`). This is not currently implemented, but is a common user request and would further improve usability, especially on case-sensitive filesystems.

## Limitations
 - This is a prototype and not a production-ready package.

---
Prototype and rationale by Chuck, October 2025.
