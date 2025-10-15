# AI CONTEXT: Coding Style and Requirements

## Coding Standards for This Project

When generating or editing code for this project, always adhere to the following requirements:

### 1. Docstrings

- Every function and method must include a docstring.
- Use **Google-style docstrings** for all functions, methods, and classes.
- Docstrings should clearly describe the purpose, parameters, return values, exceptions, and any side effects.

### 2. Type Hinting

- Use Python **3.10+ type hinting** syntax throughout the codebase.
- Prefer built-in collection types (e.g., `list`, `dict`) over `typing.List`, `typing.Dict` unless generics are required.
- Use `|` (PEP 604) for union types (e.g., `str | None`).

### 3. Imports

- Always import the `datetime` module as `import datetime as dt`.
- Do not use `from datetime import ...` or `import datetime` without aliasing as `dt`.

### 4. General Style

- All public and private functions/methods must have a docstring, even if brief.
- Use ruff for formatting with autofix.
- Use descriptive parameter and variable names.

### 5. Example Function Template

```python
def example_function(arg1: int, arg2: str | None = None) -> bool:
    """
    Brief summary of what the function does.

    Args:
        arg1 (int): Description of arg1.
        arg2 (str | None, optional): Description of arg2. Defaults to None.

    Returns:
        bool: Description of the return value.
    """
    # ...function body...
```

### Formatting

- Always run ruff before checkin (with autofix)
- Always run mypi before checkin
- When generating markdown # headings should have a line before and after
- When generating - list the - should be the first character on the line no spaces.
- When generating any markdown there should not be more than  one empty line in a row
- When generating markdown the first line must not be blank
- When generating markdown the last line should be a blank

### 6. AI Instructions

- When asked to generate or refactor code, always follow the above rules.
- If you see code that does not follow these rules, suggest or make corrections.
- If a function or method is missing a docstring, add one in Google style.
- If type hints are missing or not using 3.10+ syntax, update them.
- Always use `import datetime as dt` for any datetime usage.

---
This file is intended for use as AI prompt context to enforce coding standards and style for this project.
