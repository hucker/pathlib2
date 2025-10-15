import pytest
from pathlib2.pathlib2 import Path2

def setup_files_and_dirs(tmp_path, files, dirs):
    for fname in files:
        (tmp_path / fname).write_text("data")
    for dname in dirs:
        (tmp_path / dname).mkdir()

def test_glob_no_dot(tmp_path):
    # Pattern with no dot should match all files and dirs
    files = ['foo', 'bar.txt', 'baz.csv']
    dirs = ['adir']
    setup_files_and_dirs(tmp_path, files, dirs)
    found = sorted(f.name for f in Path2(tmp_path).glob('*'))
    assert set(found) == set(files + dirs)

def test_glob_malformed_braces(tmp_path):
    # Malformed brace pattern should not crash and should fallback to normal glob
    files = ['foo.txt', 'bar.txt']
    setup_files_and_dirs(tmp_path, files, [])
    found = sorted(f.name for f in Path2(tmp_path).glob('*.{txt'))
    assert found == []
    found2 = sorted(f.name for f in Path2(tmp_path).glob('*.txt}'))
    assert found2 == []

def test_glob_include_files_dirs_options(tmp_path):
    files = ['a.txt', 'b.txt']
    dirs = ['adir']
    setup_files_and_dirs(tmp_path, files, dirs)
    # Only files
    found_files = sorted(f.name for f in Path2(tmp_path).glob('*', include_files=True, include_dirs=False))
    assert set(found_files) == set(files)
    # Only dirs
    found_dirs = sorted(f.name for f in Path2(tmp_path).glob('*', include_files=False, include_dirs=True))
    assert set(found_dirs) == set(dirs)
    # Both
    found_both = sorted(f.name for f in Path2(tmp_path).glob('*', include_files=True, include_dirs=True))
    assert set(found_both) == set(files + dirs)

def test_rglob_multi_ext(tmp_path):
    files = ['a.csv', 'b.xls', 'c.xlsx', 'd.txt']
    subdir = tmp_path / 'subdir'
    subdir.mkdir()
    for fname in files:
        (subdir / fname).write_text("data")
    found = sorted(f.name for f in Path2(tmp_path).rglob('*.{csv,xls,xlsx}'))
    assert set(found) == {'a.csv', 'b.xls', 'c.xlsx'}


