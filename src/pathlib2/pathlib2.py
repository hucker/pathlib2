
import pathlib
from typing import Generator
from fnmatch import fnmatch



class Path2(pathlib.Path):
    """
    Subclass of pathlib.Path with enhanced glob and rglob methods for multi-extension patterns.

    Supports patterns like '*.tif' (standard) and '*.{tif,jpg}' (multiple extensions).
    Numeric pattern support is not included; this class focuses on globbing and multi-extension patterns only.
    """
    _flavour = type(pathlib.Path())._flavour  # type: ignore[attr-defined]  # Required for pathlib subclassing



    def glob(
        self,
        pattern: str,
        *,
        case_sensitive: bool | None = None
    ) -> Generator["Path2", None, None]:
        """
        Yield files matching the given pattern, supporting multi-extension patterns.

        Args:
            pattern (str): Glob pattern. Supports brace-enclosed, comma-separated extensions (e.g., '*.{tif,jpg}').

        Yields:
            pathlib.Path: Paths matching the pattern.

        Example:
            for f in Path2("/some/dir").glob("*.{tif,jpg}"):
                print(f)
        """
        return self._custom_glob(pattern, recursive=False)



    def rglob(
        self,
        pattern: str,
        *,
        case_sensitive: bool | None = None
    ) -> Generator["Path2", None, None]:
        """
        Recursively yield files matching the given pattern, supporting multi-extension patterns.

        Args:
            pattern (str): Glob pattern. Supports brace-enclosed, comma-separated extensions (e.g., '*.{tif,jpg}').

        Yields:
            pathlib.Path: Paths matching the pattern recursively.

        Example:
            for f in Path2("/some/dir").rglob("*.{tif,jpg}"):
                print(f)
        """
        return self._custom_glob(pattern, recursive=True)

    def _custom_glob(self, pattern: str, recursive: bool) -> Generator["Path2", None, None]:
        """
        Internal helper for glob and rglob supporting multi-extension patterns.

        Args:
            pattern (str): Glob pattern, possibly with brace-enclosed extensions.
            recursive (bool): Whether to search recursively (rglob) or not (glob).

        Yields:
            pathlib.Path: Paths matching the pattern.
        """
        dot_idx = pattern.rfind('.')
        if dot_idx == -1:
            # No extension, fallback to normal glob
            yield from (super().glob(pattern) if not recursive else super().rglob(pattern))
            return
        ext_part = pattern[dot_idx+1:]
        if ext_part.startswith('{') and ext_part.endswith('}'):
            exts = set(ext_part[1:-1].split(','))
            # Replace the extension in the pattern with .*
            base_pattern = pattern[:dot_idx] + ".*"
            search_pattern = '**/*' if recursive else '*'
            for p in super().rglob(search_pattern) if recursive else super().glob(search_pattern):
                # Match the base pattern (with .*):
                if not fnmatch(p.name, base_pattern):
                    continue
                # Check extension after last dot
                file_ext = p.name.rsplit('.', 1)[-1]
                if file_ext in exts:
                    yield p
        else:
            yield from (super().glob(pattern) if not recursive else super().rglob(pattern))
