

import pathlib
import sys
from typing import Generator
from fnmatch import fnmatch



class Path2(pathlib.Path):

    def glob(
        self,
        pattern: str,
        include_files: 'bool | None' = None,
        include_dirs: 'bool | None' = None,
        **kwargs
    ) -> Generator["Path2", None, None]:
        """
        Yield files and/or directories matching the given pattern, supporting multi-extension patterns.

        Args:
            pattern (str): Glob pattern. Supports brace-enclosed, comma-separated extensions (e.g., '*.{tif,jpg}').
            include_files (bool|None): If True, include files in results. If None, defaults based on pattern.
            include_dirs (bool|None): If True, include directories in results. If None, defaults based on pattern.
            **kwargs: Passed to underlying pathlib glob.

        Yields:
            pathlib2.Path2: Paths matching the pattern.
        """
        pattern = str(pattern)
        dot_idx = pattern.rfind('.')
        ext_part = pattern[dot_idx+1:] if dot_idx != -1 else ''
        is_multi_ext = ext_part.startswith('{') and ext_part.endswith('}')
        # If user did not specify, set defaults based on pattern
        if is_multi_ext:
            if include_files is None:
                include_files = True
            if include_dirs is None:
                include_dirs = False
        else:
            if include_files is None:
                include_files = True
            if include_dirs is None:
                include_dirs = True
        yield from self._custom_glob(pattern, recursive=False, include_files=include_files, include_dirs=include_dirs, **kwargs)

    def rglob(
        self,
        pattern: str,
        include_files: 'bool | None' = None,
        include_dirs: 'bool | None' = None,
        **kwargs
    ) -> Generator["Path2", None, None]:
        """
        Recursively yield files and/or directories matching the given pattern, supporting multi-extension patterns.

        Args:
            pattern (str): Glob pattern. Supports brace-enclosed, comma-separated extensions (e.g., '*.{tif,jpg}').
            include_files (bool|None): If True, include files in results. If None, defaults based on pattern.
            include_dirs (bool|None): If True, include directories in results. If None, defaults based on pattern.
            **kwargs: Passed to underlying pathlib rglob.

        Yields:
            pathlib2.Path2: Paths matching the pattern recursively.
        """
        pattern = str(pattern)
        dot_idx = pattern.rfind('.')
        ext_part = pattern[dot_idx+1:] if dot_idx != -1 else ''
        is_multi_ext = ext_part.startswith('{') and ext_part.endswith('}')
        # If user did not specify, set defaults based on pattern
        if is_multi_ext:
            if include_files is None:
                include_files = True
            if include_dirs is None:
                include_dirs = False
        else:
            if include_files is None:
                include_files = True
            if include_dirs is None:
                include_dirs = True
        yield from self._custom_glob(pattern, recursive=True, include_files=include_files, include_dirs=include_dirs, **kwargs)

    """
    Subclass of pathlib.Path with enhanced glob and rglob methods for multi-extension patterns.

    Supports patterns like '*.tif' (standard) and '*.{tif,jpg}' (multiple extensions).
    Numeric pattern support is not included; this class focuses on globbing and multi-extension patterns only.
    """

    # Only set _flavour for Python < 3.13
    if sys.version_info < (3, 13):  # pragma: no cover
        _flavour = type(pathlib.Path())._flavour  # type: ignore[attr-defined]

    

    def _custom_glob(self, pattern: str, recursive: bool, include_files: bool = True, include_dirs: bool = True, **kwargs) -> Generator["Path2", None, None]:
        """
        Internal helper for glob and rglob supporting multi-extension patterns and file/dir filtering.
        """
        pattern = str(pattern)
        dot_idx = pattern.rfind('.')
        def _should_yield(p: pathlib.Path) -> bool:
            """
            Determine if a path should be yielded based on include_files and include_dirs flags.

            Args:
                p (pathlib.Path): The path to check.
            Returns:
                bool: True if the path should be yielded (file and include_files is True, or directory and include_dirs is True),
                      False otherwise.
                      - True: Yield this path in the glob results.
                      - False: Do not yield this path.
            """
            if p.is_file() and include_files:
                return True
            if p.is_dir() and include_dirs:
                return True
            return False
        if dot_idx == -1:
            for p in (super().glob(pattern, **kwargs) if not recursive else super().rglob(pattern, **kwargs)):
                if _should_yield(p):
                    yield p
            return
        ext_part = pattern[dot_idx+1:]
        if ext_part.startswith('{') and ext_part.endswith('}'):
            exts = set(ext_part[1:-1].split(','))
            pattern_fname = pattern[:dot_idx]
            search_pattern = '**/*' if recursive else '*'
            for p in super().rglob(search_pattern, **kwargs) if recursive else super().glob(search_pattern, **kwargs):
                name = p.name
                if '.' not in name:
                    continue
                fname, ext = name.rsplit('.', 1)
                if not fnmatch(fname, pattern_fname):
                    continue
                if ext in exts and _should_yield(p):
                    yield p
        else:
            for p in (super().glob(pattern, **kwargs) if not recursive else super().rglob(pattern, **kwargs)):
                if _should_yield(p):
                    yield p
