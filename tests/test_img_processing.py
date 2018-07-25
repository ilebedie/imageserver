import pytest
import pathlib
from image_processing import make_thumbnail

BASE_DIR = pathlib.Path(__file__).parent


def test_thumbnails():
    asset_path = BASE_DIR / 'assets' / 'test.jpg'
    out_path = BASE_DIR / 'assets' / 'out.jpg'
    with open(asset_path, 'rb') as f:
        thumbnail_buf = make_thumbnail(f.read(), target_size=200)
        with open(out_path, 'wb') as out:
            out.write(thumbnail_buf)
