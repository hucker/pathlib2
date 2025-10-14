import pathlib
from typing import Iterator

class PDirPath(pathlib.Path):
    """
    A subclass of pathlib.Path that extends glob and rglob to support patterns like:
    - '*.tif' (normal)
    - '*.{tif,jpg}' (multiple extensions)
    """
    _flavour = type(pathlib.Path())._flavour  # Required for pathlib subclassing

    def glob(self, pattern: str) -> Iterator[pathlib.Path]:
        return self._custom_glob(pattern, recursive=False)

    def rglob(self, pattern: str) -> Iterator[pathlib.Path]:
        return self._custom_glob(pattern, recursive=True)

    def _custom_glob(self, pattern: str, recursive: bool) -> Iterator[pathlib.Path]:
        dot_idx = pattern.rfind('.')
        if dot_idx == -1:
            # No extension, fallback to normal glob
            yield from (super().glob(pattern) if not recursive else super().rglob(pattern))
            return
        ext_part = pattern[dot_idx+1:]
        if ext_part.startswith('{') and ext_part.endswith('}'):
            exts = set(ext_part[1:-1].split(','))
            base_pattern = pattern[:dot_idx]
            # Remove trailing '*' or '?' from base_pattern for matching
            star_idx = base_pattern.rfind('*')
            q_idx = base_pattern.rfind('?')
            last_wild = max(star_idx, q_idx)
            if last_wild != -1:
                prefix = base_pattern[:last_wild+1]
            else:
                prefix = base_pattern
            # Use '**/*' for recursive, '*' for non-recursive
            search_pattern = '**/*' if recursive else '*'
            for p in super().rglob(search_pattern) if recursive else super().glob(search_pattern):
                if not p.is_file():
                    continue
                if not p.name.startswith(prefix.rstrip('*?')):
                    continue
                if p.suffix and p.suffix[1:] in exts:
                    yield p
        else:
            yield from (super().glob(pattern) if not recursive else super().rglob(pattern))
