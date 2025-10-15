import pytest
from pathlib2.pathlib2 import Path2

@pytest.fixture
def legacy_test_dir(tmp_path):
    """Create files and dirs for legacy/pathlib compatibility tests."""
    (tmp_path / 'foo.txt').touch()
    (tmp_path / 'bar.txt').touch()
    (tmp_path / 'baz.md').touch()
    (tmp_path / 'dir.txt').mkdir()
    (tmp_path / 'subdir').mkdir()
    return tmp_path

def test_legacy_glob_behavior(legacy_test_dir):
    """Legacy glob/rglob matches files and dirs with .txt extension (backward compatible)."""
    p = Path2(legacy_test_dir)
    result = sorted([f.name for f in p.glob('*.txt')])
    assert set(result) == {'foo.txt', 'bar.txt', 'dir.txt'}
    result = sorted([f.name for f in p.rglob('*.txt')])
    assert 'foo.txt' in result and 'bar.txt' in result and 'dir.txt' in result

def test_new_behavior_curly_braces(legacy_test_dir):
    """Curly brace pattern matches only files by default (new behavior)."""
    p = Path2(legacy_test_dir)
    result = sorted([f.name for f in p.glob('*.{txt}')])
    assert set(result) == {'foo.txt', 'bar.txt'}
    result = sorted([f.name for f in p.glob('*.{txt}', include_dirs=True, include_files=False)])
    assert set(result) == {'dir.txt'}

def test_new_behavior_explicit_flags(legacy_test_dir):
    """Explicit include_files/include_dirs flags change legacy behavior."""
    p = Path2(legacy_test_dir)
    result = sorted([f.name for f in p.glob('*.txt', include_files=True, include_dirs=False)])
    assert set(result) == {'foo.txt', 'bar.txt'}
    result = sorted([f.name for f in p.glob('*.txt', include_files=False, include_dirs=True)])
    assert set(result) == {'dir.txt'}
