
from enum import Enum, auto
import pathlib
import sys
from typing import Generator
from fnmatch import fnmatch

# Enum for case sensitivity options
class MatchCase(Enum):
    SENSITIVE = auto()
    IGNORE = auto()
    IGNORE_EXTENSION = auto()

class Path2(pathlib.Path):
    """
    Subclass of pathlib.Path with enhanced glob and rglob methods for multi-extension patterns.

    Supports patterns like '*.tif' (standard) and '*.{tif,jpg}' (multiple extensions).
    Numeric pattern support is not included; this class focuses on globbing and multi-extension patterns only.
    """

    # Only set _flavour for Python < 3.13
    if sys.version_info < (3, 13):
        _flavour = type(pathlib.Path())._flavour  # type: ignore[attr-defined]

    def glob(
        self,
        pattern: str,
        match_case: "MatchCase" = MatchCase.SENSITIVE,
        include_files: bool = True,
        include_dirs: bool = True
    ) -> Generator["Path2", None, None]:
        """
        Yield files and/or directories matching the given pattern, supporting multi-extension patterns and case sensitivity options.

        Args:
            pattern (str): Glob pattern. Supports brace-enclosed, comma-separated extensions (e.g., '*.{tif,jpg}').
            match_case (MatchCase): Case sensitivity mode (default: SENSITIVE).
            include_files (bool): If True, include files in results (default: True).
            include_dirs (bool): If True, include directories in results (default: True).

        Yields:
            pathlib2.Path2: Paths matching the pattern.

        Example:
            for f in Path2("/some/dir").glob("*.{tif,jpg}", match_case=MatchCase.IGNORE_EXTENSION, include_files=True, include_dirs=False):
                print(f)
        """
        return self._custom_glob(pattern, recursive=False, match_case=match_case, include_files=include_files, include_dirs=include_dirs)



    def rglob(
        self,
        pattern: str,
        match_case: "MatchCase" = MatchCase.SENSITIVE,
        include_files: bool = True,
        include_dirs: bool = True
    ) -> Generator["Path2", None, None]:
        """
        Recursively yield files and/or directories matching the given pattern, supporting multi-extension patterns and case sensitivity options.

        Args:
            pattern (str): Glob pattern. Supports brace-enclosed, comma-separated extensions (e.g., '*.{tif,jpg}').
            match_case (MatchCase): Case sensitivity mode (default: SENSITIVE).
            include_files (bool): If True, include files in results (default: True).
            include_dirs (bool): If True, include directories in results (default: True).

        Yields:
            pathlib2.Path2: Paths matching the pattern recursively.

        Example:
            for f in Path2("/some/dir").rglob("*.{tif,jpg}", match_case=MatchCase.IGNORE_EXTENSION, include_files=True, include_dirs=False):
                print(f)
        """
        return self._custom_glob(pattern, recursive=True, match_case=match_case, include_files=include_files, include_dirs=include_dirs)

    def _custom_glob(self, pattern: str, recursive: bool, match_case: "MatchCase", include_files: bool = True, include_dirs: bool = True) -> Generator["Path2", None, None]:
        """
        Internal helper for glob and rglob supporting multi-extension patterns, case sensitivity, and file/dir filtering.
        """
        dot_idx = pattern.rfind('.')
        def _filter_type(p):
            if p.is_file() and include_files:
                return True
            if p.is_dir() and include_dirs:
                return True
            return False
        if dot_idx == -1:
            for p in (super().glob(pattern) if not recursive else super().rglob(pattern)):
                if _filter_type(p):
                    yield p
            return
        ext_part = pattern[dot_idx+1:]
        if ext_part.startswith('{') and ext_part.endswith('}'):
            exts = set(ext_part[1:-1].split(','))
            pattern_fname = pattern[:dot_idx]
            search_pattern = '**/*' if recursive else '*'
            for p in super().rglob(search_pattern) if recursive else super().glob(search_pattern):
                name = p.name
                if '.' not in name:
                    continue
                fname, ext = name.rsplit('.', 1)
                if match_case == MatchCase.IGNORE:
                    # Fully case-insensitive: match filename and extension both case-insensitively
                    if not fnmatch(fname.lower(), pattern_fname.lower()):
                        continue
                    if ext.lower() in {e.lower() for e in exts} and _filter_type(p):
                        yield p
                elif match_case == MatchCase.IGNORE_EXTENSION:
                    # Extension-insensitive: filename part case-sensitive, extension case-insensitive
                    # If pattern_fname is '*', match all filenames
                    if pattern_fname == '*':
                        fname_match = True
                    else:
                        fname_match = fnmatch(fname, pattern_fname)
                    if not fname_match:
                        continue
                    if ext.lower() in {e.lower() for e in exts} and _filter_type(p):
                        yield p
                else:  # SENSITIVE
                    if not fnmatch(fname, pattern_fname):
                        continue
                    if ext in exts and _filter_type(p):
                        yield p
        else:
            for p in (super().glob(pattern) if not recursive else super().rglob(pattern)):
                if _filter_type(p):
                    yield p
