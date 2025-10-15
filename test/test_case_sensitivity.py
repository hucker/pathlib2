# --- All imports at the top ---
import pytest
import os
import sys
from pathlib2.pathlib2 import Path2, MatchCase



# --- Helper and fixture definitions ---
def get_unique_case_insensitive(files):
    """On case-insensitive filesystems, only unique (casefolded) filenames can exist."""
    seen = set()
    unique = []
    for f in files:
        f_ci = f.casefold()
        if f_ci not in seen:
            seen.add(f_ci)
            unique.append(f)
    return unique

# Files with NO full filename collisions (safe for all platforms)
NON_COLLIDING_FILES = [
    "foo.csv", "bar.xls", "baz.CSV", "foo.txt", "README.md",
    "baz.Txt", "ReadMe.MD", "MiXeD.TxT", "MiXeD.CsV",
    "case1.TxT", "case2.txt", "unique.UPPER", "unique.lower"
]

# Files WITH case-colliding names (only for case-sensitive platforms)
COLLIDING_FILES = [
    "foo.txt", "FOO.TXT", "foo.TXT"
]

@pytest.fixture(scope="module")
def shared_file_dir_no_collisions(tmp_path_factory):
    d = tmp_path_factory.mktemp("casefiles_nocollide")
    files = NON_COLLIDING_FILES
    for fname in files:
        (d / fname).touch()
    return d

@pytest.fixture(scope="module")
def shared_file_dir_with_collisions(tmp_path_factory):
    d = tmp_path_factory.mktemp("casefiles_collide")
    files = COLLIDING_FILES
    for fname in files:
        (d / fname).touch()
    return d


def is_case_insensitive_fs():
    # Windows is always case-insensitive; macOS default FS is case-insensitive
    return os.name == "nt" or (sys.platform == "darwin")



# --- 1. Tests with NO filename collisions: run on all platforms ---
@pytest.mark.parametrize(
    "pattern,match_case,expected,desc",
    [
        # On case-insensitive FS, all case variants match for SENSITIVE/IGNORE/IGNORE_EXTENSION
        ("*.csv", MatchCase.SENSITIVE,
            ["foo.csv", "baz.CSV", "MiXeD.CsV"],
            "Case-insensitive FS: all .csv/.CSV variants match for SENSITIVE" if is_case_insensitive_fs() else "Case-sensitive: only matches .csv exactly"),
        ("*.csv", MatchCase.IGNORE,
            ["foo.csv", "baz.CSV", "MiXeD.CsV"],
            "Case-insensitive: matches all .csv/.CSV variants"),
        ("*.csv", MatchCase.IGNORE_EXTENSION,
            ["foo.csv", "baz.CSV", "MiXeD.CsV"],
            "Extension-insensitive: matches all .csv/.CSV variants, case-sensitive filename"),
        ("*.TXT", MatchCase.SENSITIVE,
            ["baz.Txt", "MiXeD.TxT", "case1.TxT", "foo.txt", "case2.txt"],
            "Case-insensitive FS: all .TXT/.Txt/.TxT/.txt variants match for SENSITIVE" if is_case_insensitive_fs() else "Case-sensitive: only matches .Txt and .TxT exactly"),
        ("*.TXT", MatchCase.IGNORE,
            ["baz.Txt", "MiXeD.TxT", "case1.TxT", "foo.txt", "case2.txt"],
            "Case-insensitive: matches all .TXT/.Txt/.TxT/.txt variants"),
        ("*.TXT", MatchCase.IGNORE_EXTENSION,
            ["baz.Txt", "MiXeD.TxT", "case1.TxT", "foo.txt", "case2.txt"],
            "Extension-insensitive: matches all .TXT/.Txt/.TxT/.txt variants, case-sensitive filename"),
    ]
)
def test_no_collision_case_patterns(shared_file_dir_no_collisions, pattern, match_case, expected, desc):
    p = Path2(shared_file_dir_no_collisions)
    found = [f.name for f in p.glob(pattern, match_case=match_case)]
    assert set(found) == set(expected), desc


# --- 2. Tests that REQUIRE filename collisions: skip on case-insensitive FS ---
@pytest.mark.skipif(is_case_insensitive_fs(), reason="Requires case-sensitive filesystem for filename collisions.")
@pytest.mark.parametrize(
    "pattern,match_case,expected,desc",
    [
        ("*.TXT", MatchCase.SENSITIVE, ["foo.TXT"], "Case-sensitive: only matches .TXT exactly"),
        ("*.TXT", MatchCase.IGNORE, ["foo.txt", "FOO.TXT", "foo.TXT"], "Case-insensitive: matches all .txt/.TXT variants"),
    ]
)
def test_collision_case_patterns(shared_file_dir_with_collisions, pattern, match_case, expected, desc):
    p = Path2(shared_file_dir_with_collisions)
    found = [f.name for f in p.glob(pattern, match_case=match_case)]
    assert set(found) == set(expected), desc


# --- Platform-specific filename case tests ---
@pytest.mark.skipif(
    is_case_insensitive_fs(),
    reason="Only runs on case-sensitive filesystems (e.g. Linux)",
)
def test_case_sensitive_filesystem_distinct(tmp_path):
    # On case-sensitive FS, both files can exist and be found
    (tmp_path / "test.csv").touch()
    (tmp_path / "test.CSV").touch()
    files = {f.name for f in Path2(tmp_path).glob("test.*")}
    assert files == {
        "test.csv",
        "test.CSV",
    }, "Both files should exist and be found on case-sensitive filesystems"


@pytest.mark.skipif(
    not is_case_insensitive_fs(),
    reason="Only runs on case-insensitive filesystems (e.g. Windows/macOS)",
)
def test_case_insensitive_filesystem_collapse(tmp_path):
    # On case-insensitive FS, only one file will exist (the last one created wins)
    (tmp_path / "test.csv").touch()
    (tmp_path / "test.CSV").touch()
    files = {f.name for f in Path2(tmp_path).glob("test.*")}
    # Only one file will be present, and its name will be the last one created
    assert len(files) == 1, "Only one file should exist on case-insensitive filesystems"



# --- Parametrized multi-extension and case tests (removed old test_case_sensitivity) ---
