import os
import pytest
from pathlib2.pathlib2 import Path2

def make_file_and_dir(tmp_path, name):
    # Create a file and a directory with the same name
    (tmp_path / name).touch()
    (tmp_path / (name + '_dir')).mkdir()
    # Also create a directory with an extension
    (tmp_path / (name + '.dir')).mkdir()

@pytest.fixture
def file_dir_ext_structure(tmp_path):
    # Files: foo.jpg, bar.jpg, baz.txt
    # Dirs: foo_dir.jpg, bar_dir.jpg, baz_dir.txt
    (tmp_path / 'foo.jpg').touch()
    (tmp_path / 'bar.jpg').touch()
    (tmp_path / 'baz.txt').touch()
    (tmp_path / 'foo_dir.jpg').mkdir()
    (tmp_path / 'bar_dir.jpg').mkdir()
    (tmp_path / 'baz_dir.txt').mkdir()
    return tmp_path

def test_glob_multi_ext_default_files_only(file_dir_ext_structure):
    p = Path2(file_dir_ext_structure)
    result = sorted([f.name for f in p.glob('*.{jpg}')])
    assert result == ['bar.jpg', 'foo.jpg']

def test_glob_single_ext_files_and_dirs(file_dir_ext_structure):
    p = Path2(file_dir_ext_structure)
    result = sorted([f.name for f in p.glob('*.jpg')])
    assert set(result) == {'bar.jpg', 'foo.jpg', 'bar_dir.jpg', 'foo_dir.jpg'}
    # Confirm both file and dir exist
    assert any((p / name).is_file() for name in result)
    assert any((p / name).is_dir() for name in result)

def test_glob_single_ext_dirs_only(file_dir_ext_structure):
    p = Path2(file_dir_ext_structure)
    result = sorted([f.name for f in p.glob('*.jpg', include_files=False, include_dirs=True)])
    assert result == ['bar_dir.jpg', 'foo_dir.jpg']
    assert all((p / name).is_dir() for name in result)

def test_glob_multi_ext_dirs_only(file_dir_ext_structure):
    p = Path2(file_dir_ext_structure)
    result = sorted([f.name for f in p.glob('*.{jpg}', include_files=False, include_dirs=True)])
    assert result == ['bar_dir.jpg', 'foo_dir.jpg']
    assert all((p / name).is_dir() for name in result)

def test_glob_multi_ext_files_and_dirs(file_dir_ext_structure):
    p = Path2(file_dir_ext_structure)
    result = sorted([f.name for f in p.glob('*.{jpg}', include_files=True, include_dirs=True)])
    assert set(result) == {'bar.jpg', 'foo.jpg', 'bar_dir.jpg', 'foo_dir.jpg'}
    assert any((p / name).is_file() for name in result)
    assert any((p / name).is_dir() for name in result)
