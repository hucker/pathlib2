
import os
import shutil
import tempfile
import pytest
from pathlib2.pathlib2 import Path2

@pytest.mark.parametrize(
    "filenames,pattern,expected",
    [
        # No matches
        (["a.tif", "b.tif"], "*.{pdf,doc}", []),
        # Files with no extension
        (["foo", "bar.tif"], "*.{tif,jpg}", ["bar.tif"]),
        # Hidden files
        ([".hidden.tif", "visible.tif"], "*.{tif}", [".hidden.tif", "visible.tif"]),
        # Multiple dots
        (["foo.bar.tif", "baz.tif"], "*.{tif}", ["foo.bar.tif", "baz.tif"]),
        # Trailing comma
        (["a.tif", "b.jpg"], "*.{tif,}", ["a.tif"]),
        # Single extension in braces
        (["a.tif", "b.jpg"], "*.{tif}", ["a.tif"]),
    ]
)
def test_edge_cases_multi_extension(tmp_path, filenames, pattern, expected):
    # Create files
    for fname in filenames:
        (tmp_path / fname).touch()
    p = Path2(tmp_path)
    found = sorted([f.name for f in p.glob(pattern)])
    assert found == sorted(expected)

 
@pytest.fixture
def temp_dir_with_files():
    temp_dir = tempfile.mkdtemp()
    files = [
        'a.tif', 'b.tif', 'c.jpg', 'd.png', 'e.txt', 'f.tif', 'g.jpg', 'h.docx'
    ]
    for fname in files:
        open(os.path.join(temp_dir, fname), 'w').close()
    yield temp_dir
    shutil.rmtree(temp_dir)

def test_glob_normal_pattern(temp_dir_with_files):
    p = Path2(temp_dir_with_files)
    tif_files = sorted([f.name for f in p.glob('*.tif')])
    assert tif_files == ['a.tif', 'b.tif', 'f.tif']



@pytest.mark.parametrize(
    "pattern,expected",
    [
        ('*.{tif}', ['a.tif', 'b.tif', 'f.tif']),
        ('*.{jpg}', ['c.jpg', 'g.jpg']),
        ('*.{tif,jpg}', ['a.tif', 'b.tif', 'c.jpg', 'f.tif', 'g.jpg']),
        ('*.{tif,jpg,png}', ['a.tif', 'b.tif', 'c.jpg', 'd.png', 'f.tif', 'g.jpg']),
        ('*.{tif,jpg,docx}', ['a.tif', 'b.tif', 'c.jpg', 'f.tif', 'g.jpg', 'h.docx']),
    ]
)
def test_glob_multi_extension_pattern(temp_dir_with_files, pattern, expected):
    p = Path2(temp_dir_with_files)
    files = sorted([f.name for f in p.glob(pattern)])
    assert files == sorted(expected)

def test_rglob_multi_extension_pattern(temp_dir_with_files):
    # Create subdir and add files
    p = Path2(temp_dir_with_files)
    subdir = p / 'sub'
    subdir.mkdir()
    (subdir / 'x.tif').touch()
    (subdir / 'y.jpg').touch()
    files = sorted([f.name for f in p.rglob('*.{tif,jpg}') if (subdir / f.name).is_file() or (p / f.name).is_file()])
    assert 'x.tif' in files and 'y.jpg' in files
